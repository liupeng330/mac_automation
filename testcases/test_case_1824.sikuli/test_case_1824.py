from nose.plugins.attrib import attr
from helper import *
from sikuli import *
from global_config import *

from controls.sign_in_control import *
from controls.rt_control import *
from controls.system_tray_control import *
from controls.player_control import *

import ops.operations as op

from base import *


class TestCase_1824(TestCase_Base):

    """ Playback: Playback video with separate window """

    def setUp(self):
        try:
            TestCase_Base.setUp(self)
            # prepare test content
            self.test_name = "Play_local.mp4"
            self.test_case_path = prepare_content(
                "1824", False, self.test_name)
            self.player = Player(region)
            op.launch_RT_before_running_case()
            assert_step(self.RT.remove_all_from_mymac_view())
        except:
            TestCase_Base.tearDown(self)
            raise

    @attr('BVT')
    def test_play_with_separate_window(self):
        # add test clip into local library
        log("Add test clip into local library")
        assert_step(self.RT.add_to_my_library(self.test_case_path))

        # play it
        log("Play it")
        assert_step(self.RT.play_video(play_local_item, 'Play_local'))

        # verify test clip is played
        log("Verify test clip is played")
        assert_step(self.RT.verify_rt_is_playing_video())

        log("Click 'play_in_separate_window_button'")
        self.RT.play_in_seperate_window()

        log("Wait player start to play")
        assert_step(self.player.wait_till_start_playing())

        log("Maximize player window")
        self.player.maximize()

        log("Verify title of player window")
        assert self.player.get_title() == get_title_of_file(self.test_name), "The title of player window is not equal to '{0}'".format(get_title_of_file(self.test_name))

        log("Close separate window")
        self.player.close()

    def tearDown(self):
        TestCase_Base.tearDown(self)
