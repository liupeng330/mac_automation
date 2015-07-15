from sikuli import *
from controls.screenshots import *
from helper import *
from global_config import *
import time

class SystemTray(object):

    def __init__(self, region):
        self.region = region

    def sign_in(self):
        self.click_system_tray()
        log("click sign in menu item from system tray")

        # Need to use default screen region due to popup menu isn't shown in
        # top menu area
        if osx_version == "10.10":
            region.click(system_tray_signin_10_10)
        elif osx_version == "10.9":
            region.click(system_tray_signin_10_9)

    def sign_out(self):
        self.click_system_tray()
        log("click sign out menu item from system tray")
        # Need to use default screen region due to popup menu isn't shown in
        # top menu area
        click(system_tray_signout)

    def quit(self):
        self.click_system_tray()
        log("click quit menu item from system tray")
        click(system_tray_quit)

    def pause(self):
        self.click_system_tray()
        log("click pause menu item from system tray")
        click(system_tray_pause)

    def resume(self):
        self.click_system_tray()
        log("click resume menu item from system tray")
        click(system_tray_resume)

    def click_system_tray(self):
        log("click RT icon on system tray")
        self.region.click(system_tray_icon)

    def switch_cloud_env(self, env):
        log("switch cloud env to " + env)
        self.click_system_tray()
        time.sleep(1)
        type("Qu")
        try:
            region.keyDown(Key.CTRL)
            region.keyDown(Key.SHIFT)
            type(Key.ENTER)
        finally:
            region.keyUp(Key.CTRL)
            region.keyUp(Key.SHIFT)

        time.sleep(1)
        run_apple_script("set_cloud_env.applescript", self._get_cloud_env_string(env))

    def _get_cloud_env_string(self, env):
        if env == "int":
            return cloud_env_string_int
        if env == "int2":
            return cloud_env_string_int2
        if env == "prod":
            return cloud_env_string_prod


if __name__ == "__main__":
    s = SystemTray(top_menu_bar_region)
    s.quit()
