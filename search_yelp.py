# Open Top page of yelp, search location = "Perth Western Australia" and Category = "Restaurants".

import time
import os
from urllib.parse import unquote
from requests_html import HTMLSession

# List all the restaurant into the file
# dictionary:
#  - Name of the restaurant
#  -- Genre
#  -- Area
#  -- Address
#  -- Phone number
#  -- Website (optional)
#  -- Message the business (optional)
rest_list = dict()


def element_link(element_obj):
    ''' Return a link taken from the element.
        element_obj.absolute_links is a Set object. It's supposed to contain only one item,
        or no object if there's no link in the element.
        Take an item (string of URL) from Set object by min().
    '''
    if element_obj :
        return min(element_obj.absolute_links)
    else :
        return ''

def get_website_url(url_element) :
    ''' Get URL from url_element, which is supposed to have <a> in it.
        If url_element is empty, return ''.
    '''

    if not url_element :
        return ''

    web_url = unquote(url_element.find('a', first = True).attrs['href'])
    if 'url=' in web_url :
        web_url = web_url[web_url.find('url=')+4 : web_url.find('&')]

    return web_url

def each_rest_page(each_url):
    ''' Open individual page of restaurants specified by 'url' and get information.
        Return a dictionary containing 'web', 'message', 'reservation'.
    '''
    if not each_url : return {}

    each_session = HTMLSession()
    each_req = each_session.get(each_url)

    website_url = get_website_url(each_req.html.find('span.biz-website.js-biz-website.js-add-url-tagging', first = True))
    print('website : {}'.format(website_url), flush=True)
    return {'website' : website_url}

def crawl_main_list(top_url):
    ''' Get the list of businesses from Main page of Yelp.
        top_url : URL to open and crawl.
    '''
    session = HTMLSession()
    req = session.get(top_url)

    top_list = req.html.find('li.regular-search-result')

    # Take information of restaurants from Main Page
    for a_rest in top_list:
        time.sleep(5)
        # Go to the link to the individual restaurant page.
        # Get the restaurant's website, message, reservation values by Dict.
        rest_page_info = each_rest_page(element_link(a_rest.find('h3.search-result-title > span.indexed-biz-name', first = True).find('a.biz-name.js-analytics-click', first = True)))

        # Get this restaurant's information and set them to Dict.
        rest_name = a_rest.find('h3.search-result-title > span.indexed-biz-name > a.biz-name.js-analytics-click > span', first = True).text
        rest_genre_list = [ rest_genre.text for rest_genre in a_rest.find('div.price-category > span.category-str-list > a')]
        rest_area = a_rest.find('div.secondary-attributes', first = True).find('span.neighborhood-str-list', first = True).text
        rest_address = a_rest.find('div.secondary-attributes', first = True).find('address', first = True).text.replace('\n', ', ')
        rest_phone = a_rest.find('div.secondary-attributes', first = True).find('span.biz-phone', first = True).text

        # Set information to rest_list.
        rest_list[rest_name] =  { 'genre' : rest_genre_list,
                                  'area' : rest_area,
                                  'address' : rest_address,
                                  'phone' : rest_phone,
                                  'website' : rest_page_info['website']
                                }



    # Return 'next page' link
    return element_link(req.html.find(
                'a.u-decoration-none.next.pagination-links_anchor', first = True))

def main():

    # Search on Yelp by 'Bayswater', 'within 2km'
    url = 'https://www.yelp.com.au/search?find_loc=Bayswater,+Perth+Western+Australia&start=0&l=g:115.90344429,-31.925212481,115.929021835,-31.9033555268'

    cnt = 1
    while url:
        url = crawl_main_list(url)
        print(" --- Page {} finished.".format(cnt), flush=True)

        time.sleep(5)
        cnt = cnt+1
        print("next URL:{}".format(url), flush=True)

    # print dictionary
    for key_rest, info_rest in rest_list.items():
        print("{}  :   {}".format(key_rest, info_rest))

    print("*** {} Bussinesses found ***".format(len(rest_list)))


if __name__ == '__main__':
    main()
