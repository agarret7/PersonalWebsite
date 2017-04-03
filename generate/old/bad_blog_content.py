import os
import shutil
from meta import web_url

def generate_blog_content():
    cwd_files = sorted(os.listdir("../content/posts/"), key = lambda x: float(x.strip(".txt.")))
    
    for n, filename in enumerate(cwd_files):
        content = ["<article>", "  <smallNav>"]

        # Appending navigation to previous and next page.
        prev_page = ""
        next_page = ""
        
        if n > 0:
            with open("../content/posts/" + cwd_files[n - 1], "r") as prev_post:
                prev_page = "    <a href=\"" + str(int(filename.strip(".txt")) - 1) + ".html\" class=\"left\">" + \
                            "« <div class=\"main\">" + prev_post.readline().strip("\n") + "</div></a>"
            content.append(prev_page)
        if n < len(cwd_files)-1:
            with open("../content/posts/" + cwd_files[n + 1], "r") as next_post:
                next_page = "    <a href=\"" + str(int(filename.strip(".txt")) + 1) + ".html\" class=\"right\">" + \
                             "<div class=\"main\">" + next_post.readline().strip("\n") + "</div> »</a>"
            content.append(next_page)

        content.append("  </smallNav>")
        
        with open("../content/posts/" + filename, "r") as source:
            comments_count_text = " | <img width=\"10\" height=\"10\" src=\"../backend/media/speech_bubble.png\"></img>" + \
                                  " <a href=\"" + web_url + "blog/" + filename.strip(".txt") + ".html#disqus_thread\"" + \
                                  " data-disqus-identifier=\"" + filename.strip(".txt") + "\">Comments</a>"

            # Title and date.
            content.append("  <h2>" + source.readline().strip("\n") + "<br>")
            content.append("  <subtitle><img width=\"10\" height=\"10\" src=\"../backend/media/clock.png\"></img> " + source.readline().strip("\n") + \
                           comments_count_text + "</subtitle></h3>")

            # Post body
            for line in source:
                if line is not "\n":
                    content.append("  <p>" + line.strip("\n") + "</p>")
        
        # Share buttons
        with open("../share.html", "r") as share:
            for line in share:
                if line is not "\n":
                    content.append("  " + line.strip("\n"))

        comments_text = [""]
        with open("../comments.html") as comments:
            for line in comments:
                if line is not "\n":
                    comments_text.append("  " + line.strip("\n"))

        comments_text.append("</article>")
        # Formating for HTML template
        content = ("\n\n" + 6*" ").join(content)
        comments_text = ("\n" + 6*" ").join(comments_text)
        shutil.copyfile("../template.html", "../../blog/" + filename.strip(".txt") + ".html")

        # Write to HTML file in website
        with open("../../blog/" + filename.strip(".txt") + ".html", "r+") as target:
            template = target.read()
            comments_html = comments_text.format(post_number = filename.strip(".txt"))
            blog_html = template.format(rel_root_loc = '..', article_flag = content,
                                        preview_flag = '', aside_flag = '',
                                        blog_active = "active", contact_active = '',
                                        comments_flag = comments_html)
            # Erase and overwrite
            target.seek(0)
            target.truncate()
            target.write(blog_html)
