import sqlite3
import sys
import os

lib = os.path.join(os.path.expanduser("~"), "mac_auto")
if lib not in sys.path:
    sys.path.append(lib)

from global_config import *

user_name = (sys.argv[1],)
conn = sqlite3.connect(rpds_db_file)
c = conn.cursor()
c.execute('''SELECT connected FROM cloud_user WHERE username = ?''', user_name)
ret = c.fetchall()
conn.close()
if (1,) in ret:
    print 'True'
else:
    print 'False'
