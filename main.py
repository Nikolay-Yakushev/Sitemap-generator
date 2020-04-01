import sys
import argparse

if __name__ == '__main__':
    from sitemap import SiteMap, traverse_breadth
    import db

    parser = argparse.ArgumentParser(description='Sitemap generator')
    parser.add_argument('-u', '--url', help="Try this: python3 main.py -u=https://scrapethissite.com/", type=str)
    args = parser.parse_args()
    url = args.url
    # 'https://proxy-seller.ru/'

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
    db.delete_table(table_name)

    # executemany method added
    db.write_db(table_name, sitemap_first.parent_children)
