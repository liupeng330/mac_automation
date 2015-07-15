from sikuli import *
from controls.screenshots import *
from global_config import *
import time
from helper import *


class SignIn(object):

    def __init__(self, region, username, password):
        self.region = region
        self.username = username
        self.password = password

    def sign_in(self):
        if self.region.exists(sign_in_button, default_wait_time):
            log("Clicking 'Sign In' button")
            self.region.click(sign_in_button)
        elif self.region.exists(sign_in_button2, default_wait_time):
            log("Found 'Sign In' button in 'Sign up' page")
        else:
            return False, "Fail to find 'Sign In' button in sign in panel!!"

        if not self.region.exists(sign_in_button2, default_wait_time):
            return False, "Fail to get 'Sign up' page"

        log("Start to sign in via applescript")
        if not self._fill_email_passwd_with_applescript():
            return False, "Fail to fill 'Email' and 'Password' text box via AppleScript"
        time.sleep(2)
        self.dismiss_welcome_page()
        return True

    def dismiss_welcome_page(self):
        if self.region.exists(welcome_page_recommended, default_wait_time):
            for r in self.region.findAll(welcome_page_recommended):
                self.region.click(r)
        if self.region.exists(sign_in_get_started, default_wait_time):
            log("Clicking 'Get Started' button")
            self.region.click(sign_in_get_started)
        if self.region.exists(welcome_page_get_started, default_wait_time):
            log("Clicking 'Get Started' button in welcome page")
            self.region.click(welcome_page_get_started)

    def _fill_email_passwd_with_applescript(self):
        path_of_script = os.path.join(applescript_path, "fill_email_and_passwd_for_signin.applescript")
        p = subprocess.Popen(['osascript', path_of_script, self.username, self.password], stdout=subprocess.PIPE)
        out, err = p.communicate()
        if 'ERROR' in out:
            return False
        else:
            return True
