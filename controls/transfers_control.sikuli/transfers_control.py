from sikuli import *
from controls.screenshots import *
from global_config import *
import time


class Transfers(object):
    def __init__(self, region):
        self.region = region

    def clear_all(self):
        if not self.region.exists(transfer_dialog):
            return False, "Transfers dialog should be exist"
        self.region.click(transfer_dialog_clear_completed_button)

        while not self.region.exists(transfer_dialog_no_item):
            cancel_button_all = self.region.findAll(transfer_dialog_cancel_button)
            for cancel_button in cancel_button_all:
                self.region.click(cancel_button)
                time.sleep(1)

        return True

    def pause_all(self):
        if not self.region.exists(transfer_dialog):
            return False, "Transfers dialog should be exist"

        pause_button_all = self.region.findAll(transfer_dialog_pause_button)
        for pause_button in pause_button_all:
            self.region.click(pause_button)
            time.sleep(1)

        return True

    def resume_all(self):
        if not self.region.exists(transfer_dialog):
            return False, "Transfers dialog should be exist"

        resume_button_all = self.region.findAll(transfer_dialog_resume_button)
        for resume_button in resume_button_all:
            self.region.click(resume_button)
            time.sleep(1)

        return True


    def exists(self):
        return self.region.exists(transfer_dialog, default_wait_time)
