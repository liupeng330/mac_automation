import os
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


class TestCase_1799_Step1(TestCase_Base):

    """ Upload/Download: Upload Download video from Player window """
    """ Step1: Play a cloud video, Download it """

    def setUp(self):
        try:
            TestCase_Base.setUp(self)

            # test clip
            self.test_name = "Upload_transfer_1.mp4"
            self.test_case_path = os.path.join(
                test_content_path, "original", self.test_name)

            self.player = Player(region)

            # upload clip to cloud
            log("Start to upload media file to cloud")
            assert upload_video_via_API(
                self.test_case_path), "Fail to upload test clip '" + self.test_name + "' via API"

            op.launch_RT_before_running_case()
            assert_step(self.RT.remove_all_from_mymac_view())
        except:
            TestCase_Base.tearDown(self)
            raise

    @attr('BVT')
    def test_download_from_player_window(self):
        # verify signed in
        assert region.exists(
            has_signed_in_rt_top_bar, default_wait_time), "Fail to sign in to cloud via UI"

        log("Switch to cloud view")
        assert_step(self.RT.switch_to_cloud_view())

        # verify test clip is in the view
        log("Verify " + self.test_name + " test content has been uploaded")
        assert self.RT.does_exist_in_library(
            play_in_player_item, 'Upload_transfer_1', default_wait_time), \
            "Fail to find thumbnail of test clip '" + self.test_name + "' in cloud view"

        # play test clip
        log("Play it")
        assert_step(self.RT.play_video(play_in_player_item, 'Upload_transfer_1'))
        assert_step(self.RT.verify_rt_is_playing_video())

        log("Open player to play it")
        self.RT.play_in_seperate_window()

        log("Wait player start to play")
        assert_step(self.player.wait_till_start_playing())

        log("Maximize player window")
        self.player.maximize()

        log("Click download button")
        assert_step(self.player.download())

        # verify download complete
        log("Wait for download from cloud complete")
        assert wait_for_download_complete(self.test_name, 60 * 5), \
            "After waiting for 5 minutes, still cannot find test clip '" + self.test_name + "' in RealTimes' download folder"

        self.player.close()

        log("Switch tab to local library, to check if downloaded item exists")
        assert_step(self.RT.switch_to_mymac_view())
        assert self.RT.does_exist_in_library(
            play_in_player_item, 'Upload_transfer_1', default_wait_time), \
            "Fail to find thumbnail of test clip '" + self.test_name + "' in local library"

    def tearDown(self):
        TestCase_Base.tearDown(self)


class TestCase_1799_Step2(TestCase_Base):
    """ Upload/Download: Upload Download video from Player window """
    """ Step2: Play a local video, and upload it """

    def setUp(self):
        try:
            TestCase_Base.setUp(self)

            # prepare test content
            self.test_name = "Upload_transfer_1.mp4"
            self.test_case_path = prepare_content(
                "1799_step2", False, self.test_name)

            self.player = Player(region)

            op.launch_RT_before_running_case()
            assert_step(self.RT.remove_all_from_mymac_view())
        except:
            capture_screen(self.screenshot)
            raise

    @attr('BVT')
    def test_upload_from_player_window(self):
        # add test clip into local library
        log("Add test clip into local library")
        assert_step(self.RT.add_to_my_library(self.test_case_path))

        # play it
        log("Play it")
        assert_step(self.RT.play_video(play_in_player_item, 'Upload_transfer_1'))

        # verify test clip is played
        log("Verify test clip is played")
        assert_step(self.RT.verify_rt_is_playing_video())

        log("Open player to play it")
        self.RT.play_in_seperate_window()

        log("Wait player start to play")
        assert_step(self.player.wait_till_start_playing())

        log("Maximize player window")
        self.player.maximize()

        log("Click upload button")
        assert_step(self.player.upload())

        # verify upload by calling cloud API
        log("Wait for upload complete")
        assert wait_for_upload_complete(get_title_of_file(self.test_name), 10 * 60), "Fail to upload test clip '" + self.test_name + "' in 'Player' window"

    def tearDown(self):
        TestCase_Base.tearDown(self)
