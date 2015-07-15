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


class TestCase_1812(TestCase_Base):

    """ Recent Activity: recent played video will show in Recent Watched view"""

    def setUp(self):
        try:
            TestCase_Base.setUp(self)

            # test clip
            self.test_name = "Play_local.mp4"
            self.test_case_path = prepare_content("1812", False, self.test_name)

            op.launch_RT_before_running_case()
            assert_step(self.RT.remove_all_from_mymac_view())
        except:
            TestCase_Base.tearDown(self)
            raise

    @attr('BVT')
    def test_recent_watched(self):
        # add test clip into local library
        log("Add test clip into local library")
        assert_step(self.RT.add_to_my_library(self.test_case_path))

        # play it
        log("Play it")
        assert_step(self.RT.play_video(play_local_item, 'Play_local'))

        # verify test clip is played
        log("Verify test clip is played")
        assert_step(self.RT.verify_rt_is_playing_video())

        log("Wait 10 sec")
        time.sleep(10)

        # go back to cloud view
        log("Exit gallery view")
        self.RT.exit_gallery_view()

        log("Switch to 'Recent Activity -> Watched' view")
        assert_step(self.RT.switch_to_recent_activity_watched_view())
        assert self.RT.does_exist_in_library(play_local_item, 'Play_local', default_wait_time), \
            "Watched item doesn't exists in 'Recent Activity -> Watched' view"

    def tearDown(self):
        TestCase_Base.tearDown(self)
