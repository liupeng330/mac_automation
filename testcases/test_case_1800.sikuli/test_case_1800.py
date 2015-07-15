from nose.plugins.attrib import attr
from helper import *
from sikuli import *
from global_config import *

from controls.sign_in_control import *
from controls.rt_control import *
from controls.system_tray_control import *

import ops.operations as op

from base import *


class TestCase_1800(TestCase_Base):

    """ Upload/Download: Drag and Drop a video or photo onto the Library window/TQ/Systray """

    def setUp(self):
        try:
            TestCase_Base.setUp(self)

            # test clip
            self.test_name_video = "Upload.AVI"
            self.test_name_photo = "upload_photo.jpg"
            self.test_case_path = prepare_content(
                "1800", False, self.test_name_video, self.test_name_photo)

            op.launch_RT_before_running_case()
            assert_step(self.RT.remove_all_from_mymac_view())
        except:
            TestCase_Base.tearDown(self)
            raise

    @attr('BVT')
    def test_upload_drag_to_library(self):
        log("Navigate to test content path")
        put_finder_to_right_side_of_screen(self.test_case_path)

        log("Drag drop clips to library view")
        op.drag_drop_clips_to_library(
            self.test_case_path, upload_photo_item_in_finder_icon_view, upload_video_item_in_finder_icon_view)

        self._verify_upload()

    @attr('BVT')
    def test_upload_drag_to_TQ(self):
        log("Put transfer dialog to left side of screen")
        op.put_transfers_dialog_to_left_side_of_screen()

        log("Drag drop clips to transfers dialog")
        op.drag_drop_clips_to_transfers_dialog(
            self.test_case_path, upload_photo_item_in_finder_icon_view, upload_video_item_in_finder_icon_view)

        self._verify_upload()

    @attr('BVT')
    def test_upload_drag_to_systemTray(self):
        log("Put transfer dialog to left side of screen")
        op.put_transfers_dialog_to_left_side_of_screen()

        log("Drag drop clips to system tray")
        op.drag_drop_clips_to_system_tray(
            self.test_case_path, upload_photo_item_in_finder_icon_view, upload_video_item_in_finder_icon_view)

        self._verify_upload()

    def _verify_upload(self):
        log("Wait it upload complete")
        assert wait_for_upload_complete(
            get_title_of_file(self.test_name_photo)), "Fail to find uploaded test clip '" + self.test_name_photo + "' from cloud side via API"

        log("Wait it upload compelte")
        assert wait_for_upload_complete(
            get_title_of_file(self.test_name_video)), "Fail to find uploaded test clip '" + self.test_name_video + "' from cloud side via API"

    def tearDown(self):
        TestCase_Base.tearDown(self)
