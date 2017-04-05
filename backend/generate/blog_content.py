# Standard Modules
import os
import shutil
import meta

# Personal Modules
from utils import *

class Blog:

    def __init__(self, posts_dir):
        self.posts_dir = posts_dir
        self.posts = list(range(len(os.listdir(self.posts_dir))))
        self.num_posts = len(self.posts)

    #########################
    ### Content Observers ###
    #########################

    def get_title(self, post_num):
        """ Returns the title of this post. """
        with open(self.posts_dir + str(post_num) + ".txt", "r") as post:
            return post.readline().strip("\n")

    def get_date(self, post_num):
        """ Returns the date of this post. """
        with open(self.posts_dir + str(post_num) + ".txt", "r") as post:
            return post.readlines()[1].strip("\n")

    def get_content(self, post_num):
        """ Returns the content of this post. """
        with open(self.posts_dir + str(post_num) + ".txt", "r") as post:
            content = post.readlines()[3:]
            for line in content:
                if meta.categories_tag in line:
                    content.remove(line)
            return content

    ######################
    ### HTML Interface ###
    ######################

    def get_HTML_page_navigation(self, post_num):
        """ Returns the HTML navigation tools for this post. """
        assert post_num + 1 <= self.num_posts
        nav_html = []

        # prev_page
        if post_num > 0:
            nav_html.append(HTML_wrapper("a", {"href":str(post_num-1)+".html", "class":"left index"}, "« " + self.get_title(post_num-1)))
        # next_page
        if post_num < self.num_posts - 1:
            nav_html.append(HTML_wrapper("a", {"href":str(post_num+1)+".html", "class":"right index"}, self.get_title(post_num+1) + " »"))

        return HTML_wrapper("smallNav", text = nav_html) + "<br>"

    def get_HTML_header(self, post_num):
        """ Returns the HTML header for this post. """
        title_html = self.get_title(post_num) + "<br>"
        date_html = HTML_wrapper("img", {"width":10, "height":10, "src":meta.media_dir+"clock.png"}) + " " + self.get_date(post_num)
        comment_html = HTML_wrapper("img", {"width":10, "height":10, "src":meta.media_dir+"speech_bubble.png"}) + " " + HTML_wrapper("a", {"href":"#disqus_thread"}, "Comments")
        subtitle_html = HTML_wrapper("subtitle", text = date_html + " | " + comment_html)
        return HTML_wrapper("h2", text = [title_html, subtitle_html])

    def get_HTML_content(self, post_num):
        """ Returns the HTML content for this post. """
        html = []
        for line in self.get_content(post_num):
            if line != "\n":
                html.append(HTML_wrapper("p", text = line.strip("\n")))

        return html

    def get_HTML_share(self):
        """ Returns the HTML share buttons. """
        with open("../share.html", "r") as share:
            return share.read()

    def get_HTML_comments(self):
        """ Returns the HTML comments section. """
        with open("../comments.html") as comments:
            return comments.read()

    def write_main(self, template_loc, target_dir):
        for post in self.posts:
            # Collecting all of the appropriate text.
            html = []
            html.append(self.get_HTML_page_navigation(post) + "\n")
            html.append(self.get_HTML_header(post) + "\n")
            for line in self.get_HTML_content(post):
                html.append(line + "\n")
            html.append(self.get_HTML_share() + "\n")
            html.append(self.get_HTML_comments())

            html_text = HTML_wrapper("article", text = indent(html))

            # Writing to the actual file.
            new_post_loc = target_dir + str(post) + ".html"
            shutil.copyfile(template_loc, new_post_loc)
            write_generic(new_post_loc, rel_root_loc = "..", main_flag = html_text, blog_active = True)
            
def generate_blog_content():
    """ Interface for the main method. """
    my_blog = Blog(meta.posts_dir)
    my_blog.write_main(meta.template_loc, meta.index_dir)
