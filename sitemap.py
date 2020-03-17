import requests
from urllib.parse import urlparse, urljoin
import concurrent.futures
from bs4 import BeautifulSoup

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
foramtter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
file_handler = logging.FileHandler('errors_data.log')
file_handler.setFormatter(foramtter)
logger.addHandler(file_handler)


# This is a class that generate sitemap dict
class SiteMap:

    def __init__(self, url):
        self.url = url
        self._download_queue = [url]
        self._total_pages = []
        self.parent_children = {}

    def is_same_domain(self, url_check):
        print(urlparse(self.url).netloc)
        scheme, netloc, path, params, query, fragment = urlparse(url_check)
        # https://vk.com/proxyseller.netloc == vk.com
        # /privacy.netloc == ''
        # /privacy.schema == ''
        # Check invalid schema like "live:.cid.fc79c22e74567bb3"

        # function check if url is not empty, netloc is either empty or is internal like https://vk.com/proxyseller
        # and schema in ['http', 'https', '']
        if url_check != '' and netloc in ['', urlparse(self.url).netloc] and scheme in ['http', 'https', '']:
            # print(url_check)
            return True

    # Try to access pages except some Error arises
    @staticmethod
    def get_content(url):
        try:
            source = requests.get(url, stream=True)
        # exceptions which might arise
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError,
                requests.exceptions.InvalidURL,
                requests.exceptions.InvalidSchema, requests.exceptions.ReadTimeout) as e:
            logger.warning(f'{url} unable to access due to {e}')
            return None
        # check if  url is html page
        content_type = source.headers.get('content-type')
        if source.status_code == 200:
            if 'text/html' in content_type:
                return source.content
        return None

    def search_links(self, page_content, base_url):
        result = []
        # soap = <!DOCTYPE html>
        # <html lang="en">
        # <head>
        #     <title>Title</title>
        # </head>
        # <body>
        #   <a> href = "https://vk.com/cbr/" </a>
        #   <a> href = "https://scrapethissite.com/" </a>
        # </body>
        # </html>
        soap = BeautifulSoup(page_content, 'lxml')

        for anchor_link in soap.find_all('a'):

            # href might be either full link like href==https://vk.com/proxyseller/privacy
            #  or relative one line href==/privacy
            href = anchor_link.get('href')
            if self.is_same_domain(href):
                # print(href)
                # after check might be either
                # full: https://proxy-seller.ru/blog/parser_datacol_dlya_seo-specialistov
                # of relative: /bulgarian-proxy

                # Examples :
                #  href=/reception/
                #  base_url = https://www.cbr.ru/
                #  abs_url =  https://www.cbr.ru/reception/
                abs_url = urljoin(base_url, urlparse(href).path)
                result.append(abs_url)
        return result

    def parser(self, url_requested):
        # print(f'{url_requested} is in process')
        # starting the queue of urls'
        # first url is the website
        # for which sitemap need to be build
        page_content = self.get_content(url_requested)
        if page_content is None:
            # delete from queue page with content equal to None
            # remove provide thread safe operation
            self._download_queue.remove(url_requested)
        # links_found is a list of all url founded in the parsed page
        links_found = self.search_links(page_content, url_requested)
        # print(links_found)
        # check if requested url has been already parsed
        if url_requested not in self.parent_children:
            self.parent_children[url_requested] = []
        for link_rel in links_found:

            # check if page have been already parsed to exclude doubles in self._parent_pages as well
            if link_rel not in self._total_pages and link_rel not in self.parent_children:
                # append to a queue list and to a all pages of a site
                self._download_queue.append(link_rel)
                self._total_pages.append(link_rel)
                # form connection between parent and children
                self.parent_children[url_requested].append(link_rel)
        # delete from queue page which has been checked
        # remove provide thread safe operation
        self._download_queue.remove(url_requested)
        return True

    # concurrently parse pages
    def crawler(self):
        while len(self._download_queue) > 0:
            with concurrent.futures.ThreadPoolExecutor(max_workers=32) as executor:
                # map thread to url in download_queue
                executor.map(self.parser, self._download_queue)
        # delete links which has no children links
        for parent_link in list(self.parent_children):
            if not len(self.parent_children[parent_link]):
                self.parent_children.pop(parent_link)
        return True


# start_point = https://scrapethissite.com/
def traverse_breadth(structure, start_point):
    # yield main url of a structure
    yield start_point
    # structure[start] = ['https://scrapethissite.com/pages/', 'https://scrapethissite.com/lessons/',...]
    page_nodes = structure[start_point]
    while len(page_nodes) > 0:
        # pages we will get after parsing structure[start]
        next_pages = []
        for page in page_nodes:
            yield page
            next_pages.extend(structure.get(page, []))
        page_nodes = next_pages
