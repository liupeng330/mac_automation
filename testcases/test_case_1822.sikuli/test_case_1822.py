import os
from nose.plugins.attrib import attr
import time

import helper
from sikuli import *
from global_config import *

from controls.sign_in_control import *
from controls.rt_control import *
from controls.system_tray_control import *

import ops.operations as op

from base import *


class TestCase_1822(TestCase_Base):

    """ Social Info: Like or unlike media in Shared with me """

    def setUp(self):
        try:
            TestCase_Base.setUp(self)

            log("Start to verify if RT is signed in or not")
            if self.RT.is_sign_in:
                log("RT has been signed in already, start to sign out")
                self.RT.sign_out()

            op.launch_RT_before_running_case()
            self.RT.remove_all_from_cloud_view()

            # test clip
            test_name = "Download.mp4"
            test_case_path = os.path.join(
                test_content_path, "original", test_name)
            assert os.path.isfile(test_case_path), "The media file doesn't exist in '" + test_case_path + "'"

            # upload clip to cloud
            assert helper.upload_video_via_API(
                test_case_path), "Fail to upload test clip '" + self.test_name + "' via API"
            assert_step(self.RT.switch_to_all_view())

            # share the clip to account_username2
            assert_step(self.RT.share_media_in_library_view(["Download"]))

            op.switch_to_account2()
            log("after sign in")
        except:
            TestCase_Base.tearDown(self)
            raise

    @attr('BVT')
    def test_like_unlike_media(self):
        assert_step(self.RT.switch_to_shared_with_me_view())

        # verify the shared item is in the view
        assert self.RT.does_exist_in_library(new_shared_media_item, "Download", default_wait_time), \
            "The shared item doesn't exist in 'Share with me' view"

        # like the shared album
        log("Like a shared media")
        assert_step(self.RT.like_media(new_shared_media_item))

        # exit the gallery mode
        log("Cloud gallery view")
        self.RT.close_gallery_view()
        time.sleep(2)

        # unlike the same album
        log("Unlike the shared media")
        assert_step(self.RT.unlike_media(shared_media_item))

    def tearDown(self):
        TestCase_Base.tearDown(self)
