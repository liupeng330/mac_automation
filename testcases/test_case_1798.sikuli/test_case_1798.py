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


class TestCase_1798(TestCase_Base):

    """ Sharing: A share a photo to B """

    def setUp(self):
        try:
            TestCase_Base.setUp(self)

            # test clip
            self.test_name = "share_photo_1.jpg"
            self.test_case_path = os.path.join(
                test_content_path, "original", self.test_name)

            # upload clip to cloud
            assert upload_photo_via_API(
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
    def test_share_photo_from_library_view(self):
        # verify signed in
        assert region.exists(
            has_signed_in_rt_top_bar, default_wait_time), "Fail to sign in to cloud from UI"

        # verify test clip is in the view
        log("Verify share_photo_1.jpg has been uploaded")
        assert region.exists(
            share_photo_item1, default_wait_time), "Fail to find thumbnail of test clip 'share_photo_1.jpg' from current view"

        assert_step(self.RT.share_media_in_library_view(["share_photo_1"]))
        op.switch_to_account2()
        assert_step(self.RT.switch_to_shared_with_me_view())

        #verify the shared item is in the view
        assert region.exists(share_photo_item1, default_wait_time), "Fail to find thumbnail of shared clip 'share_photo_1.jpg' in the 'share with me' view"

    def tearDown(self):
        TestCase_Base.tearDown(self)
