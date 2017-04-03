import meta

def get_aside():
    """ Gets the aside text from the aside file. """
    with open("../aside.html") as aside_file:
        return ''.join(indent(aside_file.readlines()))

def check_input(text):
    """ Ensures that text is a string or a list of strings. """
    assert isinstance(text, (str, list))
    if isinstance(text, list):
        for line in text:
            assert isinstance(line, str)

def HTML_wrapper(tag, attributes = {}, text = ""):
    """ Wraps some text in tags with a given dict of attributes.

        tag: HTML tag to wrap text.
        attributes: List of attributes to modify the tag.
        text: text to be wrapped. Must be a string, or a list of strings.
        returns: An inline HTML tag wrapping text if it's a string,
        or a block tag if it's a list of strings.
        
        eg 1. HTML_wrapper('a', {"href" : "home.html"}, "link") returns
            <a href="home.html">link</a>

        eg 2. HTML_wrapper('p', text = ["some text"]) returns
            <p>
              some text
            </p>
    """
    check_input(text)
    
    elem = "<" + tag
    for attr, value in attributes.items():
        elem += " " + attr + '=\"' + str(value) + '\"'
    elem += ">"
    
    if isinstance(text, str):
        elem += text
    else:
        elem += "\n"
        for block in text:
            block = block.split("\n")
            for line in block:
                elem += "  " + line + "\n"

    elem += "</" + tag + ">"
    return elem

def indent(text, num_spaces = meta.indentation):
    """ Indents the given text by num_spaces.

        text: text to indent. Must be a string, or a list of strings.
        num_spaces: number of spaces to indent. Must be an non-negative int.
        returns: same type as text, with appropriate indents.
    """
    check_input(text)

    if isinstance(text, str):
        text_list = text.split("\n")
        text_list = [num_spaces*" " + t for t in text_list]
        return "\n".join(text_list)
    else:
        text = [num_spaces*" " + t for t in text]
        return text
    
def write_generic(target, rel_root_loc = '.', main_flag = '', blog_active = False, contact_active = False):
    """ Generates the file from the template according to the provided flags.

        target: HTML document to be formatted.
        rel_root_loc: Location of the main folder relative to this folder.
        main_flag: text representing text to be put in the main part of the template.
        blog_active: boolean representing whether or not current page is the blog.
        contact_active: boolean representing whether or not current page is contact.
        returns: html_text. Modifies target file to be html_text.
    """
    with open(target, "r+") as target_file:
        template = target_file.read()
        html_text = template.format(rel_root_loc = rel_root_loc, main_flag = main_flag,
                                    blog_active = "active" if blog_active else "",
                                    contact_active = "active" if contact_active else "")
        target_file.seek(0)
        target_file.truncate()
        target_file.write(html_text)
        return html_text

