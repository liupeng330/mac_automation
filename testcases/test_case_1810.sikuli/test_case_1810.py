import os
from nose.plugins.attrib import attr
from helper import *
from sikuli import *
from global_config import *

from controls.sign_in_control import *
from controls.rt_control import *
from controls.system_tray_control import *

import ops.operations as op

from base import *


class TestCase_1810(TestCase_Base):

    """ Upload/Download: Download cloud media from gallery view """

    def setUp(self):
        try:
            TestCase_Base.setUp(self)

            # test clip
            self.test_name = "Download.mp4"
            self.test_case_path = os.path.join(
                test_content_path, "original", self.test_name)

            # upload clip to cloud
            assert upload_video_via_API(
                self.test_case_path), "Fail to upload test clip '" + self.test_name + "' via API"

            op.launch_RT_before_running_case()
        except:
            TestCase_Base.tearDown(self)
            raise

    @attr('BVT')
    def test_download(self):
        # verify signed in
        log("Verify signed in")
        assert region.exists(
            has_signed_in_rt_top_bar, default_wait_time), "Fail to sign in to cloud via API"

        # verify test clip is in the view
        log("Verify test clip is in the view")
        assert self.RT.does_exist_in_library(
            download_video_item, 'Download', default_wait_time), \
            "Fail to find thumbnail of test clip '" + self.test_name + "'"

        # play test clip
        log("Play test clip")
        self.RT.play_video(download_video_item, 'Download')

        # verify test clip is played
        log("Verify test clip is played")
        self.RT.verify_rt_is_playing_video()

        # download test clip from bottom bar
        log("Download test clip from bottom bar")
        self.RT.download_via_bottom_bar()

        # verify download complete
        log("Verify download complete")
        assert wait_for_download_complete(
            self.test_name), "After waiting for one minute, test clip '" + self.test_name + "' is not downloaded to local"

        # go back to cloud view
        log("Exit gallery view")
        self.RT.exit_gallery_view()

    def tearDown(self):
        TestCase_Base.tearDown(self)
