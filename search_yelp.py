import time
import os
from urllib.parse import unquote
from requests_html import HTMLSession
import search_yelp_tk as sytk
import search_yelp_out as syout
# Open Top page of yelp, search businesses with options,
#  then output the list to a file specified.

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
    if element_obj:
        return min(element_obj.absolute_links)
    else:
        return ''

def get_website_url(url_element):
    ''' Get URL from url_element, which is supposed to have <a> in it.
        If url_element is empty, return ''.
    '''

    if not url_element:
        return ''

    web_url = unquote(url_element.find('a', first = True).attrs['href'])
    if 'url=' in web_url :
        web_url = web_url[web_url.find('url=')+4 : web_url.find('&')]

    return web_url

def have_msg_form(msgf_element):
    ''' Check if the message form or/and reservation form is
        in the indevidual restaurant page.
        Return Tuple : Message form (True/False), Reservation form (True/False)
    '''
    msgf = msgf_element.find('a.js-message-biz')
    return ('Message the business' in [i.text for i in msgf],
            'Request a reservation' in [i.text for i in msgf])

def check_takes_rsrv(sidebar_element):
    ''' Check if there's "Takes Reservation" and 'Yes/No' for it
        in the right sidebar area.
        Return 'Yes', 'No', or '' if there's no information.
    '''
    dd = ''
    for divyw in sidebar_element.find('div.ywidget'):
        if divyw.find('h3', containing='More business info'):
            for dl in divyw.find('dl'):
                if dl.find('dt.attribute-key', containing='Takes Reservations'):
                    dd = dl.find('dd', first=True).text
    return dd

def each_rest_page(e_session, each_url):
    ''' Open individual page of restaurants specified by 'url' and get information.
        Return a dictionary containing 'web', 'message', 'reservation'.
    '''
    if not each_url:
        return {'web' : '', 'message' : False, 'reservation' : False}

    each_req = e_session.get(each_url)

    website_url = get_website_url(each_req.html.find('span.biz-website.js-biz-website.js-add-url-tagging', first = True))
    msg_form, resv_form = have_msg_form(each_req.html.find(
                                        'div.mapbox-text', first=True))

    takes_rsrv = check_takes_rsrv(each_req.html.find(
                                    'div.column.column-beta.sidebar',
                                    first=True))

    print('website : {} , message :{} , reserv : {}, takes_rsrv : {}'.format(website_url, msg_form, resv_form, takes_rsrv), flush=True)

    return {'web' : website_url,
            'message' : msg_form,
            'reservation' : resv_form,
            'takes_rsrv' : takes_rsrv }

def crawl_main_list(session, top_url, indicator):
    ''' Get the list of businesses from Main page of Yelp.
        top_url : URL to open and crawl.
    '''
    req = session.get(top_url)
    print('get return = {} --- {}'.format(req.url, req.reason))
    top_list = req.html.find('li.regular-search-result')

    # Take information of restaurants from Main Page
    for a_rest in top_list:
        time.sleep(5)

        # Get this restaurant's information.
        rest_name = a_rest.find('h3.search-result-title > span.indexed-biz-name > a.biz-name.js-analytics-click > span', first = True).text
        # Genre, Area, Address, Phone
        rest_genre_list = [ rest_genre.text for rest_genre in a_rest.find(
                            'div.price-category > span.category-str-list > a')]

        rest_secondattr = a_rest.find('div.secondary-attributes', first=True)
        # Some businesses don't have area.
        rest_area_elem = rest_secondattr.find('span.neighborhood-str-list', first=True)
        if not rest_area_elem:
            rest_area = ''
        else:
            rest_area = rest_area_elem.text
        # Some businesses don't have <address> tag and
        #       <div class="biz-parent-container"> tag instead.
        rest_address_elem = rest_secondattr.find('address', first=True)
        if not rest_address_elem:
            rest_located = rest_secondattr.find('div.biz-parent-container', first=True)
            if rest_located:
                rest_address = rest_located.text.replace('\n', ', ')
            else:
                rest_address = ''
        else:
            rest_address = rest_address_elem.text.replace('\n', ', ')
        # Some businesses don't have phone number.
        rest_phone_elem = rest_secondattr.find('span.biz-phone', first=True)
        if not rest_phone_elem:
            rest_phone = ''
        else:
            rest_phone = rest_phone_elem.text

        #print("* {}".format(rest_name), flush=True)
        print(str("* {}".format(rest_name).encode(encoding='cp932', errors='replace')), flush=True)

        # Go to the link to the individual restaurant page.
        # Get the restaurant's website, message, reservation values by Dict.
        rest_page_info = each_rest_page(session, element_link(a_rest.find(
                                'h3.search-result-title > span.indexed-biz-name',
                                first=True
                                ).find('a.biz-name.js-analytics-click', first=True)
                                ))

        # Set information to Dict rest_list.
        rest_list[rest_name] =  { 'genre' : rest_genre_list,
                                  'area' : rest_area,
                                  'address' : rest_address,
                                  'phone' : rest_phone,
                                  'web' : rest_page_info['web'],
                                  'message' : rest_page_info['message'],
                                  'reservation' : rest_page_info['reservation'],
                                  'takes_rsrv' : rest_page_info['takes_rsrv']
                                }
        indicator.set_num_to_msg(len(rest_list))

    # Return 'next page' link
    return element_link(req.html.find(
                'a.u-decoration-none.next.pagination-links_anchor', first = True))

def get_within_option(r, option):
    ''' Open the top page, get and return the distance option string
        to be set in URL.
        r : Response object of the top page.
        option : Distance option (within x km).
    '''
    within_list = r.html.find('div.filter-set.distance-filters', first=True).find('li')
    return within_list[option].find('input.radio', first=True).attrs['value']

def main():

    # Search on Yelp
    base_url = 'https://www.yelp.com.au/search'

    opt = sytk.select_option()
    if not opt:
        return

    ind = sytk.create_indicator()
    ind.set_msg('Start crawling...')
    # Specify Area, Keyword(category, genre etc)
    local_area = opt['area']
    search_area = local_area + '+Western+Australia'
    search_keyword = opt['keyword']

    payload = {'find_loc' : search_area, 'find_desc' : search_keyword}
    distance = opt['distance'] # within option

    s = HTMLSession()
    r = s.get(base_url, params=payload)
    within_param = get_within_option(r, distance)

    # assemble URL with specified 'area', 'keyword', and 'distance'
    url = r.url + '&l=' + within_param


    cnt = 1
    while url:
        url = crawl_main_list(s, url, ind)
        print(" --- Page {} finished.".format(cnt), flush=True)
        time.sleep(5)
        cnt = cnt+1
        print("next URL:{}".format(url), flush=True)

        ###########################
        # for the test, limit the data number.
        if cnt > 5:
            break
        #######################

    syout.dict_to_csv(opt['savefile'], rest_list)
    print("*** {} Bussinesses found ***".format(len(rest_list)))


if __name__ == '__main__':
    main()
