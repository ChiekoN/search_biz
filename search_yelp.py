# Open Top page of yelp, search location = "Perth Western Australia" and Category = "Restaurants".

import time
import os
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

def crawl_main_list(top_url):

    rest_selector = 'li.regular-search-result'
    rest_name_selector = 'h3.search-result-title > span.indexed-biz-name > a.biz-name.js-analytics-click > span'
    rest_genre_selector = 'div.price-category > span.category-str-list > a'
    rest_secondary_selector = 'div.secondary-attributes'
    rest_area_selector = 'span.neighborhood-str-list'
    rest_address_selector = 'address'
    rest_phone_selector = 'span.biz-phone'

    session = HTMLSession()
    req = session.get(top_url)

    top_list = req.html.find(rest_selector)

    # Take information of restaurants from Main Page
    for a_rest in top_list:
        rest_name = a_rest.find(rest_name_selector, first = True).text
        rest_genre_list = [ rest_genre.text for rest_genre in a_rest.find(rest_genre_selector)]
        rest_area = a_rest.find(rest_secondary_selector, first = True).find(rest_area_selector, first = True).text
        rest_address = a_rest.find(rest_secondary_selector, first = True).find(rest_address_selector, first = True).text.replace('\n', ', ')
        rest_phone = a_rest.find(rest_secondary_selector, first = True).find(rest_phone_selector, first = True).text

        # Set information to rest_list.
        rest_list[rest_name] =  { 'genre' : rest_genre_list,
                                  'area' : rest_area,
                                  'address' : rest_address,
                                  'phone' : rest_phone
                                }
    # Pick up 'next page' link
    next_selector = 'a.u-decoration-none.next.pagination-links_anchor'
    next_link_element = req.html.find(next_selector, first = True)
    if next_link_element :
        # next_link_element.absolute_links is set object,
        # so return that one item as a text using min().
        return min(next_link_element.absolute_links)
    else:
        return ''


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
