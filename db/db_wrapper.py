import subprocess
import sys


def _exec_command(args):
    """ Run command from args, and return a tuple (returned code, stdout, stderr) """

    print args
    p = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE)
    (output, err) = p.communicate()
    p_status = p.wait()
    return p_status, output

BASE_COMMAND = "python " + "~/mac_auto/db/has_sign_in.py"

def has_sign_in(user_name):
    ret = _exec_command(BASE_COMMAND + " " + user_name)
    return "True" in ret[1]

if __name__ == "__main__":
	print has_sign_in("macauto@real.com")