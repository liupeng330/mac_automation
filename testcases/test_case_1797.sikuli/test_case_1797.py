from nose.plugins.attrib import attr
from helper import *
from sikuli import *
from global_config import *

from controls.sign_in_control import *
from controls.rt_control import *
from controls.system_tray_control import *

import ops.operations as op

from base import *


class TestCase_1797(TestCase_Base):

    """ Sharing: A share multi videos and photos to B """

    def _check_items_exists(self):
        # verify test clips are all in the view
        log("Verify test clip is in the view")
        assert self.RT.does_exist_in_library(
            share_video_item1, 'share_video_1', default_wait_time), "Fail to find thumbnail of test clip 'share_video_1.mp4' in cloud view"
        assert self.RT.does_exist_in_library(
            share_video_item2, 'share_video_2', default_wait_time), "Fail to find thumbnail of test clip 'share_video_2.mp4' in cloud view"
        assert self.RT.does_exist_in_library(
            share_photo_item1, 'share_photo_1', default_wait_time), "Fail to find thumbnail of test clip 'share_photo_1.jpg' in cloud view"
        assert self.RT.does_exist_in_library(
            share_photo_item2, 'share_photo_2', default_wait_time), "Fail to find thumbnail of test clip 'share_photo_2.jpg' in cloud view"

    def setUp(self):
        try:
            TestCase_Base.setUp(self)

            # test clip
            self.test_files = ["share_video_1.mp4", "share_video_2.mp4", "share_photo_1.jpg", "share_photo_2.jpg"]

            # upload test files to cloud
            upload_video_files_via_API(*self.test_files[0:2])
            upload_photo_files_via_API(*self.test_files[2:])

            log("Start to verify if RT is signed in or not")
            if self.RT.is_sign_in:
                log("RT has been signed in already, start to sign out")
                self.RT.sign_out()
            op.launch_RT_before_running_case()
        except:
            TestCase_Base.tearDown(self)
            raise

    @attr('BVT')
    def test_share_multi_videos_and_photos(self):
        # switch to cloud view
        assert_step(self.RT.switch_to_cloud_view())

        # verify upload
        self._check_items_exists()

        # share multi video and photos
        assert_step(self.RT.share_media_in_library_view(["share_video_1", "share_video_2", "share_photo_1", "share_photo_2"]))

        # switch to another account
        op.switch_to_account2()

        # verify the shared item is in the view
        assert_step(self.RT.switch_to_shared_with_me_view())
        assert_step(self.RT.open_share_group(share_group_item))
        self._check_items_exists()

    def tearDown(self):
        TestCase_Base.tearDown(self)
