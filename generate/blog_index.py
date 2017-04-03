# Standard Modules
import os
import shutil

# Personal Modules
from utils import *
import meta

class Index:

    def __init__(self, content_dir, posts_dir, posts_per_page):
        self.content_dir = content_dir
        self.posts_dir = posts_dir
        self.posts_per_page = posts_per_page

        # Posts sorted from newest to oldest.
        self.posts = list(range(len(os.listdir(self.posts_dir))))[::-1]
        self.num_pages = len(self.posts) // self.posts_per_page + 1
        self.categories = set([cat for cat_list in map(self.get_categories, self.posts) for cat in cat_list])

    #########################
    ### Content Observers ###
    #########################

    def get_categories(self, post_num):
        """ Get the categories a post is under. """
        with open(self.posts_dir + str(post_num) + ".txt", "r") as post:
            # Categories are taken to be on the last line.
            paragraphs = post.readlines()
            for p in paragraphs[::-1]:
                if meta.categories_tag in p:
                    categories = p[len(meta.categories_tag):].lstrip().split(", ") # Removing tag and whitespace characters.
                    categories = list(filter(None, [cat.strip("\n") for cat in categories])) # Cleaning it up.
                    return categories
            return []

    def filter_posts(self, category):
        """ Returns a list of posts sorted under this category. """
        posts_in_category = []
        for post_num in self.posts:
            if category in self.get_categories(post_num):
                posts_in_category.append(post_num)

        return posts_in_category

    ######################
    ### HTML Interface ###
    ######################

    def get_HTML_header(self):
        """ Returns the HTML header for this index page. """
        with open(self.content_dir + "blog_index.html") as header:
            return header.read()

    def get_HTML_stub(self, post_num):
        """ Returns an HTML stub of this post. """
        post_html = ""
        with open(self.posts_dir + str(self.posts[post_num]) + ".txt", "r") as post:
            # Getting relevent information from the document.
            title_html = HTML_wrapper("a", {"href":str(self.posts[post_num])+".html"}, post.readline().strip("\n")) + "<br>"
            date_html = HTML_wrapper("img", {"width":10, "height":10, "src":meta.media_dir+"clock.png"}) + " " + post.readline().strip("\n")
            categories = self.get_categories(self.posts[post_num])
            if len(categories) > 0:
                category_links = [HTML_wrapper("a", {"href":cat.lower().replace(" ", "_")+".html"}, cat) for cat in categories]
                category_html = HTML_wrapper("h3", text = HTML_wrapper("subtitle", text = "Posted in " + ", ".join(category_links)))
            else:
                category_html = ""
            # Generating other details based on information.
            comment_counter = HTML_wrapper("a", {"href":meta.blog_url+str(self.posts[post_num])+".html#disqus_thread", "data-disqus-identifier":str(post_num)}, "Comments")
            comment_html = HTML_wrapper("img", {"width":10, "height":10, "src":meta.media_dir+"speech_bubble.png"}) + " " + comment_counter
            subtitle_html = HTML_wrapper("subtitle", text = date_html + " | " + comment_html)
            first_paragraph = ""

            for line in post:
                if line is not "\n":
                    read_more_text = HTML_wrapper("a", {"href":str(post_num)+".html"}, "[" + str(len(post.read().split())) + " more words]")
                    first_paragraph = HTML_wrapper("p", text = line.strip("\n") + " " + read_more_text)
                    break

            return HTML_wrapper("h3", text = [title_html, subtitle_html]) + "\n" + first_paragraph + "\n" + category_html + "\n"

    def get_HTML_page_navigation(self, page_num, current_page_name = "index"):
        """ Returns the HTML navigation tools for this page. """
        assert page_num + 1 <= self.num_pages
        nav_html = []

        # prev_page
        if page_num < self.num_pages - 1:
            nav_html.append(HTML_wrapper("a", {"href":current_page_name + str(page_num + 1) + ".html", "class":"left index"}, "« Older Posts"))
        # next_page
        if page_num > 0:
            nav_html.append(HTML_wrapper("a", {"href":current_page_name + ("" if page_num - 1 == 0 else str(page_num - 1)) + ".html", "class":"right index"}, "Newer Posts »"))

        return HTML_wrapper("smallNav", text = nav_html) + "<br>"

    def write_main(self, template_loc, target_dir):
        """ Generate an HTML file of this index representing the
            current index and formatted like template, and write
            it to the given target directory. """        
        for page in range(self.num_pages):
            html = [self.get_HTML_header()]
            for n in range(page*self.posts_per_page, page*self.posts_per_page + min(len(self.posts) - page*self.posts_per_page, self.posts_per_page)):            
                html.append(self.get_HTML_stub(n))

            # Joining all the top level sections together.
            if self.num_pages > 1:
                html.append(self.get_HTML_page_navigation(page))
            comment_count_script = "\n<script id=\"dsq-count-scr\" src=\"//austingarrett.disqus.com/count.js\" async></script>"
            preview_text = indent(HTML_wrapper("preview", text = html) + comment_count_script)
            aside_text = get_aside()
            html_text = "\n".join([preview_text, aside_text])

            # Writing to the actual file.
            new_index_loc = target_dir + "index" + ("" if page == 0 else str(page)) + ".html"
            shutil.copyfile(template_loc, new_index_loc)
            write_generic(new_index_loc, rel_root_loc = "..", main_flag = html_text, blog_active = True)

    def write_categories(self, template_loc, target_dir):
        """ Generate an HTML file of the category search index
            and formatted like template, and write it to the
            given target directory. """
        for cat in self.categories:
            posts_in_cat = self.filter_posts(cat)
            cat = cat.lower().replace(" ", "_")
            num_pages_cat = len(posts_in_cat) // self.posts_per_page + 1

            for page in range(num_pages_cat):
                html = [self.get_HTML_header()]
                
                for n in range(page*self.posts_per_page, page*self.posts_per_page + min(len(posts_in_cat) - page*self.posts_per_page, self.posts_per_page)):
                    html.append(self.get_HTML_stub(self.posts[posts_in_cat[n]]))

                # Joining all the top level sections together.
                if num_pages_cat > 1:
                    html.append(self.get_HTML_page_navigation(page, cat))
                comment_count_script = "\n<script id=\"dsq-count-scr\" src=\"//austingarrett.disqus.com/count.js\" async></script>"
                preview_text = indent(HTML_wrapper("preview", text = html) + comment_count_script)
                aside_text = get_aside()
                html_text = "\n".join([preview_text, aside_text])

                # Writing to the actual file.
                new_index_loc = target_dir + cat + ("" if page == 0 else str(page)) + ".html"
                shutil.copyfile(template_loc, new_index_loc)
                write_generic(new_index_loc, rel_root_loc = "..", main_flag = html_text, blog_active = True)

def generate_blog_index():
    """ Interface for the main method. """
    my_index = Index(meta.content_dir, meta.posts_dir, meta.index_posts_per_page)
    my_index.write_main(meta.template_loc, meta.index_dir)
    my_index.write_categories(meta.template_loc, meta.index_dir)
