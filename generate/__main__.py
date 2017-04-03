import os, sys

from aside import *
from home import *
from contact import *
from blog_content import *
from blog_index import *

os.chdir(os.path.dirname(os.path.dirname(os.path.realpath(__file__ + "/generate"))))

generate_aside()
generate_home()
generate_contact()
generate_blog_content()
generate_blog_index()
