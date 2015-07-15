import os
import time
from nose.plugins.attrib import attr

import helper
from sikuli import *
from global_config import *

from controls.sign_in_control import *
from controls.rt_control import *
from controls.system_tray_control import *

import ops.operations as op

from base import *


class TestCase_1795(TestCase_Base):

    """ Media Scan: Add new media files to the watch folder """

    def setUp(self):
        try:
            TestCase_Base.setUp(self)

            # prepare test content
            self.test_image_name = "MediaScan.JPG"
            self.test_image_full_path = os.path.join(
                test_content_path, "original", self.test_image_name)
            if os.path.exists(os.path.join(picture_root_folder, self.test_image_name)):
                os.remove(
                    os.path.join(picture_root_folder, self.test_image_name))

            op.launch_RT_before_running_case()
            assert_step(self.RT.remove_all_from_mymac_view())
        except:
            TestCase_Base.tearDown(self)
            raise

    @attr('BVT')
    def test_add_new_media_files_to_watch_folder(self):
        # enable pictures from media library
        log("select checkbox '" + picture_root_folder +
            "' from media library preferences dialog")
        op.check_one_item_in_media_library_preferences(picture_root_folder)

        log("wait one minute for library loading")
        time.sleep(60)

        # copy file to watch folder
        log("Copy file %s to pictures watch folder %s" %
            (self.test_image_name, picture_root_folder))
        assert helper.copy_file(self.test_image_full_path, picture_root_folder), "Fail to copy file from '%s' to pictures watch folder '%s'" % (
            self.test_image_name, picture_root_folder)

        # verify the shared item is in the view
        if osx_version == "10.10":
            assert region.exists(new_photo_found_notification_10_10,
                                 default_wait_long_time), "The 'new photo found' notification doesn't show up."
            assert region.waitVanish(
                new_photo_found_notification_10_10, default_wait_long_time), "The notification doesn't be dismissed after a while"
        elif osx_version == "10.9":
            assert region.exists(new_photo_found_notification_10_9,
                                 default_wait_long_time), "The 'new photo found' notification doesn't show up."
            assert region.waitVanish(
                new_photo_found_notification_10_9, default_wait_long_time), "The notification doesn't be dismissed after a while"
        time.sleep(2)
        log("search scanned media in library")
        rt = RT(region)
        rt.search_library(self.test_image_name)

        # verify new item is added to library view
        assert self.RT.does_exist_in_library(media_scan_item, 'MediaScan', default_wait_time), "Cannot find the thumbnail of scanned media in library view"

    def tearDown(self):
        TestCase_Base.tearDown(self)
