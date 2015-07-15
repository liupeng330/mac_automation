from helper import *
from sikuli import *
from global_config import *
from screenshots import *

from controls.sign_in_control import *
from controls.rt_control import *
from controls.system_tray_control import *
from controls.transfers_control import *

from cloud_util.cloud_wrapper import *
import time
import os

rt = RT(region)
system_tray = SystemTray(top_menu_bar_region)
cloud_helper = Wrapper(account_username, account_password, env)


def sign_in(username=account_username, password=account_password, retry=10):
    s = SignIn(region, username, password)
    while (True):
        try:
            assert_step(s.sign_in())
            break
        except:
            if retry > 1:
                log("Got exception from 'sign_in' method, will retry, %s times left." % retry)
                retry -= 1
            else:
                log("Got exception from 'sign_in' method, will throw it")
                raise


def sign_in_from_systray(username=account_username, password=account_password):
    systray = SystemTray(top_menu_bar_region)
    systray.sign_in()
    assert region.exists(sign_in_button2, default_wait_time * 3), "Fail to find 'Sign in' button in sing in page"
    sign_in(username, password)


def sign_out():
    rt.sign_out()
    rt.quit()


def launch_RT_before_running_case(retry=3):
    if retry <= 0:
        assert False, \
            ('After signing in via UI with username "{0}", and searching DB by using this SQL: '
             '"SELECT connected FROM cloud_user WHERE username = {0}", '
             'the data field "connected" is not equal to 1'
             ''
             ).format(account_username)

    log("Launch RT")
    rt.launch()

    time.sleep(2)
    if not rt.is_sign_in:
        log("Not sign in, start to sign in first")
        sign_in()

    time.sleep(5)
    log("verify if corrent user has signed in to RT from reading DB")
    if not has_signed_in_from_db(account_username):
        log(
            "The incorrect account has signed in to RT, will sign out and sign in with account '" + account_username + "' again")
        rt.sign_out()
        retry -= 1
        launch_RT_before_running_case(retry)
        return
    log("set RealTimes to initial status for running case")
    assert_step(rt.set_to_init_env())

    log("uncheck all item in media libary")
    uncheck_all_watch_folder_in_media_library_preferences()

    log("switch between all and cloud tab, to make spin disappear")
    wait_for_load_complete(3)


def first_launch_RT():
    if region.exists(first_launch_warning_dialog, default_wait_time):
        log("It's the first time to launch RT")
        region.click(first_lannch_warning_dialog_open_button)
    else:
        log("It's NOT the first time to launch RT")


def create_album():
    log("Now create album")
    if not rt.is_sign_in:
        log("Not sign in, start to sign in first")
        sign_in()

    # test clip
    test_name = "Download.mp4"
    test_case_path = os.path.join(
        test_content_path, "original", test_name)
    assert os.path.isfile(test_case_path), "Fail to find test file in '" + test_case_path + "'"

    # upload clip to cloud
    assert helper.upload_video_via_API(
        test_case_path), "Fail to upload test file '" + self.test_name + "' via API"

    # add the clip to the new created album
    assert_step(rt.add_item_to_album(download_video_item, "Download"))


def drag_drop_folder_to_rt(drag_from_folder):
    """ drag a folder to rt to let it upload to cloud """

    put_finder_to_right_side_of_screen(drag_from_folder)
    region.dragDrop(
        upload_folder_item_in_finder_icon_view, select_current_view)
    dismiss_upload_folder_dialog()


def drag_drop_folder_to_transfers_dialog(drag_from_folder):
    """ drag a folder to transfers dialog, to let it upload to cloud """

    put_finder_to_right_side_of_screen(drag_from_folder)
    region.dragDrop(
        upload_folder_item_in_finder_icon_view, transfer_dialog)
    dismiss_upload_folder_dialog()


def drag_drop_folder_to_system_tray(drag_from_folder):
    """ drag a folder to system tray, to let it upload to cloud """

    put_finder_to_right_side_of_screen(drag_from_folder)
    dragDrop(
        upload_folder_item_in_finder_icon_view, system_tray_icon)
    dismiss_upload_folder_dialog()


def dismiss_upload_folder_dialog():
    region.wait(folder_upload_to_cloud_dialog, default_wait_time)
    time.sleep(1)
    type(Key.ENTER)
    region.waitVanish(folder_upload_to_cloud_dialog, default_wait_time)


