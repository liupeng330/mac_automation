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


class TestCase_1814(TestCase_Base):

    """ Sharing: Share an album """

    def setUp(self):
        try:
            TestCase_Base.setUp(self)

            # test clip
            self.test_name = "Download.mp4"
            self.test_case_path = os.path.join(
                test_content_path, "original", self.test_name)
            self.test_album = "TestAlbum"

            # upload clip to cloud
            assert upload_video_via_API(
                self.test_case_path), "Fail to upload test clip '" + self.test_name + "' via API"

            # create an album
            assert create_collection_via_API(self.test_album), "Fail to create album '" + self.test_album + "'' via API"

            # add medias into album
            assert add_to_collection(self.test_album, get_title_of_file(self.test_name)), "Fail to add media files into album '" + self.test_album + "' via API"

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
        # Share an album
        assert_step(self.RT.share_album(download_video_item, 'TestAlbum'))

        # Switch to another account
        op.switch_to_account2()

        # Verify the shared item is in the view
        assert_step(self.RT.switch_to_shared_with_me_view())
        assert self.RT.does_exist_in_library(shared_album_item, "TestAlbum", default_wait_time), \
            "Fail to find the shared album '" + self.test_album + "' in 'Share with me' view"

    def tearDown(self):
        TestCase_Base.tearDown(self)
