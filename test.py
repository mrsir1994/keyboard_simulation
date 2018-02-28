import os
print type(os.geteuid())
print type(os.getlogin())

from time import gmtime, strftime
import time
print strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print type(strftime("%a, %d %b %Y %H:%M:%S", time.localtime(10.5)))