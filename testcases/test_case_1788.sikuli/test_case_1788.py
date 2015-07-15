from nose.plugins.attrib import attr
from helper import *
from sikuli import *
from global_config import *

from controls.sign_in_control import *
from controls.rt_control import *
from controls.system_tray_control import *

import ops.operations as op

from base import *


class TestCase_1788(TestCase_Base):

    """ Authentication: Sign in from systray """

    def setUp(self):
        try:
            TestCase_Base.setUp(self)

            log("Start to verify if RT is signed in or not")
            if self.RT.is_sign_in:
                log("RT has been signed in already, start to sign out")
                self.RT.sign_out()
        except:
            TestCase_Base.tearDown(self)
            raise

    @attr('BVT')
    def test_sign_in_from_systray(self):
        self.RT.launch()

        # verify RT has sign out
        assert region.exists(sign_in_button, default_wait_time), "Fail to find sign in button in sign in panel"

        # sign in from system tray
        op.sign_in_from_systray()
        assert self.RT.is_sign_in, "RT doesn't sign in"

    def tearDown(self):
        TestCase_Base.tearDown(self)
