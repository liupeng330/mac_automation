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


class TestCase_1823(TestCase_Base):

    """ Social Info: Check social info for media or album in items I've shared """

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
            self.test_name = "Download.mp4"
            self.test_case_path = os.path.join(
                test_content_path, "original", self.test_name)
            assert os.path.isfile(
                self.test_case_path), "The media file doesn't exist in '" + self.test_case_path + "'"

            # upload clip to cloud
            assert helper.upload_video_via_API(
                self.test_case_path), "Fail to upload test clip '" + self.test_name + "' via API"
            assert_step(self.RT.switch_to_all_view())

            # share the clip to account_username2
            assert_step(self.RT.share_media_in_library_view(["Download"]))

            op.switch_to_account()
            log("after sign in")
        except:
            TestCase_Base.tearDown(self)
            raise

    @attr('BVT')
    def test_social_info(self):
        assert_step(self.RT.switch_to_shared_with_me_view())

        # verify the shared item is in the view
        assert self.RT.does_exist_in_library(new_shared_media_item, "Download", default_wait_time), \
            "The shared media item doesn't exist in 'Share with me' view"

        # like the shared item
        assert_step(self.RT.like_media(new_shared_media_item, "Download"))

        # switch to account again
        op.switch_to_account(account_username, account_password)
        log("Swith to mac_auto")

        # go to share by me view
        self.RT.switch_to_shared_by_me_view()

        # play the item to enter gallery view mode
        assert_step(self.RT.play_video(shared_media_item, "Download"))

        # check if the like number is correct or not
        assert region.exists(one_like_message), "Fail to find the like number in gallery view"

    def tearDown(self):
        TestCase_Base.tearDown(self)
