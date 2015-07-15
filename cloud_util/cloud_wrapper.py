import subprocess
import sys


def exec_command(args):
    """ Run command from args, and return a tuple (returned code, stdout, stderr) """

    p = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE)
    (output, err) = p.communicate()
    p_status = p.wait()
    return p_status, output

BASE_COMMAND = "python " + "~/mac_auto/cloud_util/cloud_util.py"


class Wrapper(object):

    def __init__(self, username, password, env):
        self.env = env
        command = BASE_COMMAND + " --login -u %s -p %s -e %s" % (username, password, env)
        ret = exec_command(command)
        if ret[0] != 0:
            raise Exception("Login failed for command '%s'" % command)
        self.token = ret[1].strip('\n')
        self.base_command = BASE_COMMAND + " -t %s -e %s" % (self.token, self.env)

    def cleanup_all(self):
        ret = exec_command(self.base_command + " --cleanup")
        print ret[1]
        return True if ret[0] == 0 else False

    def upload_videos(self, *videos):
        ret = exec_command(
            self.base_command + " --uploadvideo \"" + ",".join(videos) + "\"")
        print ret[1]
        return True if ret[0] == 0 else False

    def upload_photos(self, *photos):
        ret = exec_command(
            self.base_command + " --uploadimage \"" + ",".join(photos) + "\"")
        print ret[1]
        return True if ret[0] == 0 else False

    def create_collection(self, name):
        ret = exec_command(self.base_command + " --createcollection " + name)
        print ret[1]
        return True if ret[0] == 0 else False

    def check_exist(self, title):
        ret = exec_command(self.base_command + " --check " + "\"" + title + "\"")
        print ret[1]
        return True if ret[0] == 0 else False

    def add_to_collection(self, collection_title, *media_title):
        ret = exec_command(
            self.base_command + " --addtocollection " + collection_title + " " + " ".join(media_title))
        print ret[1]
        return True if ret[0] == 0 else False

    def check_collection_exist(self, title):
        ret = exec_command(self.base_command + " --checkcollection " + title)
        print ret[1]
        return True if ret[0] == 0 else False

if __name__ == "__main__":
    w = Wrapper("macauto@real.com", "123456", "int")
