import subprocess
import signal
import os
import shutil
import time
import inspect
import xml.etree.ElementTree as ET
import glob

from cloud_util.cloud_wrapper import *
from global_config import *
from datetime import datetime

from db.db_wrapper import *

from sikuli import Debug

cloud_helper = Wrapper(account_username, account_password, env)
cloud_helper_for_account2 = Wrapper(account_username2, account_password2, env)


def get_process_id(name):
    p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    for line in out.splitlines():
        if name in line:
            log("Process: " + line)
            return int(line.split(None, 1)[0])
    return None


def kill_process(name, retry_times=3):
    pid = get_process_id(name)
    while pid is not None:
        try:
            os.kill(pid, signal.SIGKILL)
        except OSError:
            log("Getting error when killing process: {0},{1}".format(name, pid))
        finally:
            retry_times -= 1
            if retry_times == 0:
                raise OSError("Fail to kill process {0},{1}".format(name, pid))
            time.sleep(5)
            pid = get_process_id(name)


def kill_RT():
    kill_process(app_name)


def kill_rpds():
    kill_process(rpds_service_name)
    time.sleep(5)


def cleanup_cloud_download_folder():
    if os.path.isdir(download_root_folder):
        shutil.rmtree(download_root_folder)


def wait_for_download_complete(file_name, timeout=60):
    start = time.time()
    while not os.path.exists(os.path.join(download_folder, file_name)):
        if (time.time() - start) > timeout:
            return False
    return True


def wait_for_upload_complete(title, timeout=60):
    start = time.time()
    while not cloud_helper.check_exist(title):
        time.sleep(10)
        if (time.time() - start) > timeout:
            return False
    return True


def prepare_content(test_case_name, create_subfolder, *original_file_names):
    test_case_dir = os.path.join(
        test_content_path, test_case_name + "_" + get_time_stamp())
    old_test_dir = test_case_dir
    if create_subfolder:
        test_case_dir = os.path.join(test_case_dir, "test_folder")
    if not os.path.exists(test_case_dir):
        os.makedirs(test_case_dir)
    for test_file in original_file_names:
        src = os.path.join(test_content_path, "original", test_file)
        dst = os.path.join(test_case_dir, test_file)
        shutil.copyfile(src, dst)
    return old_test_dir


def cleanup_cloud_content_via_API():
    return cloud_helper.cleanup_all() and cloud_helper_for_account2.cleanup_all()


def upload_video_via_API(*path):
    return cloud_helper.upload_videos(*path)


def upload_photo_via_API(*path):
    return cloud_helper.upload_photos(*path)


def upload_video_files_via_API(*test_file_names):
    all_paths = []
    for i in test_file_names:
        all_paths.append(os.path.join(test_content_path, "original", i))

    # upload clip to cloud
    assert upload_video_via_API(
        *all_paths), "Fail to upload video files '" + ", ".join(test_file_names) + "' to cloud via API"


def upload_photo_files_via_API(*test_file_names):
    all_paths = []
    for i in test_file_names:
        all_paths.append(os.path.join(test_content_path, "original", i))

    # upload clip to cloud
    assert upload_photo_via_API(
        *all_paths), "Fail to upload photo files '" + ", ".join(test_file_names) + "' to cloud via API"


def create_collection_via_API(name):
    return cloud_helper.create_collection(name)


def check_colletion_exist_via_API(title):
    return cloud_helper.check_collection_exist(title)


def add_to_collection(collect_title, *media_titles):
    return cloud_helper.add_to_collection(collect_title, *media_titles)


def replace_string_in_file(file_name, search, replace):
    with open(file_name) as f:
        text = f.read()
    text = text.replace(search, replace)
    with open(file_name, 'w') as f:
        f.write(text)


def enable_rpds_debug():
    removed_lines = ""
    with file(rpds_config_file) as f:
        lines = f.readlines()
        removed_lines = [i for i in lines if "DebugLevel" in i]
    for i in removed_lines:
        replace_string_in_file(rpds_config_file, i, "")
    with open(rpds_config_file, "a") as f:
        f.write("""<Var DebugLevel="-1"/>""")


def set_cloud_env(env):
    # get lines need to be replaced
    removed_lines = ""
    with file(rpds_config_file) as f:
        lines = f.readlines()
        got_header = False
        for i in range(0, len(lines)):
            if config_cloud_env_header in lines[i]:
                got_header = True
            if got_header:
                removed_lines = removed_lines + lines[i]
                if config_cloud_env_tail in lines[i]:
                    got_header = False

    # prepare url according to env
    media_url = ""
    users_url = ""
    status_url = ""
    app_url = ""
    if env == 'int' or env == 'int2':
        media_url = server_media_url.format(env)
        users_url = server_users_url.format(env)
        status_url = server_status_url.format(env)
        app_url = server_app_url.format(env)
    elif env == 'prod':
        media_url = server_media_url.replace("{0}.", "")
        users_url = server_users_url.replace("{0}.", "")
        status_url = server_status_url.replace("{0}.", "")
        app_url = server_app_url.replace("{0}.", "")

    # set env
    root = ET.fromstringlist(removed_lines)
    for el in root.findall("Var"):
        if "ServerMediaURL" in el.attrib:
            el.attrib["ServerMediaURL"] = media_url
        if "ServerUsersURL" in el.attrib:
            el.attrib["ServerUsersURL"] = users_url
        if "ServerStatusURL" in el.attrib:
            el.attrib["ServerStatusURL"] = status_url
        if "ServerAppURL" in el.attrib:
            el.attrib["ServerAppURL"] = app_url

    # change config file
    replace_lines = ET.tostring(root) + "\n"
    replace_string_in_file(rpds_config_file, removed_lines, replace_lines)


