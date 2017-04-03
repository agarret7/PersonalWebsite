# Standard Modules
import shutil

# Personal Modules
from utils import *

def generate_contact():
    """ Interface for main method. """
    with open(meta.content_dir + "contact.html", "r") as source:
        html_text = indent(HTML_wrapper("article", text = source.readlines()))

        # Writing to the actual file.
        new_contact_loc = meta.root_dir + "contact.html"
        shutil.copyfile(meta.template_loc, new_contact_loc)
        write_generic(new_contact_loc, rel_root_loc = ".", main_flag = html_text, contact_active = True)
