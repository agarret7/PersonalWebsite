# Personal Modules
import blog_index
from utils import *
import meta

def li(text, link = "", header = False):
    """ Returns a new HTML list element for the aside.
            text: input text for the element.
            link: optional link which will create an <a> tag as well.
            header: determines whether or not this element is an aside header. """
    html = text
    if link is not "":
        html = HTML_wrapper("a", {"href":link}, "» " + html)
    if header:
        html = HTML_wrapper("h3", text = html)
    html = HTML_wrapper("li", text = html)
    return html

def generate_aside():
    """ Interface for the main method. """
    aside_html = [li("Featured Posts", header = True)]
    aside_html.append(li("Placeholder to be replaced."))
    # TODO: Implement featured posts functionality

    aside_html.append(li("Categories", header = True))
    my_index = blog_index.Index(meta.content_dir, meta.posts_dir, meta.index_posts_per_page)
    for cat in my_index.categories:
        aside_html.append(li(cat, cat.lower().replace(" ", "_")+".html"))

    aside_html = HTML_wrapper("aside", text = HTML_wrapper("ul", text = aside_html))

    with open("../aside.html", "w") as aside:
        aside.write(aside_html)
