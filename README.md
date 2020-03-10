# Sitemap-generator

this is a Sitemap generator 

Python Site Map Generator uses python multi-threaded approach to read all links accessible through the Web site and generate proper
sitemap for SEO purposes. Script was meant to use threading technology to allow easy and very fast approach while generating sitemaps for your Web pages.
The script will run under Linux operating system which supports Python 3 language.


Usage example:

Input:

    python3.8 main.py 'https://scrapethissite.com/'
    
python output(tarverse breadth):

    https://scrapethissite.com/
    https://scrapethissite.com/pages/
    https://scrapethissite.com/lessons/
    https://scrapethissite.com/faq/
    https://scrapethissite.com/login/
    https://scrapethissite.com/pages/simple/
    https://scrapethissite.com/pages/forms/
    https://scrapethissite.com/pages/ajax-javascript/
    https://scrapethissite.com/pages/frames/
    https://scrapethissite.com/pages/advanced/
    https://scrapethissite.com/robots.txt

PostgreSQL database output:

    rest_db=# select * from urls;
                url_parent             |                     url_child                     
    -----------------------------------+---------------------------------------------------
     https://scrapethissite.com/       | https://scrapethissite.com/pages/
     https://scrapethissite.com/       | https://scrapethissite.com/lessons/
     https://scrapethissite.com/       | https://scrapethissite.com/faq/
     https://scrapethissite.com/       | https://scrapethissite.com/login/
     https://scrapethissite.com/faq/   | https://scrapethissite.com/robots.txt
     https://scrapethissite.com/pages/ | https://scrapethissite.com/pages/simple/
     https://scrapethissite.com/pages/ | https://scrapethissite.com/pages/forms/
     https://scrapethissite.com/pages/ | https://scrapethissite.com/pages/ajax-javascript/
     https://scrapethissite.com/pages/ | https://scrapethissite.com/pages/frames/
     https://scrapethissite.com/pages/ | https://scrapethissite.com/pages/advanced/
   
