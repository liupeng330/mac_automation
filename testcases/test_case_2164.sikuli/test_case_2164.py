from nose.plugins.attrib import attr
from helper import *
from sikuli import *
from global_config import *

from controls.sign_in_control import *
from controls.rt_control import *
from controls.system_tray_control import *
from controls.player_control import *

import ops.operations as op

from base import *
from datetime import datetime
from threading import Thread
import unittest


class TestCase_2164(TestCase_Base):

    """ Story: Create and Publish a RealTime Story """

    def _check_items_exists(self):
        # verify test clips are all in the view
        log("Verify test clip is in the view")
        for i in range(len(story_play_items)):
            assert region.exists(story_play_items[i], default_wait_time), "Fail to find screenshot of number " + str(i + 1) + "in library view"

    def setUp(self):
        try:
            TestCase_Base.setUp(self)
            self.player = Player(region)
        except:
            TestCase_Base.tearDown(self)
            raise

    def _create_story(self):
        op.launch_RT_before_running_case()

        log("Remove all items first")
        assert_step(self.RT.remove_all())

        # test clip
        self.test_files = ["Playback_1_1.mp4", "Playback_1_2.mp4", "Playback_2_1.mp4", "Playback_2_2.mp4", "Playback_3_1.mp4", "Playback_3_2.mp4"]

        # upload test files to cloud
        upload_video_files_via_API(*self.test_files)

        # switch to cloud view
        assert_step(self.RT.switch_to_cloud_view())

        # verify upload
        self._check_items_exists()

        log("Switch to 'Stories -> Suggested' view")
        self.RT.switch_to_stories_suggested_view()

        log("Verify whether suggested story exists or not")
        assert region.exists(suggested_story_icon, default_wait_time), "Fail to find 'Suggested story icon' in 'Stories -> Suggested' view"

    @attr('BVT')
    def test_create_and_preview_story(self):
        self._create_story()

        log("Preview it")
        self.RT.play_video(suggested_story_icon)

        log("Verify test clip is played")
        assert_step(self.RT.wait_till_start_playing())

        log("Restore the window size of RealTimes")
        self.RT.restore_windows_size()

        log("Set value of playing process bar value to 0")
        self.RT.reset_play_process_bar()

        log("Verify playback")
        self._verify_playback()

    @attr('BVT')
    def test_create_and_publish_story(self):
        self._create_story()

        log("Upload suggested story to cloud")
        self.RT.upload_story()

        expected_story_name = "My Story - " + datetime.now().strftime("%b %d, %Y")
        log("Verify whether suggested story with name '{0}' is uploaded to cloud or not".format(expected_story_name))
        assert wait_for_upload_complete(expected_story_name, 60 * 5), "Fail to find story '{0}' from cloud, after waiting for 5 minutes".format(expected_story_name)

        expected_story_file_name = os.path.join(saved_stories_folder, expected_story_name + ".mov")
        log("Verify whether saved story '{0}' exists in local system".format(expected_story_file_name))
        assert os.path.exists(expected_story_file_name), "Fail to find saved story file '{0}'".format(expected_story_file_name)

        log("Exit gallery view")
        self.RT.exit_gallery_view()

        log("Switch to 'Stories -> Cloud' view")
        self.RT.switch_to_stories_cloud_view()
        assert self.RT.does_exist_in_library(expected_story_name, expected_story_name, default_wait_time), \
            "Fail to find uploaded story item in 'Stories -> Cloud' view"

        log("Play it")
        self.RT.play_video(story_item)

        log("Verify test clip is played")
        assert_step(self.RT.verify_rt_is_playing_video())

        log("Click 'play_in_separate_window_button'")
        self.RT.play_in_seperate_window()

        log("Wait player start to play")
        assert_step(self.player.wait_till_start_playing())

        log("Set player window to original size")
        self.player.set_to_original_size()

        log("Restart to play")
        self.player.reset_process_bar()

        log("Verify playback")
        self._verify_playback()

    @unittest.skip('Not implement')
    @attr('BVT')
    def test_share_story(self):
        raise NotImplementedError
        self._create_story()

        log("Share story")
        assert_step(self.RT.share_story(suggested_story_icon, wait_time=60*5))

    def _verify_playback(self):
        play_verify = VerifyPlay(30, *story_play_nums)
        play_verify.start()
        play_verify.wait()
        assert_step(play_verify.verify_result())

    def tearDown(self):
        TestCase_Base.tearDown(self)
