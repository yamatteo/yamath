import sys
try:
    sys.path.append(__path__[0])
    sys.path.append('')
except NameError:
    pass

from admin_views import *
from session_views import *
from user_views import *
