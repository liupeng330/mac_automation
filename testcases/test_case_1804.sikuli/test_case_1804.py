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
import unittest


class TestCase_1804(TestCase_Base):

    """ Notification: Network disconnected notification pop up for offline mode or error """

    def setUp(self):
        try:
            TestCase_Base.setUp(self)
            log("launch RT")    
            op.launch_RT_before_running_case()
            # test clip
            test_name = "Download.mp4"
            test_case_path = os.path.join(
                test_content_path, "original", test_name)
            assert os.path.isfile(test_case_path), "Fail to find media file '" + test_case_path + "'"

            # upload clip to cloud
            assert helper.upload_video_via_API(
                test_case_path), "Fail to upload test clip '" + self.test_name + "' via API"

            time.sleep(2)

            # go to cloud tab
            assert_step(self.RT.switch_to_cloud_view())

            assert self.RT.does_exist_in_library(
                download_video_item, 'Download', default_wait_time), \
                "Fail to find test clip '" + download_video_item + "' in cloud view"
        except:
            TestCase_Base.tearDown(self)
            raise

    @unittest.skip('TODO: How to test when connecting with cable, not WIFI')
    @attr('BVT')
    def test_network_disconnect_notification(self):
        log("turn off wifi")
        assert helper.turn_off_wifi(), "Failed to turn off wifi"

        time.sleep(2)
        # verify the no network notification is showed up in the cloud tab
        assert region.exists(
            no_network_notification, default_wait_long_time), \
            "'No network' notification doesn't show up after turning WIFI off"

        log("turn on wifi")
        assert helper.turn_on_wifi(), "Fail to turn WIFI on via command 'networksetup -setairportpower en0 on'"
        time.sleep(2)

        assert self.RT.does_exist_in_library(
            download_video_item, 'Download', default_wait_long_time), \
            "After reconnecting WIFI, the item in library view can't be shown up again"

    def tearDown(self):
        TestCase_Base.tearDown(self)
