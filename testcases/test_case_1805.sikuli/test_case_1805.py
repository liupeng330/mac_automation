import __builtin__
import os
import traceback

from nose.plugins.attrib import attr
from helper import *
from sikuli import *
from global_config import *

from controls.sign_in_control import *
from controls.rt_control import *
from controls.system_tray_control import *

import ops.operations as op

from base import *


def handler(event):
    log("Got notification")
    # stops the observation
    event.region.stopObserver()
    TestCase_1805.got_notification = True


class TestCase_1805(TestCase_Base):

    """ Verify Notification in RealTimes """

    got_notification = False

    def setUp(self):
        try:
            log("test_DownloadNotification: setUp start...")
            TestCase_Base.setUp(self)
            TestCase_1805.got_notification = False
            log("test_DownloadNotification: setUp end...")
        except:
            TestCase_Base.tearDown(self)
            raise

    @attr('BVT')
    def test_download_notification(self):
        log("test_DownloadNotification: Start...")
        try:
            log("test_DownloadNotification: upload a video via API")
            self.test_name = "Download.mp4"
            self.test_case_path = os.path.join(
                test_content_path, "original", self.test_name)
            assert upload_video_via_API(
                self.test_case_path), "Fail to upload test clip '" + self.test_case_path + "' via API"

            log("test_DownloadNotification: Start Sign in process.")
            op.launch_RT_before_running_case()
            log("test_DownloadNotification: Sign in successfully.")

            log("Verify the video have been uploaded.")
            assert self.RT.does_exist_in_library(
                download_video_item, 'Download', default_wait_time), \
                "Fail to find thumbnail of test clip '" + self.test_name + "' in library"

            log("Download the video.")
            time.sleep(5)
            assert_step(self.RT.download_video(download_video_item, 'Download'))

            log("Wait the Download complete notification appear.")
            if osx_version == "10.10":
                assert region.exists(download_complete_notification_10_10, default_wait_long_time), "'Download video complete' notification doesn't show up"
            elif osx_version == "10.9":
                assert region.exists(download_complete_notification_10_9, default_wait_long_time), "'Download video complete' notification doesn't show up"

        except Exception as ex:
            log("test_DownloadNotification: failed with exception: %s" %
                __builtin__.type(ex).__name__)
            log(traceback.format_exc())
            raise
        except:
            log("test_DownloadNotification: Unknown exception occur, Details:.")
            log(traceback.format_exc())
            raise
        else:
            log("test_DownloadNotification: ends successfully without exception occur.")

    @attr('BVT')
    def test_upload_notification(self):
        # test clip
        self.test_name_video = "Upload_WebAPI.AVI"
        self.test_case_path = prepare_content(
            "1805", False, self.test_name_video)

        op.launch_RT_before_running_case()
        assert_step(self.RT.remove_all_from_mymac_view())

        # add test clip into local library
        log("Add test clip into local library")
        assert_step(self.RT.add_to_my_library(self.test_case_path))

        # upload video to cloud
        log("Upload a video to cloud")
        assert self.RT.does_exist_in_library(upload_video_item, 'Upload', default_wait_long_time)
        self.RT.upload_video(upload_video_item, 'Upload')

        if osx_version == "10.10":
            region.onAppear(upload_complete_notification_10_10, handler)
        elif osx_version == "10.9":
            region.onAppear(upload_complete_notification_10_9, handler)
        region.observe(default_wait_long_time)
        assert TestCase_1805.got_notification, "'Upload Complete' notification doesn't show up"

        # verify upload by calling cloud API
        log("Verify upload by calling cloud API")
        assert wait_for_upload_complete(
            get_title_of_file(self.test_name_video)), "Fail to find test clip '" + self.test_name_video + "' from cloud side after uploading it in library"

    def tearDown(self):
        log("test_DownloadNotification: tearDown start...")
        TestCase_Base.tearDown(self)
        log("test_DownloadNotification: tearDown End...")
