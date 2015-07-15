from nose.plugins.attrib import attr
from helper import *
from sikuli import *
from global_config import *

from controls.sign_in_control import *
from controls.rt_control import *
from controls.system_tray_control import *
from controls.player_control import *

import ops.operations as op

import time
import unittest

from base import *


@unittest.skip("No slideshow feature")
class TestCase_1826(TestCase_Base):

    """ Playback: Slideshow test """

    def _check_items_exists(self):
        # verify test clips are all in the view
        log("Verify test clip is in the view")
        for i in range(len(story_play_items)):
            assert region.exists(story_play_items[i], default_wait_time), "Fail to find screenshot of number " + str(i + 1) + "in library view"

    def setUp(self):
        try:
            TestCase_Base.setUp(self)

            self.test_files = ["Playback_1_1.mp4", "Playback_2_1.mp4", "Playback_3_1.mp4"]

            # test clip
            self.test_case_path = prepare_content(
                "1826", False, *self.test_files)

            op.launch_RT_before_running_case()
            assert_step(self.RT.remove_all_from_mymac_view())
        except:
            TestCase_Base.tearDown(self)
            raise

    @attr('BVT')
    def test_play_media_with_gallery_view_and_select_slideshow(self):
        log("Go to local library view")
        assert_step(self.RT.switch_to_mymac_view())

        log("Add test clips into local library")
        assert_step(self.RT.add_to_my_library(self.test_case_path))

        self._check_items_exists()
        log("Play num 1 item")
        assert_step(self.RT.play_video(story_play_items[0]))

        log("Select the first item in gallery view")
        for i in range(len(slideshow_play_items)):
            assert_step(self.RT.click_left_arrows_button_in_gallery_view())
            time.sleep(0.5)

        log("Click 'play with slideshow' button")
        self.RT.play_with_slideshow()

        log("Start to verify playback with slideshow")
        self._verify_playback()

    @attr('BVT')
    def test_play_slideshow_with_album(self):
        log("Go to cloud view")
        assert_step(self.RT.switch_to_cloud_view())

        # upload test files to cloud
        log("Upload test content to cloud")
        upload_video_files_via_API(*self.test_files)
        self._check_items_exists()

        # add items into album
        log("Add test content to album")
        assert_step(self.RT.add_item_to_album(story_play_items, item_in_album_view=slideshow_album_item))

        log("Play an album with slideshow, via right click menu item")
        self.RT.play_with_slideshow_for_album(slideshow_album_item)

        log("Start to verify playback with slideshow")
        self._verify_playback()

    def _verify_playback(self):
        play_verify = VerifyPlay(60*2, *slideshow_play_items)
        play_verify.start()
        play_verify.wait()
        assert_step(play_verify.verify_result())

    def tearDown(self):
        TestCase_Base.tearDown(self)
