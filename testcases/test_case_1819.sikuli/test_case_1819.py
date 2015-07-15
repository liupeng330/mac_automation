import os
from nose.plugins.attrib import attr
from helper import *
from sikuli import *
from global_config import *

from controls.sign_in_control import *
from controls.rt_control import *
from controls.system_tray_control import *

import ops.operations as op

from base import *


class TestCase_1819(TestCase_Base):

    """ Sharing: Share cloud media from library view and gallery view """

    def setUp(self):
        try:
            TestCase_Base.setUp(self)

            # test clip
            self.test_name = "Download.mp4"
            self.test_case_path = os.path.join(
                test_content_path, "original", self.test_name)

            # upload clip to cloud
            assert upload_video_via_API(
                self.test_case_path), "Fail to upload test clip '" + self.test_name + "' via API"

            log("Start to verify if RT is signed in or not")
            if self.RT.is_sign_in:
                log("RT has been signed in already, start to sign out")
                self.RT.sign_out()
            op.launch_RT_before_running_case()
        except:
            TestCase_Base.tearDown(self)
            raise

    @attr('BVT')
    def test_share_from_library_view(self):
        # verify signed in
        assert region.exists(
            has_signed_in_rt_top_bar, default_wait_time), "Fail to sign in to cloud via UI"

        # verify test clip is in the view
        log("Verify Download.mp4 test content has been uploaded")
        assert self.RT.does_exist_in_library(download_video_item, "Download", default_wait_time), \
            "Fail to find thumbnail of test clip '" + self.test_name + "'"

        assert_step(self.RT.share_media_in_library_view(["Download"]))
        op.switch_to_account2()
        assert_step(self.RT.switch_to_shared_with_me_view())

        # verify the shared item is in the view
        assert self.RT.does_exist_in_library(new_shared_media_item, "Download", default_wait_time), \
            "After sharing the test clip '" + self.test_name + "', fail to find it in 'Share with me' view"

    @attr('BVT')
    def test_share_from_gallery_view(self):
        # verify signed in
        assert region.exists(
            has_signed_in_rt_top_bar, default_wait_time), "Fail to sign in to cloud via UI"

        # verify test clip is in the view
        log("Verify Download.mp4 test content has been uploaded")
        assert self.RT.does_exist_in_library(download_video_item, "Download", default_wait_time), \
            "Fail to find thumbnail of test clip '" + self.test_name + "'"

        # play item
        log("Play video")
        assert_step(self.RT.play_video(download_video_item, 'Download'))

        log("Wait it to play")
        self.RT.wait_till_start_playing()

        # share it
        log("Share it from gallery view")
        assert_step(self.RT.share_media())

        # switch to another account, and check it
        op.switch_to_account2()
        assert_step(self.RT.switch_to_shared_with_me_view())

        # verify the shared item is in the view
        assert self.RT.does_exist_in_library(new_shared_media_item, "Download", default_wait_time), \
            "After sharing the test clip '" + self.test_name + "', fail to find it in 'Share with me' view"

    def tearDown(self):
        TestCase_Base.tearDown(self)
