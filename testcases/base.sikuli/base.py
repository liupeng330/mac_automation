import sys

import unittest

import helper
from sikuli import *
from global_config import *

from controls.sign_in_control import *
from controls.rt_control import *
from controls.system_tray_control import *

import ops.operations as op
import shutil
import time


class TestCase_Base(unittest.TestCase):

    def setUp(self):
        # launch rt for switch cloud env
        helper.log("TestCase_Base setUp starts.")
        helper.log("Current test is *** " + self._testMethodName + " ***")
        self.screenshot = self._testMethodName + "_" + helper.get_time_stamp() + ".png"

        try:
            helper.log("Cleanup diagnostic report files")
            helper.cleanup_diagnostic_report_folders()

            helper.log("region: %s" % region)
            self.RT = RT(region)
            self.RT.launch()

            # handle warning dialog
            helper.log("TestCase_Base setUp: %s" % "Handle warning dialog, only appear when first launch")
            op.first_launch_RT()

            helper.log("set cloud env to " + str(env))
            self.SysTray = SystemTray(top_menu_bar_region)
            self.SysTray.switch_cloud_env(env)
            time.sleep(5)
            helper.kill_RT()
            helper.kill_rpds()
            self.RT.launch()

            # clean up all content in cloud
            helper.log("Clean up all content in cloud.")
            assert helper.cleanup_cloud_content_via_API(
            ), "Fail to cleanup all test content via cloud API"

            # clean up download folder
            helper.log("Clean up 'Download' folder")
            helper.cleanup_cloud_download_folder()

            # upload init.mp4 for cloud
            helper.log("Upload 'init.mp4' to cloud")
            assert helper.upload_video_via_API(
                os.path.join(test_content_path, "original", "init.mp4")), \
                "Fail to upload 'init.mp4' to cloud"

        except Exception, ex:
            helper.log("TestCase_Base setUp failed with exception:")
            helper.log("Exception occur: %s" % ex.message)
            raise
        else:
            helper.log("TestCase_Base setUp ends successfully without exception occur.")

    def tearDown(self):
        helper.log("TestCase_Base tearDown starts.")
        if sys.exc_info()[0] is not None:
            helper.capture_screen(self.screenshot)
        helper.dismiss_crash_dialog()
        helper.fetch_diagnostic_report_files()
        if reset_realtimes:
            helper.log("Reset DB from 'Preferences' dialog")
            helper.reset_DB_from_preferences_dialog()
        helper.kill_RT()
        helper.cleanup_cloud_download_folder()
        helper.log("TestCase_Base tearDown ends.")
