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


class TestCase_1828(TestCase_Base):

    """ Recent Activity: recent uploaded media will show in Recent Uploaded view """

    def setUp(self):
        try:
            TestCase_Base.setUp(self)

            # test clip
            self.test_name_video = "Upload.AVI"
            self.test_case_path = prepare_content(
                "1828", False, self.test_name_video)

            op.launch_RT_before_running_case()
            assert_step(self.RT.remove_all_from_mymac_view())
        except:
            TestCase_Base.tearDown(self)
            raise

    @attr('BVT')
    def test_recent_uploaded(self):
        # add test clip into local library
        log("Add test clip into local library")
        assert_step(self.RT.add_to_my_library(self.test_case_path))

        # upload video to cloud
        log("Upload a video to cloud")
        time.sleep(5)
        self.RT.upload_video(upload_video_item, 'Upload')

        # verify upload by calling cloud API
        log("Verify upload by calling cloud API")
        assert wait_for_upload_complete(
            get_title_of_file(self.test_name_video)), "Fail to get test clip '" + self.test_name_video + "' via API, after uploading it"

        log("Switch to 'Recent Activity -> Uploaded' view")
        assert_step(self.RT.switch_to_recent_activity_uploaded_view())
        assert self.RT.does_exist_in_library(upload_video_item, 'Upload', default_wait_time), \
            "The uploaded item doesn't exists in 'Recent Activity -> Uploaded' view"

    def tearDown(self):
        TestCase_Base.tearDown(self)
