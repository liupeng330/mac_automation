from nose.plugins.attrib import attr
from sikuli import *
from global_config import *
from helper import *

from controls.sign_in_control import *
from controls.rt_control import *
from controls.system_tray_control import *

import ops.operations as op

from base import *


class TestCase_1821(TestCase_Base):

    """ Social Info: Like or unlike album in Shared with me """

    def setUp(self):
        try:
            TestCase_Base.setUp(self)

            log("Start to verify if RT is signed in or not")
            if self.RT.is_sign_in:
                log("RT has been signed in already, start to sign out")
                self.RT.sign_out()

            op.launch_RT_before_running_case()
            self.RT.remove_all_from_cloud_view()
            op.create_album()
            assert_step(self.RT.share_album(test_album_item, "test"))
            op.switch_to_account2()
        except:
            TestCase_Base.tearDown(self)
            raise

    @attr('BVT')
    def test_like_unlike_album(self):
        assert_step(self.RT.switch_to_shared_with_me_view())

        # verify the shared album is in the view
        assert self.RT.does_exist_in_library(shared_album_item, "test", default_wait_time), \
            "Fail to find shared album in the 'Share with me' view"

        # like the shared album
        assert_step(self.RT.like_album(shared_album_item))
        self.RT.back_to_album()

        # unlike the same album
        assert_step(self.RT.unlike_album(shared_album_item))

    def tearDown(self):
        TestCase_Base.tearDown(self)
