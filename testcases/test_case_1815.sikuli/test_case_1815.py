from nose.plugins.attrib import attr
from helper import *
from sikuli import *
from global_config import *

from controls.sign_in_control import *
from controls.rt_control import *
from controls.system_tray_control import *

import ops.operations as op

from base import *


class TestCase_1815(TestCase_Base):

    """ Recent Activity: Event generation """

    def _check_items_exists(self):
        # verify test clips are all in the view
        log("Verify test clip is in the view")
        assert self.RT.does_exist_in_library(
            share_video_item1, "share_video_1", default_wait_time), "Fail to find thumbnail of test clip 'share_video_1.mp4' in current view"
        assert self.RT.does_exist_in_library(
            share_video_item2, "share_video_2", default_wait_time), "Fail to find thumbnail of test clip 'share_video_2.mp4' in current view"

    def setUp(self):
        try:
            TestCase_Base.setUp(self)

            # test clip
            self.test_files = ["share_video_1.mp4", "share_video_2.mp4"]

            # upload test files to cloud
            upload_video_files_via_API(*self.test_files)

            log("Start to verify if RT is signed in or not")
            if self.RT.is_sign_in:
                log("RT has been signed in already, start to sign out")
                self.RT.sign_out()
            op.launch_RT_before_running_case()
        except:
            TestCase_Base.tearDown(self)
            raise

    @attr('BVT')
    def test_recent_activity_event(self):
        # switch to cloud view
        assert_step(self.RT.switch_to_cloud_view())

        # verify upload
        self._check_items_exists()

        # share group
        assert_step(self.RT.share_group())

        log("Switch to 'Recent Activity -> All' view")
        assert_step(self.RT.switch_to_recent_activity_all_view())

        assert self.RT.does_exist_in_library(download_video_item, "Download", default_wait_time), "Cannot find the thumbnail of share group item in 'recent activity -> All' view"
        assert_step(self.RT.open_share_group(download_video_item))
        self._check_items_exists()

    def tearDown(self):
        TestCase_Base.tearDown(self)
