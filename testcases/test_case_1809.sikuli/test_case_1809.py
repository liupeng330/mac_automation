import time
from nose.plugins.attrib import attr
from helper import *
from sikuli import *
from global_config import *

from controls.sign_in_control import *
from controls.rt_control import *
from controls.system_tray_control import *

import ops.operations as op

from base import *


class TestCase_1809(TestCase_Base):

    """ Upload/Download: Upload local video and photo from gallery view """

    def setUp(self):
        try:
            TestCase_Base.setUp(self)

            # test clip
            self.test_name_video = "Upload.AVI"
            self.test_name_photo = "upload_photo.jpg"
            self.test_case_path = prepare_content(
                "1809", False, self.test_name_video, self.test_name_photo)

            op.launch_RT_before_running_case()
            assert_step(self.RT.remove_all_from_mymac_view())
        except:
            TestCase_Base.tearDown(self)
            raise

    @attr('BVT')
    def test_upload_local_video_photo_from_gallery_view(self):
        # add test clip into local library
        log("Add test clip into local library")
        assert_step(self.RT.add_to_my_library(self.test_case_path))

        # play it to enter gallery view
        log("Play it to enter gallery view")
        assert_step(self.RT.play_video(upload_video_item, 'Upload'))

        # verify test clip is played
        log("Verify test clip is played")
        self.RT.verify_rt_is_playing_video()

        # upload it via gallery view
        log("Upload it via gallery view")
        self.RT.upload_via_bottom_bar()

        # verify upload by calling cloud API
        log("Verify upload by calling cloud API")
        assert wait_for_upload_complete(
            get_title_of_file(self.test_name_video)), "Fail to find test clip '" + self.test_name_video + "' via API, after uploading it from gallery view"

        log("Exit gallery view")
        self.RT.exit_gallery_view()

        # switch to photo in gallery view
        log("Switch to photo in gallery view")
        time.sleep(2)
        assert_step(self.RT.view_photo(upload_photo_item, 'upload_photo'))
        assert_step(self.RT.verify_in_gallery_view(upload_photo_item_in_gallery_view))

        # upload it via gallery view
        log("Upload it via gallery view")
        self.RT.upload_via_bottom_bar()

        # verify upload by calling cloud API
        log("Verify upload by calling cloud API")
        assert wait_for_upload_complete(
            get_title_of_file(self.test_name_photo)), "Fail to find test clip '" + self.test_name_photo + "' via API, after uploading it from gallery view"

    def tearDown(self):
        TestCase_Base.tearDown(self)