def clear_all_items_in_transfers_dialog():
    """
    open transfers dialog,
    clear all items in Transfers dialog,
    and close it
    """

    rt.open_transfers_dialog()
    transfers_dialog = Transfers(region)
    assert_step(transfers_dialog.clear_all())
    type("w", Key.CMD)
    assert not transfers_dialog.exists(), "Fail to dismiss 'Transfers' dialog"


def stop_all_items_in_transfers_dialog():
    """
    open transfers dialog,
    stop all items in Transfers dialog,
    and close it
    """

    rt.open_transfers_dialog()
    transfers_dialog = Transfers(region)
    assert_step(transfers_dialog.pause_all())
    type("w", Key.CMD)
    assert not transfers_dialog.exists(), "Fail to dismiss 'Transfers' dialog"


def stop_and_resume_items_in_transfers_dialog():
    """
    open transfers dialog,
    stop all items, and resume all items,
    and close it
    """

    rt.open_transfers_dialog()
    transfers_dialog = Transfers(region)
    assert_step(transfers_dialog.pause_all())
    assert_step(transfers_dialog.resume_all())
    type("w", Key.CMD)
    assert not transfers_dialog.exists(), "Fail to dismiss 'Transfers' dialog"


def stop_and_resume_items_in_systray():
    """
    stop all items and resume all item
    """

    system_tray.pause()
    time.sleep(10)
    system_tray.resume()


def put_transfers_dialog_to_left_side_of_screen():
    rt.open_transfers_dialog()
    os.system(
        "osascript " + os.path.join(applescript_path, "put_transfers_dialog_to_left_side_of_screen.applescript"))


def uncheck_all_watch_folder_in_media_library_preferences():
    os.system(
        "osascript " + os.path.join(applescript_path, "uncheck_all_watch_folder.applescript"))


def check_one_item_in_media_library_preferences(name):
    os.system(
        "osascript " + os.path.join(applescript_path, "select_one_item_in_media_library.applescript") + " " + name)


def drag_drop_clips_to_library(test_content_path, *clips):
    log("Navigate to test content path")
    put_finder_to_right_side_of_screen(test_content_path)

    for clip in clips:
        assert region.exists(clip,
                             default_wait_time), "Fail to find test clip from screen before doing Drag&Drop operation"
        log("Drag drop a clip to RT")
        region.dragDrop(clip, select_current_view)


def drag_drop_clips_to_transfers_dialog(test_content_path, *clips):
    log("Navigate to test content path")
    put_finder_to_right_side_of_screen(test_content_path)

    for clip in clips:
        assert region.exists(clip,
                             default_wait_time), "Fail to find test clip from screen before doing Drag&Drop operation"
        log("Drag drop a clip to transfers dialog")
        region.dragDrop(clip, transfer_dialog)


def drag_drop_clips_to_system_tray(test_content_path, *clips):
    log("Navigate to test content path")
    put_finder_to_right_side_of_screen(test_content_path)

    for clip in clips:
        assert region.exists(clip,
                             default_wait_time), "Fail to find test clip from screen before doing Drag&Drop operation"
        log("Drag drop a clip to system tray")
        dragDrop(clip, system_tray_icon)


def switch_to_account2():
    # sign out account, then sign in account2
    # You'd better use switch_to_account directly.
    if rt.is_sign_in:
        rt.sign_out()

    rt.launch()
    sign_in(account_username2, account_password2)
    log("After sign in")

    assert region.exists(
        has_signed_in_rt_top_bar,
        default_wait_time), "Fail to sign in with another test account '" + account_username2 + "'"


def switch_to_account(account=account_username2, password=account_password2):
    '''
    account: specify a account to switch to
    '''
    if rt.is_sign_in:
        rt.sign_out()

    rt.launch()
    sign_in(account, password)
    log("after sign in")

    assert region.exists(has_signed_in_rt_top_bar, default_wait_time), "Has not signed in to cloud"


def wait_for_load_complete(switch_times):
    '''
    workaround for make spin disappear
    '''
    while not check_exist_by_cliclick("init"):
        rt.switch_to_cloud_view()
        time.sleep(1)
        rt.switch_to_all_view()
        switch_times -= 1
        if switch_times == 0:
            log(">>>>*** Still cannot find 'init' in library view!! ***<<<<")
            return
    else:
        log("Get 'init' in library")
        return
