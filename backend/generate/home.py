# Standard Modules
import shutil

# Personal Modules
from utils import *

def generate_home():
    """ Interface for main method. """
    with open(meta.content_dir + "home.html", "r") as source:
        html_text = indent(HTML_wrapper("article", text = source.readlines()))

        # Writing to the actual file.
        new_home_loc = meta.root_dir + "home.html"
        shutil.copyfile(meta.template_loc, new_home_loc)
        write_generic(new_home_loc, rel_root_loc = ".", main_flag = html_text)
