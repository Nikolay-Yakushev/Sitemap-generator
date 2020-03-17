#!/usr/bin/env python3.8
import sys

if __name__ == '__main__':
    from sitemap import SiteMap, traverse_breadth
    import db

<<<<<<< HEAD
    url = sys.argv[1]
        #'https://proxy-seller.ru/'
=======
    url = sys.argv[1] 
    #'https://proxy-seller.ru/'
>>>>>>> 0803d802a4aa0a185550952a75e9351536e51f7d
    # examples to test:
    # 1) https://scrapethissite.com/
    # 2) https://proxy-seller.ru/
    # 3) https://yandex.ru/

    # creating sitemap object
    sitemap_first = SiteMap(url)
    table_name = 'urls'
    result = sitemap_first.crawler()
    # print when all pages are downloaded
    if result:
        print("Downloaded")
    # using generator to traverse urls in breadth
    url_structure = traverse_breadth(sitemap_first.parent_children, url)
    # traverse breadth
    for url in url_structure:
        print(url)

    # delete table (uncomment if necessary)
    #db.delete_table(table_name)

    # executemany method added
    db.write_db(table_name, sitemap_first.parent_children)
