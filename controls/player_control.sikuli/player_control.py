from sikuli import *
from screenshots import *
from global_config import *
import helper
import time
from threading import Thread

class Player(object):

    def __init__(self, region):
        self.region = region

    def get_value_of_progress_bar(self):
        ret = 0.0
        try:
            ret = float(
                helper.run_apple_script("value_process_bar_player.applescript").rstrip("\n"))
        except:
            pass
        return ret

    def maximize(self):
        helper.run_apple_script("maximize_player.applescript")

    def close(self):
        helper.run_apple_script("close_player.applescript")

    def download(self):
        if self.region.exists(download_button_in_player_window):
            self.region.click(download_button_in_player_window)
            return True
        return False, "Fail to find 'Download' button from 'Player window'"

    def upload(self):
        if self.region.exists(upload_button_in_player_window):
            self.region.click(upload_button_in_player_window)
            return True
        return False, "Fail to find 'Upload' button from 'Player window'"

    def is_playing(self):
        return self.get_value_of_progress_bar() > 0

    def play(self):
        helper.run_apple_script("play_player.applescript")

    def stop(self):
        helper.run_apple_script("stop_player.applescript")

    def restart(self):
        self.stop()
        self.play()

    def wait_till_start_playing(self, timeout=30):
        start = time.time()
        while not self.is_playing():
            if (time.time() - start) > timeout:
                return False, "Timeout for waiting to start playing in Player window"
            time.sleep(2)
        return True

    def reset_process_bar(self):
        helper.rerun_apple_script("reset_value_process_bar_player.applescript", 5)

    def get_title(self):
        return helper.run_apple_script("get_title_of_player.applescript").rstrip('\n')

    def set_to_original_size(self):
        helper.run_apple_script("set_original_size_of_player.applescript")

    def make_overlay_display(self):
        size = self._get_size_of_window()
        position = self._get_position_of_window()
        if len(size) != 2 or len(position) != 2:
            return False, "Fail to get size and position of player window"
        for i in range(2):
            self.region.hover(Location(position[0], position[1]))
            self.region.hover(Location(position[0] + size[0], position[1] + size[1]))

    def _get_size_of_window(self):
        return self._parse_ret(helper.run_apple_script("get_size_of_player.applescript"))

    def _get_position_of_window(self):
        return self._parse_ret(helper.run_apple_script("get_position_of_player.applescript"))

    def _parse_ret(self, ret):
        ret = ret.replace('{', '').replace('}', '')
        return [int(i) for i in ret.split(',')]


class VerifyPlay(object):

    def __init__(self, timeout, *screenshots):
        self.num_of_screenshots = len(screenshots)
        self.threads = [None] * self.num_of_screenshots
        self.results = [None] * self.num_of_screenshots

        for i in range(self.num_of_screenshots):
            self.threads[i] = Thread(target=self._exist, args=(screenshots[i], timeout, i))

    def _exist(self, image, timeout, index):
        self.results[index] = region.exists(image, timeout)

    def start(self):
        for t in self.threads:
            t.start()

    def wait(self):
        for t in self.threads:
            t.join()

    def verify_result(self):
        failed_index = [str(i+1) for i in range(self.num_of_screenshots) if self.results[i] is None]
        if len(failed_index) != 0:
            return False, "Playback verification got failed, cannot find screenshots for numbers \"" + ",".join(failed_index) + "\""
        return True