def exec_command(args):
    p = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE)
    (output, err) = p.communicate()
    p_status = p.wait()
    return p_status, output


def run_apple_script(file_name, *args):
    command = "osascript " + os.path.join(applescript_path, file_name)
    for arg in args:
        command = command + " " + "\"" + arg + "\""
    ret = exec_command(command.strip())
    if ret[0] != 0:
        raise Exception(ret[1])
    return ret[1]


def get_bounds_of_screen():
    out = run_apple_script("get_bounds_of_screen.applescript").rstrip('\n').split(',')
    return int(out[2]), int(out[3])


def get_height_of_dock():
    return int(run_apple_script("get_height_of_dock.applescript").rstrip('\n'))


def get_time_stamp():
    local_time = time.localtime(time.time())
    return "{0}-{1}-{2}_{3}-{4}-{5}".format(local_time.tm_year, local_time.tm_mon, local_time.tm_mday, local_time.tm_hour, local_time.tm_min, local_time.tm_sec)


def rerun_apple_script(file_name, retry_times, *args):
    while(retry_times > 0):
        retry_times -= 1
        try:
            run_apple_script(file_name, *args)
            return
        except:
            if retry_times <= 0:
                log("Fail to retry, raise exception!!")
                raise
            else:
                log("Try again")
                time.sleep(5)


def retry(method, retry_times=5):
    while(retry_times > 0):
        retry_times -= 1
        try:
            assert_step(method())
            return
        except:
            if retry_times <= 0:
                log("Fail to retry, raise exception!!")
                raise
            else:
                log("Try again")


def get_title_of_file(file_fullpath):
    return os.path.splitext(os.path.basename(file_fullpath))[0]


def capture_screen(file_name):
    if not os.path.exists(screenshot_file_folder):
        os.makedirs(screenshot_file_folder)
    full_path = os.path.join(screenshot_file_folder, file_name)
    log("Capture screen to '" + full_path + "'")
    os.system("screencapture " + full_path)


def put_finder_to_right_side_of_screen(path):
    path_of_script = os.path.join(
        applescript_path, "put_finder_window_to_right_side_of_screen.applescript")
    os.system("osascript {0} {1}".format(path_of_script, path))


def reset_DB_from_preferences_dialog():
    run_apple_script("reset_DB.applescript")


def assert_step(result):
    if result is None:
        return
    if isinstance(result, bool):
        assert result
    elif isinstance(result, tuple) and len(result) == 2:
        assert result[0], result[1]


def log(content):
    caller = inspect.getframeinfo(inspect.currentframe().f_back)[2]
    print "[%s] [%s] %s" % (str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')), caller, content)
    Debug.user(content)


def copy_file(file_path, folder_path):
    try:
        shutil.copy(file_path, folder_path)
    except Exception, e:
        log("There is a copy exception: %s" % e)
        return False
    return True


def turn_on_wifi():
    if not os.system("networksetup -setairportpower en0 on"):
        return True
    return False


def turn_off_wifi():
    if not os.system("networksetup -setairportpower en0 off"):
        return True
    return False


def has_signed_in_from_db(user_name):
    return has_sign_in(user_name)


def dismiss_crash_dialog():
    path_of_script = os.path.join(
    applescript_path, "dismiss_crash_dialog.applescript")
    os.system("osascript {0}".format(path_of_script))


def cleanup_diagnostic_report_folders():
    for p in diagnostic_report_paths:
        files = glob.glob(os.path.join(p, 'RealTimes*'))
        files = files + (glob.glob(os.path.join(p, 'rpdsvc*')))
        for f in files:
            log("Removing crash file '{0}'".format(str(f)))
            try:
                os.remove(f)
            except Exception:
                log("Fail to delete crash file, pls use 'sudo' to run automation!")
                raise


def fetch_diagnostic_report_files():
    if not os.path.exists(crash_report_path):
        os.makedirs(crash_report_path)
    for p in diagnostic_report_paths:
        files = glob.glob(os.path.join(p, 'RealTimes*'))
        for f in files:
            log("RealTimes crashed: '{0}'".format(get_title_of_file(str(f))))
            copy_file(str(f), crash_report_path)
        files = glob.glob(os.path.join(p, 'rpdsvc*'))
        for f in files:
            log("RPDS crashed: '{0}'".format(get_title_of_file(str(f))))
            copy_file(str(f), crash_report_path)


def click_item_by_cliclick(name):
    command = cliclick_path + " c:{0}"
    _run_for_cliclick(name, command)


def double_click_item_by_cliclick(name):
    command = cliclick_path + " dc:{0}"
    _run_for_cliclick(name, command)


def right_click_item_by_cliclick(name):
    command = cliclick_path + " kd:ctrl c:{0} ku:ctrl"
    _run_for_cliclick(name, command)


def check_exist_by_cliclick(name):
    try:
        run_apple_script("get_clip_position_in_library.applescript", name)
    except Exception:
        return False
    return True


def _run_for_cliclick(name, command):
    co = run_apple_script("get_clip_position_in_library.applescript", name).strip().rstrip('\n')
    time.sleep(1)
    command = command.format(co)
    ret = exec_command(command)
    if ret[0] != 0:
        raise Exception(ret[1])


def multiple_select_by_cliclick(names):
    command = " kd:cmd"
    for name in names:
        command += " c:" + run_apple_script("get_clip_position_in_library.applescript", name).strip().rstrip('\n')
    command += " ku:cmd"
    command = cliclick_path + command
    ret = exec_command(command)
    if ret[0] != 0:
        return False
    return True


if __name__ == "__main__":
    cleanup_cloud_content_via_API()
