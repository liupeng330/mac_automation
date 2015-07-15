import os
from nose.plugins.attrib import attr
from helper import *
from sikuli import *
from global_config import *

from controls.sign_in_control import *
from controls.rt_control import *
from controls.system_tray_control import *
from controls.transfers_control import *

import ops.operations as op

from base import *


class TestCase_1820(TestCase_Base):

    """ Media Management: Add/edit caption """

    def setUp(self):
        try:
            TestCase_Base.setUp(self)

            # test clip
            self.test_name = "rename.mov"
            self.test_case_path = os.path.join(
                test_content_path, "original", self.test_name)

            op.launch_RT_before_running_case()
            assert_step(self.RT.remove_all_from_cloud_view())
        except:
            TestCase_Base.tearDown(self)
            raise

    @attr('BVT')
    def test_edit_caption_library(self):
        # upload clip to cloud
        assert upload_video_via_API(
            self.test_case_path), "Fail to upload test clip '" + self.test_name + "' via API"

        log("Switch to cloud view")
        assert_step(self.RT.switch_to_cloud_view())

        log("Edit caption")
        assert_step(self.RT.edit_caption(rename_video_item, 'rename', rename_text_item, 'new_name'))

        log("Verify rename clip from cloud API")
        assert wait_for_upload_complete("new_name"), "Fail to get renamed clip via API"

    @attr('BVT')
    def test_edit_caption_gallery_view(self):
        # upload clip to cloud
        assert upload_video_via_API(
            self.test_case_path), "Fail to upload test clip '" + self.test_name + "' via API"

        log("Switch to cloud view")
        assert_step(self.RT.switch_to_cloud_view())

        log("Play video to enter gallery view")
        assert_step(self.RT.play_video(rename_video_item, 'rename'))
        assert self.RT.is_in_gallery_view(), "RT doesn't enter into gallery view"

        log("Edit caption")
        assert_step(self.RT.rename_in_gallery_view(rename_video_item_in_gallery_view, "new_name", newname_video_item_in_gallery_view))

        log("Verify rename clip from cloud API")
        assert wait_for_upload_complete("new_name"), "Fail to rename a video in gallery view"

    @attr('BVT')
    def test_edit_caption_album(self):
        log("Create collection via cloud API")
        create_collection_via_API("rename_collection") 

        log("Switch to album")
        retry(self.RT.switch_to_albums_view)

        log("Open album")
        assert_step(self.RT.open_album(rename_collection_item, 'rename_collection'))

        log("Edit caption")
        assert_step(self.RT.rename_album_in_album_header(rename_collection_title, "new_name", newname_collection_title))

        log("Verify rename collection from cloud API")
        assert check_colletion_exist_via_API("new_name"), "Fail to get the renamed collection via API"

    def tearDown(self):
        TestCase_Base.tearDown(self)
