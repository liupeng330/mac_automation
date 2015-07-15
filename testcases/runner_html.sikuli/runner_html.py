import sys
import os
import re
import unittest

lib = os.path.join(os.path.expanduser("~"), "mac_auto")
if lib not in sys.path:
    sys.path.append(lib)

from global_config import *

if path_of_site_packages not in sys.path:
    sys.path.append(path_of_site_packages)

from htmloutput.html_test_runner import HTMLTestRunner

report_file = None
test_case_ids = None
build = None
for arg in sys.argv[1:]:
    if arg.startswith("report:"):
        report_file = arg.split(":")[1]
        print "test result file is " + report_file
    if arg.startswith("cases:"):
        test_case_ids = arg.split(":")[1].split(",")
    if arg.startswith("build:"):
        build = arg.split(":")[1]

# It'll load all test caes in current folder if no test case indicated
if test_case_ids is None or len(test_case_ids) == 0:
    print "Loading all test cases in current folder"
    test_case_module_names = [re.sub("\.sikuli$", "", i) for i in os.listdir(
        os.path.join(test_home_path, "testcases")) if i.startswith("test_case")]
else:
    test_case_module_names = ["test_case_{0}".format(i) for i in test_case_ids]

test_case_modules = []
for i in test_case_module_names:
    print "Importing module " + i
    test_case_modules.append(__import__(i, globals(), locals(), [], -1))

suite = None
if len(test_case_modules) >= 1:
    suite = unittest.TestLoader().loadTestsFromModule(test_case_modules[0])
for m in test_case_modules[1:]:
    suite.addTests(unittest.TestLoader().loadTestsFromModule(m))

outfile = open(report_file, "w")
runner = HTMLTestRunner(stream=outfile, verbosity=2, title='OSX RealPlayer Cloud Test Report', build=build)

print "Start running test"
runner.run(suite)
