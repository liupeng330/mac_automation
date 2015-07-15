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


class TestCase_1794(TestCase_Base):

    """ Upload/Download: Global pause and resume work for transferring items """

    def setUp(self):
        try:
            TestCase_Base.setUp(self)

            # test clip
            self.test_name_video1 = "Upload_transfer_1.mp4"
            self.test_name_video2 = "Upload_transfer_2.mp4"
            self.test_case_path = prepare_content(
                "1794", True, self.test_name_video1, self.test_name_video2)

            op.launch_RT_before_running_case()
            assert_step(self.RT.remove_all_from_mymac_view())
            assert_step(self.RT.switch_to_cloud_view())
        except:
            TestCase_Base.tearDown(self)
            raise

    @attr('BVT')
    def test_upload_global_pause_resume_for_transferring_items(self):
        log("Clear all items in transfers dialog")
        op.clear_all_items_in_transfers_dialog()

        log("Drap drop a folder to RT")
        op.drag_drop_folder_to_rt(self.test_case_path)

        # let run uploading a while
        time.sleep(10)

        log("Stop all items in transfers dialog, and resume them again")
        op.stop_and_resume_items_in_systray()

        self.RT.open_transfers_dialog()

        log("Verify items are uploaded to cloud")
        assert wait_for_upload_complete(
            get_title_of_file(self.test_name_video1), 60 * 10), "After pausing and resuming the uploading process in transfers dialog, test file '" + self.test_name_video1 + "' fail to upload to cloud"
        assert wait_for_upload_complete(
            get_title_of_file(self.test_name_video2), 60 * 10), "After pausing and resuming the uploading process in transfers dialog, test file '" + self.test_name_video2 + "' fail to upload to cloud"

    def tearDown(self):
        TestCase_Base.tearDown(self)
