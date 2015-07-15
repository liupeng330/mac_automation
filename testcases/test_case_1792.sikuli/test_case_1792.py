import time
from nose.plugins.attrib import attr
from helper import *
from sikuli import *
from global_config import *

from controls.sign_in_control import *
from controls.rt_control import *
from controls.system_tray_control import *
from controls.transfers_control import *

import ops.operations as op

from base import *


class TestCase_1792(TestCase_Base):

    """ Upload/Download: Can cancel the transferring files """

    def setUp(self):
        try:
            TestCase_Base.setUp(self)

            # test clip
            self.test_name_video1 = "Upload_transfer_1.mp4"
            self.test_name_video2 = "Upload_transfer_2.mp4"
            self.test_case_path = prepare_content(
                "1792", True, self.test_name_video1, self.test_name_video2)

            op.launch_RT_before_running_case()
            assert_step(self.RT.remove_all_from_mymac_view())
        except:
            TestCase_Base.tearDown(self)
            raise

    @attr('BVT')
    def test_upload_can_cancel_transferring_files(self):
        try:
            log("Clear all items in transfers dialog")
            op.clear_all_items_in_transfers_dialog()

            log("Drap drop a folder to RT")
            op.drag_drop_folder_to_rt(self.test_case_path)

            # let run uploading a while
            time.sleep(10)

            log("Stop all items in transfers dialog")
            op.stop_all_items_in_transfers_dialog()

            log("Verify items are NOT uploaded to cloud")
            assert not wait_for_upload_complete(
                get_title_of_file(self.test_name_video1), 60), "After pausing the uploading process in transfers dialog, test file '" + self.test_name_video1 + "' can still be uploaded to cloud"
            assert not wait_for_upload_complete(
                get_title_of_file(self.test_name_video2), 60), "After pausing the uploading process in transfers dialog, test file '" + self.test_name_video2 + "' can still be uploaded to cloud"
        except:
            raise
        finally:
            op.clear_all_items_in_transfers_dialog()

    def tearDown(self):
        TestCase_Base.tearDown(self)
