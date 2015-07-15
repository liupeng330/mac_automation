from nose.plugins.attrib import attr
from helper import *
from sikuli import *
from global_config import *

from controls.sign_in_control import *
from controls.rt_control import *
from controls.system_tray_control import *

import ops.operations as op

from base import *


class TestCase_1793(TestCase_Base):

    """ Upload/Download: Drag & Drop to upload a folder contains videos or photos onto the Library window """

    def setUp(self):
        try:
            TestCase_Base.setUp(self)

            # test clip
            self.test_name_video = "Upload.AVI"
            self.test_name_photo = "upload_photo.jpg"
            self.test_case_path = prepare_content(
                "1793", True, self.test_name_video, self.test_name_photo)

            op.launch_RT_before_running_case()
            assert_step(self.RT.remove_all_from_mymac_view())
        except:
            TestCase_Base.tearDown(self)
            raise

    @attr('BVT')
    def test_upload_drag_to_library(self):
        log("Drap drop a folder to RT")
        op.drag_drop_folder_to_rt(self.test_case_path)
        self._verify_upload()

    @attr('BVT')
    def test_upload_drag_to_transfer_dialog(self):
        log("Put transfers dialog to left side of screen")
        op.put_transfers_dialog_to_left_side_of_screen()

        log("Drap drop a folder to transfers dialog")
        op.drag_drop_folder_to_transfers_dialog(self.test_case_path)

        self._verify_upload()

    @attr('BVT')
    def test_upload_drag_to_system_tray(self):
        log("Drap drop a folder to transfers dialog")
        op.drag_drop_folder_to_system_tray(self.test_case_path)
        self._verify_upload()

    def _verify_upload(self):
        log("Wait upload compelte for a photo")
        assert wait_for_upload_complete(
            get_title_of_file(self.test_name_photo))

        log("Wait upload compelte for a video")
        assert wait_for_upload_complete(
            get_title_of_file(self.test_name_video))

    def tearDown(self):
        TestCase_Base.tearDown(self)
