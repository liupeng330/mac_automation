import __builtin__
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



class TestCase_1818(TestCase_Base):

    """ Create Album in RealTimes """

    def setUp(self):
        try:
            log("test_CreateAlbum: setUp start...")
            TestCase_Base.setUp(self)
            log("test_CreateAlbum: setUp end...")
        except:
            TestCase_Base.tearDown(self)
            raise

    @attr('BVT')
    def test_CreateAlbum(self):
        log("test_CreateAlbum: Start...")
        try:
            log("test_CreateAlbum: Start Sign in process.")
            op.launch_RT_before_running_case()
            log("test_CreateAlbum: Sign in successfully.")

            log("test_CreateAlbum: Create Album.")
            op.create_album()
            log("test_CreateAlbum: Create Album and add item to Album successfully.")

            log("test_CreateAlbum: Verify the Album from CloudAPI.")
            wait_for_upload_complete("test")
            log("test_CreateAlbum: The Album is created successfully.")

        except Exception as ex:
            log("test_CreateAlbum: failed with exception: %s" % __builtin__.type(ex).__name__)
            log(traceback.format_exc())
            raise
        except:
            log("test_CreateAlbum: Unknown exception occur, Details:.")
            log(traceback.format_exc())
            raise
        else:
            log("test_CreateAlbum: ends successfully without exception occur.")

    def tearDown(self):
        log("test_CreateAlbum: tearDown start...")
        TestCase_Base.tearDown(self)
        log("test_CreateAlbum: tearDown End...")
