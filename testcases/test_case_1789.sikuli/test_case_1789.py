import os

from nose.plugins.attrib import attr
import helper
from sikuli import *
from global_config import *

from controls.sign_in_control import *
from controls.rt_control import *
from controls.system_tray_control import *

import ops.operations as op

from base import *


class TestCase_1789(TestCase_Base):

    """ Media Scan: Appropriate fixed folder is scanned """

    def setUp(self):
        try:
            TestCase_Base.setUp(self)

            # prepare test content
            self.test_name = "Upload.AVI"
            self.test_image_name = "MediaScan.JPG"
            self.test_case_path = prepare_content(
                "1789", False, self.test_name)

            op.launch_RT_before_running_case()
            assert_step(self.RT.remove_all_from_mymac_view())

            # add test clip into local library
            log("Add test clip into local library, in order to add path '" +
                self.test_case_path + "' into 'Media Library'")
            assert_step(self.RT.add_to_my_library(self.test_case_path))
        except:
            TestCase_Base.tearDown(self)
            raise

    @attr('BVT')
    def test_add_media_folder_to_preference_as_watch_folder(self):
        assert self.RT.does_exist_in_library(upload_video_item, 'Upload', default_wait_time), "Fail to find Upload.AVI in library"

        # copy file to watch folder
        log("Copy file %s to folder %s" %
            (self.test_image_name, self.test_case_path))
        assert helper.copy_file(os.path.join(test_content_path, "original", self.test_image_name),
                                self.test_case_path), "Fail to copy file from '" + self.test_image_name + "' to folder '" + self.test_case_path + "'"

        # verify the shared item is in the view
        if osx_version == "10.10":
            assert region.exists(new_photo_found_notification_10_10,
                                 default_wait_long_time), "The 'new photo found' notification doesn't show up."
        elif osx_version == "10.9":
            assert region.exists(new_photo_found_notification_10_9,
                                 default_wait_long_time), "The 'new photo found' notification doesn't show up."

        # verify new item is added to library view
        assert self.RT.does_exist_in_library(media_scan_item, 'MediaScan', default_wait_time), "Cannot find the thumbnail of scanned media in library view"

    def tearDown(self):
        TestCase_Base.tearDown(self)
