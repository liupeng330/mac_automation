from nose.plugins.attrib import attr
from helper import *
from sikuli import *
from global_config import *

from controls.sign_in_control import *
from controls.rt_control import *
from controls.system_tray_control import *

import ops.operations as op

from base import *


class TestCase_1790(TestCase_Base):

    """ Authentication: Sign out from systray """

    def setUp(self):
        try:
            TestCase_Base.setUp(self)
            op.launch_RT_before_running_case()
        except:
            TestCase_Base.tearDown(self)
            raise

    @attr('BVT')
    def test_sign_out_from_systray(self):
        systray = SystemTray(top_menu_bar_region)
        systray.sign_out()
        self.RT.launch()

        # verify RT has sign out
        assert region.exists(sign_in_button, default_wait_time), "Fail to find 'Sign in' button in sign in panel"

    def tearDown(self):
        TestCase_Base.tearDown(self)
