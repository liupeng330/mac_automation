from sikuli import *
from screenshots import *
from global_config import *
import helper
import os
import time


class RT(object):

    def __init__(self, region):
        self.region = region

    def launch(self):
        """ launch RT """

        self.app = App(app_name)
        helper.log("Opening RT")
        while self.app.open() == None:
            helper.log("Opening RT is failed, retry!!")
            time.sleep(5)
        helper.log("Focusing RT")
        self.app.focus()

    def maximize(self):
        helper.run_apple_script("maximize_rt.applescript")

    def maximize_separate_playback_window(self):
        helper.run_apple_script("maximize_playback_separate_window.applescript")

    def restore_windows_size(self):
        helper.run_apple_script("restore_rt.applescript")

    def reset_play_process_bar(self):
        helper.rerun_apple_script("reset_value_process_bar_play_gallery_view.applescript", 5)

    def sign_out(self):
        """ sign out from RT account setting menu """

        helper.log("Click account setting button on top bar")
        if self.region.exists(account_setting_button_top_bar, default_wait_time):
            self.region.click(account_setting_button_top_bar)
            helper.log("Click sign out button")
            self.region.click(sign_out_button_in_account_setting_button_top_bar)
            return True
        return False, "Fail to find 'Account setting button on top bar of RealTimes"

    @property
    def is_sign_in(self):
        return self.region.exists(has_signed_in_rt_top_bar, default_wait_time)

    def set_to_init_env(self):
        # need to sign in first
        if not self.is_sign_in:
            return False, "RealTimes is not in signed in status!!"

        # maximize RT
        self.maximize()

        # check if current is in gallery view
        self.make_overlay_display()
        if self.is_in_gallery_view():
            self.exit_gallery_view()

        # check if 'Photos&Videos' is selected
        if self.region.exists(photos_and_videos_button_selected, default_wait_time):
            self.region.click(photos_and_videos_button_selected)
        else:
            return False, "Fail to find 'Photos & Videos' button"
        helper.assert_step(self.switch_to_all_view())
        return True

    def quit(self):
        self.app.close()

    def play_video(self, item, name=''):
        if self.region.exists(item, default_wait_time):
            self.region.doubleClick(item)
            return True
        elif helper.check_exist_by_cliclick(name):
            helper.double_click_item_by_cliclick(name)
            return True
        else:
            return False, "Fail to find item in library view before playing it"

    def play_in_seperate_window(self):
        self.region.click(play_in_separate_window_button)

    def play_with_slideshow(self):
        self.region.click(play_as_slideshow_button)

    def play_with_slideshow_for_album(self, item):
        self.region.rightClick(item)
        time.sleep(2)
        type('sl')
        time.sleep(2)
        type(Key.ENTER)

    def click_left_arrows_button_in_gallery_view(self):
        if self.region.exists(slideshow_left_arrows_button, default_wait_time):
            self.region.click(slideshow_left_arrows_button)
            return True
        return False, "Fail to find button '<--' in gallery view"

    def upload_video(self, item, name=''):
        if self.region.exists(item, default_wait_time):
            self.region.click(item)
        elif helper.check_exist_by_cliclick(name):
            helper.click_item_by_cliclick(name)
        else:
            return False, "Fail to select item before uploading it"
        return self.upload_via_bottom_bar()

    def upload_story(self):
        helper.assert_step(self.play_video(suggested_story_icon))
        helper.assert_step(self.wait_till_start_playing(2 * 60))
        self.make_overlay_display()
        self.region.click(story_save_button)
        time.sleep(1)
        type('up')
        time.sleep(1)
        type(Key.ENTER)

    def upload_via_bottom_bar(self):
        if self.region.exists(plus_button, default_wait_time):
            self.region.click(plus_button)
            time.sleep(2)
            type('up')
            time.sleep(2)
            type(Key.ENTER)
            return True
        return False, "Fail to find 'Upload' menu item"

    def download_video(self, item, name=''):
        if self.region.exists(item, default_wait_time):
            self.region.click(item)
        elif helper.check_exist_by_cliclick(name):
            helper.click_item_by_cliclick(name)
        else:
            return False, "Fail to select item before downloading it"
        return self.download_via_bottom_bar()

    def download_via_bottom_bar(self):
        if self.region.exists(plus_button, default_wait_time):
            self.region.click(plus_button)
            time.sleep(2)
            type('do')
            time.sleep(2)
            type(Key.ENTER)
            return True
        return False, "Fail to find 'Download' menu item"

    def view_photo(self, item, name=''):
        if self.region.exists(item, default_wait_time):
            self.region.doubleClick(item)
        elif helper.check_exist_by_cliclick(name):
            helper.double_click_item_by_cliclick(name)
        else:
            return False, 'Fail to find photo in library view'
        return True

    def edit_caption(self, item, name, old_caption_screenshot, new_caption):
        if self.region.exists(item, default_wait_time):
            self.region.click(item)
        elif helper.check_exist_by_cliclick(name):
            helper.click_item_by_cliclick(name)
        else:
            return False, 'Fail to find test clip for rename testing'
        time.sleep(1)
        self.region.click(old_caption_screenshot)
        time.sleep(2)
        type(new_caption)
        type(Key.ENTER)
        return True

    def make_overlay_display(self):
        # the following movement is to make overlay button show up
        size = self._get_size_of_window()
        position = self._get_position_of_window()
        if len(size) != 2 or len(position) != 2:
            return False, "Fail to get size and position of player window"
        for i in range(2):
            self.region.hover(Location(position[0], position[1]))
            self.region.hover(Location(position[0], position[1] + size[1]))

    def _get_size_of_window(self):
        return self._parse_ret(helper.run_apple_script("get_size_of_player.applescript"))

    def _get_position_of_window(self):
        return self._parse_ret(helper.run_apple_script("get_position_of_player.applescript"))

    def _parse_ret(self, ret):
        ret = ret.replace('{', '').replace('}', '')
        return [int(i) for i in ret.split(',')]

    def get_value_of_progress_bar(self):
        ret = 0.0
        try:
            ret = float(
                helper.run_apple_script("get_value_process_bar_play_gallery_view.applescript").rstrip("\n"))
        except:
            pass
        return ret

    def is_playing(self):
        return self.get_value_of_progress_bar() > 0

    def wait_till_start_playing(self, timeout=30):
        start = time.time()
        while not self.is_playing():
            if (time.time() - start) > timeout:
                return False, "Timeout for waiting to start playing in gallery view"
            time.sleep(2)
        return True

    def verify_rt_is_playing_video(self):
        self.make_overlay_display()
        if not self.region.exists(pause_button, default_wait_long_time):
            return False, "'Pause' button should be shown"
        self.make_overlay_display()
        if not self.region.exists(play_in_separate_window_button, default_wait_time):
            return False, "'Play in separate window' button should be shown"
        return True

    def is_in_gallery_view(self):
        self.make_overlay_display()
        return self.region.exists(play_in_separate_window_button, default_wait_time)

    def exit_gallery_view(self):
        self.make_overlay_display()
        self.region.click(exit_gallery_button)

    def verify_in_gallery_view(self, item):
        self.make_overlay_display()
        if not self.region.exists(item, default_wait_time):
            return False, "Item wasn't shown in gallery view"
        return True

    def rename_in_gallery_view(self, item, new_name, new_name_screenshot, retry=5):
        while not self.region.exists(new_name_screenshot, default_wait_time):
            self.make_overlay_display()
            self.region.doubleClick(item)
            time.sleep(2)
            type(new_name)
            type(Key.ENTER)
            self.make_overlay_display()
            retry -= 1
            if retry == 0:
                return False, 'Fail to find rename caption from UI!!'
        else:
            return True

    def switch_to_all_view(self):
        if self.region.exists(content_location_switcher_all_selected, default_wait_time):
            self.region.click(content_location_switcher_all_selected)
            return True
        return False, "Fail to switch to 'All' view"

    def switch_to_mymac_view(self):
        if self.region.exists(content_location_switcher_mymac_selected, default_wait_time):
            self.region.click(content_location_switcher_mymac_selected)
            return True
        return False, "Fail to switch to 'MyMac' view"

    def switch_to_cloud_view(self):
        if self.region.exists(content_location_switcher_cloud_selected, default_wait_time):
            self.region.click(content_location_switcher_cloud_selected)
            return True
        return False, "Fail to switch to 'RealCloud' view"

    def switch_to_albums_view(self):
        if self.region.exists(my_albums_button_selected, default_wait_time):
            self.region.click(my_albums_button_selected)
            return True
        return False, "Fail to switch to 'Albums' view"

    def switch_to_share_view(self):
        if self.region.exists(sharing_button_selected, default_wait_time):
            self.region.click(sharing_button_selected)
            return True
        return False, "Fail to switch to 'Sharing' view"

    def switch_to_shared_by_me_view(self):
        helper.assert_step(self.switch_to_share_view())
        if self.region.exists(share_everyone_item):
            self.region.click(share_everyone_item)
            self.region.click(share_by_me_dropdown_list_item)
            return True
        return False, "The 'Share By Me' button is not clicked"

    def switch_to_shared_with_me_view(self):
        return self.switch_to_share_view()

    def switch_to_recent_activity_view(self):
        if self.region.exists(recent_activity_selected, default_wait_time):
            self.region.click(recent_activity_selected)
            return True
        return False, "Fail to find 'Recent' button"

    def switch_to_recent_activity_all_view(self):
        self.switch_to_recent_activity_view()
        return self.switch_to_all_view()

    def switch_to_recent_activity_watched_view(self):
        self.switch_to_recent_activity_view()
        if self.region.exists(content_location_switcher_watched_selected, default_wait_time):
            self.region.click(content_location_switcher_watched_selected)
            return True
        return False, "Fail to switch to 'Recent Activity -> Watched' view"

    def switch_to_recent_activity_uploaded_view(self):
        self.switch_to_recent_activity_view()
        if self.region.exists(content_location_switcher_uploaded_selected, default_wait_time):
            self.region.click(content_location_switcher_uploaded_selected)
            return True
        return False, "Fail to switch to 'Recent Activity -> Uploaded' view"

    def switch_to_stories_view(self):
        if self.region.exists(stories_button_selected, default_wait_time):
            self.region.click(stories_button_selected)
            return True
        return False, "Fail to switch to 'Stories' view"

    def switch_to_stories_suggested_view(self):
        self.switch_to_stories_view()
        if self.region.exists(content_location_switcher_stories_suggested_selected, default_wait_time):
            self.region.click(content_location_switcher_stories_suggested_selected)
            return True
        return False, "Fail to switch to 'Stories -> Suggested' view"

    def switch_to_stories_saved_view(self):
        self.switch_to_stories_view()
        if self.region.exists(content_location_switcher_stories_saved_selected, default_wait_time):
            self.region.click(content_location_switcher_stories_saved_selected)
            return True
        return False, "Fail to switch to 'Stories -> Saved' view"

    def switch_to_stories_cloud_view(self):
        self.switch_to_stories_view()
        if self.region.exists(content_location_switcher_stories_cloud_selected, default_wait_time):
            self.region.click(content_location_switcher_stories_cloud_selected)
            return True
        return False, "Fail to switch to 'Stories -> Cloud' view"

    def add_to_my_library(self, content_folder_path):
        """ add contents in 'content_folder_path' to 'My Mac' """

        # switch to 'My Mac'
        helper.retry(self.switch_to_mymac_view)

        # use shortcut "CMD + L" to open file dialog
        type("l", Key.CMD)
        time.sleep(2)

        # change view to 'as icon'
        type("1", Key.CMD)
        time.sleep(2)

        # go to content_folder_path
        type("g", Key.CMD + Key.SHIFT)
        time.sleep(2)
        type(content_folder_path)

        # click 'Go' button
        time.sleep(2)
        type(Key.ENTER)

        # click 'Open' button
        time.sleep(2)
        type(Key.ENTER)

        return True

    def remove_all_from_mymac_view(self):
        """ remove all items from ''My Mac' view """

        # switch to 'My Mac'
        helper.log("switch to 'My Mac'")
        helper.retry(self.switch_to_mymac_view)
        time.sleep(2)
        # remove all from current view
        return self.remove_all()

    def remove_all_from_cloud_view(self):
        """ remove all items from 'Cloud' view """

        # switch to 'Cloud'
        helper.log("switch to 'Cloud'")
        helper.retry(self.switch_to_cloud_view)
        time.sleep(2)
        # remove all from current view
        return self.remove_all()

    def remove_all(self):
        retry = 5
        while not self.region.exists(no_photos_or_videos, default_wait_time):
            # select all
            self.region.click(select_current_view)
            type("a", Key.CMD)
            # click delete button
            type(Key.DELETE)
            # if current view contains cloud&local content, will select 'delete
            # from this mac' radio button
            if self.region.exists(delete_from_this_mac_radio_button, default_wait_time):
                self.region.click(delete_from_this_mac_radio_button)

            time.sleep(2)
            type(Key.ENTER)

            retry -= 1
            if retry < 0:
                break
        else:
            helper.log("No photos or videos, return")
        return True

    def open_transfers_dialog(self):
        if self.region.exists(transfers_button, default_wait_time):
            self.region.click(transfers_button)
            return
        if self.region.exists(transfers_button_in_progress, default_wait_time):
            self.region.click(transfers_button_in_progress)
            return

    def add_item_to_album(self, screenshot, name, item_in_album_view=test_album_item, album_name="new"):
        if self.region.exists(screenshot, default_wait_time):
            self.region.click(screenshot)
        else:
            helper.click_item_by_cliclick(name)
        helper.assert_step(self.add_to_album_via_bottom_bar())

        if album_name == 'new':
            self.region.wait(new_album_dialog_button)
            self.region.click(new_album_dialog_button)

            time.sleep(1)
            type("test")

            time.sleep(1)
            type(Key.ENTER)

            if not region.exists(album_item_dialog_icon, default_wait_time):
                type(Key.ESC)
                return False, "Failed to create new album"

            helper.log("Click album icon in dialog")
            self.region.click(album_item_dialog_icon)

            helper.log("Click 'Enter' to add item to album")
            time.sleep(1)
            type(Key.ENTER)
            helper.assert_step(self.switch_to_albums_view())
            if not self.does_exist_in_library(item_in_album_view, "test", default_wait_time):
                return False, "Failed to add item to the new created album"
        else:
            type(album_name)
            time.sleep(1)
            type(Key.ENTER)
            helper.assert_step(self.switch_to_albums_view())
        return True

    def add_to_album_via_bottom_bar(self):
        if self.region.exists(plus_button, default_wait_time):
            self.region.click(plus_button)
            time.sleep(2)
            type('ad')
            time.sleep(2)
            type(Key.ENTER)
            return True
        return False, "Fail to find 'Add to Album' menu item"

    def open_album(self, album_item, name=''):
        if self.region.exists(album_item, default_wait_time):
            self.region.doubleClick(album_item)
        elif helper.check_exist_by_cliclick(name):
            helper.click_item_by_cliclick(name)
        else:
            return False, "The specified album doesn't exist"
        return True

    def open_share_group(self, group_item):
        if not self.region.exists(group_item):
            return False, "The specified shared group doesn't exist"
        self.region.doubleClick(group_item)
        return True

    def like_album(self, album_item, name=''):
        """To like the specified album in the sharing folder"""

        helper.assert_step(self.switch_to_shared_with_me_view())
        if not self.open_album(album_item, name):
            return False, "Open album failed"
        if not self.region.exists(like_button):
            return False, "There is no like button or it is already liked"
        self.region.click(like_button)
        time.sleep(2)
        if not self.region.exists(unlike_button):
            return False, "You can't like the album, like operation is failed"
        return True

    def back_to_album(self):
        self.region.click(back_button)

    def unlike_album(self, album_item):
        """To unlike the specified album in the sharing folder"""
        helper.assert_step(self.switch_to_shared_with_me_view())
        if not self.open_album(album_item):
            return False, "Open album failed"
        if not self.region.exists(unlike_button):
            return False, "There is no unlike button or it is already unliked"
        self.region.click(unlike_button)
        time.sleep(2)
        if not self.region.exists(like_button):
            return False, "Unlike operation is failed"
        return True

    def rename_album_in_album_header(self, item, new_name, new_name_screenshot, retry=5):
        if not self.region.exists(item, default_wait_time):
            return False, "Cannot find album title"
        while not self.region.exists(new_name_screenshot, default_wait_time):
            self.region.click(item)
            time.sleep(1)
            type(new_name)
            type(Key.ENTER)
            retry -= 1
            if retry == 0:
                return False, 'Fail to find new name from UI!!'
        else:
            return True

    def like_media(self, media_item, name=''):
        """To like the specified media in the sharing folder"""
        helper.assert_step(self.switch_to_shared_with_me_view())
        self.play_video(media_item, name)
        time.sleep(5)

        if not self.region.exists(like_button):
            return False, "There is no like button or it is already liked"
        self.region.click(like_button)
        time.sleep(2)
        if not self.region.exists(unlike_button):
            return False, "You can't like the media, like operation is failed"
        if not self.region.exists(one_like_message):
            return False, "The like number is not correct"
        return True

    def unlike_media(self, media_item, name=''):
        """To like the specified media in the sharing folder"""
        helper.assert_step(self.switch_to_shared_with_me_view())
        self.play_video(media_item, name)
        time.sleep(5)

        if not self.region.exists(unlike_button):
            return False, "There is no unlike button or it is already unliked"
        self.region.click(unlike_button)
        time.sleep(2)
        if not self.region.exists(like_button):
            return False, "You can't unlike the media, unlike operation is failed"
        if self.region.exists(one_like_message):
            return False, "The like number is not correct"
        return True

    def share_media_in_library_view(self, name_list, share_to_account=account_username2):
        """
        Share a media item or multiple media items to another account.
        Currently we use default account_username to share
        """

        if self.region.exists(photos_and_videos_button_selected):
            self.region.click(photos_and_videos_button_selected)
        else:
            return False, "Fail to find 'Photos & Videos' button"

        # Select an album to share
        helper.log("The media item(s) will be shared")
        helper.multiple_select_by_cliclick(name_list)
        return self.share_media(share_to_account)

    def share_story(self, story_icon, share_account=account_username2, wait_time=default_wait_long_time):
        self.region.click(story_icon)
        helper.assert_step(self.share_via_bottom_bar())
        return self.share_dialog(share_account, wait_time)

    def share_media(self, share_account=account_username2):
        helper.assert_step(self.share_via_bottom_bar())
        return self.share_dialog(share_account)

    def share_via_bottom_bar(self):
        if self.region.exists(plus_button, default_wait_time):
            self.region.click(plus_button)
            time.sleep(2)
            type('sh')
            time.sleep(2)
            type(Key.ENTER)
            return True
        return False, "Fail to find 'Share' menu item"

    def share_group(self, share_to_account=account_username2):
        self.region.click(select_current_view)
        self.region.click(share_group_button)
        return self.share_dialog(share_to_account)

    def share_album(self, album_item, album_name='', share_to_account=account_username2):
        """ Share an album to another account, currently we use default account_username to share """

        helper.log("Switch to album")
        helper.retry(self.switch_to_albums_view)

        # Select an album to share
        helper.log("The created album will be shared")
        if self.region.exists(album_item, default_wait_long_time):
            self.region.click(album_item)
        elif helper.check_exist_by_cliclick(album_name):
            helper.click_item_by_cliclick(album_name)
        else:
            return False, "The album item doesn't exist"
        helper.assert_step(self.share_via_bottom_bar())
        time.sleep(20)
        return self.share_dialog(share_to_account)

    def share_dialog(self, share_to_account, wait_time=60*5):
        if not self.region.exists(enter_names_text_box, wait_time):
            return False, "Share dialog doesn't be poped up"

        self.region.click(enter_names_text_box)
        self.region.click(enter_names_text_box)
        time.sleep(5)
        type(share_to_account)
        time.sleep(1)
        self.region.click(write_something_text_box)
        self.region.click(write_something_text_box)
        type("share an item(s)")

        if not self.region.exists(share_button_of_share_dialog):
            return False, "The share button is not existed"
        self.region.click(share_button_of_share_dialog)

        if not self.region.exists(share_success_text, default_wait_time):
            return False, "The sharing is not successful"
        self.region.click(close_button_of_share_dialog)

        return True

    def close_gallery_view(self):
        os.system(
            "osascript " + os.path.join(applescript_path, "close_gallery_view.applescript"))

    def search_library(self, media_name):
        cmd = "osascript " + os.path.join(applescript_path, "search_library.applescript") + " " + media_name
        os.system(cmd)

    def does_exist_in_library(self, screenshot, name, wait_time):
        if self.region.exists(screenshot, wait_time):
            return True
        return helper.check_exist_by_cliclick(name)
