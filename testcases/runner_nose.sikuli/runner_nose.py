import sys
import os

lib = os.path.join(os.path.expanduser("~"), "mac_auto")
if lib not in sys.path:
    sys.path.append(lib)
import global_config

if global_config.path_of_site_packages not in sys.path:
    sys.path.append(global_config.path_of_site_packages)
import nose
from htmloutput.html_for_nose import HtmlOutput

build = None
for arg in sys.argv[1:]:
    if arg.startswith("--build="):
        build = arg.split("=")[1]
        sys.argv.remove(arg)

args = sys.argv[1:]
print args

nose.core.run(argv=args, addplugins=[HtmlOutput(title='OSX RealPlayer Cloud Test Report', build=build)])
