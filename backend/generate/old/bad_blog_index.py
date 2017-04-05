import os
import shutil
from aside import *
from meta import web_url

def generate_blog_index():

    post_files = list(reversed(sorted(os.listdir("../content/posts/"), key = lambda x: float(x.strip(".txt")))))
    num_posts_per_page = 10
    num_index_pages = len(post_files) // num_posts_per_page + 1

    tag_dict = {}

    # For each index page...
    for p in range(num_index_pages):
        content = ["<preview>"]
        content = append_header(content)
        content, tag_dict = append_article_stubs(content, p, num_posts_per_page, post_files, tag_dict)
        if num_index_pages > 1:
            content = append_page_navigation(content, p, num_index_pages)
        content.append("</preview>")

        # Script to get comment counts working.
        comment_count_script = "<script id=\"dsq-count-scr\" src=\"//austingarrett.disqus.com/count.js\" async></script>"
        content.append(comment_count_script)
        
        # Formating for HTML template
        content = ("\n" + 6*" ").join(content)
        shutil.copyfile("../template.html", "../../blog/index" + ("" if p == 0 else str(p)) + ".html")

        # Write to HTML file in website
        with open("../../blog/index" + ("" if p == 0 else str(p)) + ".html", "r+") as target:
            template = target.read()
            aside_text = get_aside().format(rel_root_loc = "..")
            blog_html = template.format(rel_root_loc = '..', article_flag = '',
                                        preview_flag = content, aside_flag = aside_text,
                                        blog_active = "active", contact_active = '',
                                        comments_flag = '')

            # Erase and overwrite
            target.seek(0)
            target.truncate()
            target.write(blog_html)

def append_header(content):
    # Parsing in blog title and pretty stuff.
    with open("../content/blog_index.html") as title:
        for line in title:
            if line is not "\n":
                content.append("  " + line.strip("\n"))

        # Spacing for the header.
        content.append("")

    return content

def append_article_stubs(content, page_number, num_posts_per_page, post_files, tag_dict):
    # For the 10 posts on this index page...
    for n in range(page_number*num_posts_per_page, page_number*num_posts_per_page + min(len(post_files) - page_number*num_posts_per_page, num_posts_per_page)):
        post_num = post_files[n].strip(".txt")
        # Auto-generated article stubs.
        with open("../content/posts/" + post_files[n], "r") as source:
            comments_count_text = " | <img width=\"10\" height=\"10\" src=\"../backend/media/speech_bubble.png\"></img>" + \
                                  " <a href=\"" + web_url + "blog/" + post_num + ".html#disqus_thread\"" + \
                                  " data-disqus-identifier=\"" + post_num + "\">Comments</a>"
            # Title, date, and stub.
            content.append("  <h3><a href=\"" + post_num + ".html\">" + source.readline().strip("\n") + "</a><br>")
            content.append("  <subtitle><img width=\"10\" height=\"10\" src=\"../backend/media/clock.png\"></img> " + source.readline().strip("\n") + \
                           comments_count_text + "</subtitle></h3>")
            tags = source.readline().split(", ")

            for tag in tags:
                if tag not in tag_dict.keys():
                    tag_dict[tag] = set(post_num)
                else:
                    tag_dict[tag].add(post_num)

            for line in source:
                if line is not "\n":
                    read_more_text = " <a href=\"" + post_num + ".html\">" + "[" + str(len(source.read().split())) + " more words]</a>"
                    content.append("  <p>" + line.strip("\n") + read_more_text + "</p>\n")
                    break

            tag_links = ["<a href=\"" + tag.lower().replace(" ", "_") + ".html\">" + tag + "</a>" for tag in tags]
            tag_text = "Posted in " + ', '.join(tag_links)
            content.append("  <h3><subtitle>" + tag_text + "</subtitle></h3>")
            
    return content, tag_dict

def append_page_navigation(content, page_number, num_pages):
    content.append("  <smallNav>")
    # Appending navigation to previous and next page.
    prev_page = ""
    next_page = ""

    # prev_page
    if page_number < num_pages - 1:
        prev_page = "    <a href=\"index" + str(page_number + 1) + ".html\" class=\"left index\">« Older Posts</a>"
        content.append(prev_page)
    # next_page
    if page_number > 0:
        next_page = "    <a href=\"index" + ("" if page_number-1 == 0 else str(page_number - 1)) + ".html\" class=\"right index\">Newer Posts »</a>"
        content.append(next_page)

    content.append("  </smallNav><br>")

    return content
