from os.path import expanduser, join
import os

app_name = "RealTimes"
rpds_service_name = "rpdsvc"

# ------test accounts---------------
env = "int"

# test account
account_username = "mac_se_1@real.com"
account_password = "123456"

# test account for share
account_username2 = "mac_se_2@real.com"
account_password2 = "123456"
# -------------------------------------

# OSX version, pls change to "10.9" if you want to run on OS X 10.9 version
osx_version = "10.10"

# Need to reset realtimes for every test cases
reset_realtimes = True

# Default wait time for searching screenshot
default_wait_time = 10
default_wait_long_time = 60

test_home_path = join(expanduser("~"), "mac_auto")
test_content_path = join(test_home_path, "test_contents")
test_report_path = join(test_home_path, "reports")
screenshot_file_folder = join(test_home_path, "screenshots")
applescript_path = join(test_home_path, "applescript")
crash_report_path = join(test_home_path, "crash")
cliclick_path = join(test_home_path, "cliclick")

server_media_url = "http://media.{0}.real.com/"
server_users_url = "https://users.{0}.real.com/"
server_status_url = "http://events.{0}.real.com/"
server_app_url = "https://beta.{0}.real.com"

cloud_env_string_int = "INT (int.real.com)"
cloud_env_string_int2 = "INT2 (int2.real.com)"
cloud_env_string_prod = "PROD (real.com)"

rpds_config_file = join(
	expanduser("~"), "Library/Application Support/" + app_name + "/RPDS/rpdsvc.cfg")
config_cloud_env_header = "<List Name=\"CloudManager\">"
config_cloud_env_tail = "</List>"

rpds_db_file = join(
	expanduser("~"), "Library/Application Support/" + app_name + "/RPDS/db/library.db")

saved_state_folder = join(
    expanduser("~"), "Library/Saved Application State/com.RealNetworks.app.{0}.savedState".format(app_name)
)

download_root_folder = os.path.join(
    os.path.expanduser("~"), "Movies", app_name)
download_folder = download_root_folder #os.path.join(download_root_folder, "mac's Cloud Downloads")

saved_stories_folder = os.path.join(
    download_root_folder, "Saved Stories")

picture_root_folder = os.path.join(
    os.path.expanduser("~"), "Pictures")

path_of_site_packages = "/Library/Python/2.7/site-packages"

# For parsing unittest log
error_identifers = ['AssertionError', 'AttributeError', 'FindFailed', 'SyntaxError', 'crashed']

# Crash file location
diagnostic_report_paths = ['/Library/Logs/DiagnosticReports', join(expanduser("~"), "Library/Logs/DiagnosticReports")]

if __name__ == "__main__":
    import shutil
    if os.path.isdir(saved_state_folder):
        shutil.rmtree(saved_state_folder)
