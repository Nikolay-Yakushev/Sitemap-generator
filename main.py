#!/usr/bin/env/python3.8
import sys

if __name__ == '__main__':
    from sitemap import SiteMap, traverse_breadth
    import db

    url = sys.argv[1]  #'https://scrapethissite.com/'
    # creating sitemap object
    sitemap = SiteMap(url)
    table_name = 'urls'
    result = sitemap.crawler()
    # print when all pages are downloaded
    if result:
        print("Downloaded")
    # using generator to walk traverse urls in breadth
    url_structure = traverse_breadth(sitemap.parent_children, url)

    # traverse breadth
    for url in url_structure:
        print(url)
    # delete from db table if it has been created recently
    db.delete_table(table_name)
    for url_parent, links_children in sitemap.parent_children.items():
        for url_child in links_children:
            # writing to db
            db.write_db(table_name, url_parent, url_child)

