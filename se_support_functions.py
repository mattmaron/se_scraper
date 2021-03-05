import requests
import json
from bs4 import BeautifulSoup
import re 
import time
import gspread

"""
get_apt_details - pulls details for each apartment
"""
def get_apt_details(url):
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
        'content-type': 'application/json',
        'os': 'web',
        'origin': 'https://streeteasy.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://streeteasy.com/',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,la;q=0.8'}

    url = url
    r = requests.get(url,headers=headers)
    html=str(r.text)
    soup = BeautifulSoup(html, 'html.parser')

    ## meta properties
    description = soup.find("meta",  property="og:description")
    title = soup.find("meta",  property='og:title')
    coordinates = soup.find("meta",  property='ICBM')
    url = soup.find("meta",  property="og:url")

    ## return variables
    title_1=title["content"] if title else "No place name"
    splice=title_1.find("For Rent:")
    title_final=title_1[splice+9:]
    url_1=url["content"] if url else "No url given"

    try:
        description_1=description["content"] 
    
    except:
        description_1='None'
 
    #price scape
    bs=description_1.find('$')
    es=description_1.find('.')
    price=description_1[bs:es]

    ##amen
    divs = soup.find_all('div', {'class' : 'details_info'})
    amens=[]
    for x in divs:
        he=x.get_text()
        he=he.strip()
        if he not in amens:
            amens.append(he) 
        else:
            pass

    #print(title_1,url_1,description_1,price)
    amens_ds=amens[0]
    res = re.sub(r"([0-9]+(\.[0-9]+)?)",r" \1 ", amens_ds).strip()

    #get number of bathrooms
    beds1=res.find("beds")
    rooms1=res.find("rooms")
    baths1=res.find("baths")
    
    beds_num=res[rooms1+5:beds1]
    baths_num=res[beds1+4:]

    ##backyard checker
    divs_backyard = soup.find('div', {'class' : 'Description-block jsDescriptionExpanded'})
    backyard_flag=divs_backyard.find("yard")

    if backyard_flag is not None:
        flag='Possible Backyard'
    else:
        flag="-"
    return title_final,url_1,description_1,price,beds_num,baths_num,amens_ds,flag


"""

pull_listings - pulls listings from the search results page

"""
def pull_listings(listings_url):
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
        'content-type': 'application/json',
        'os': 'web',
        'origin': 'https://streeteasy.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://streeteasy.com/',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,la;q=0.8'}

    url = listings_url
    print(url)
    r = requests.get(url,headers=headers)
    print(r.status_code)
    html=str(r.text)
    soup = BeautifulSoup(html, 'html.parser')

    ### create list of apt links
    links_group=[]
    articles = soup.find_all('h3', {'class' : 'details-title'})
    for article in articles:
        print(article)
        links = article.findAll('a')
        #print(links)
        for a in links:
            details=a['href']
            details=str(details)
            apt_link='https://streeteasy.com'+details
            links_group.append(apt_link)

    return links_group

"""

generate_next_listings_results - generates the next url to pull listings results from 

"""
def get_next_listings_results(listings_url):
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
        'content-type': 'application/json',
        'os': 'web',
        'origin': 'https://streeteasy.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://streeteasy.com/',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,la;q=0.8'}

    url = listings_url
    r = requests.get(url,headers=headers)
    html=str(r.text)
    soup = BeautifulSoup(html, 'html.parser')

    ref_urls = soup.find_all('span', {'class' : 'next'})
    for link in ref_urls:
        links = link.findAll('a')

    # for a in links:
    #     apt_link='https://streeteasy.com'+a['href']
