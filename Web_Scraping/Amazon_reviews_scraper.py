import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from config_sandeep import header_amazon,ASIN_list

"""
Verified Purchase Only!
Recent Purchase
"""

ls_ASIN = []

headers  = header_amazon
url = 'https://www.amazon.co.uk/product-reviews'
review_list = []


def get_soup(url):
    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.text,'html.parser')
    return soup

def get_reviews(soup,ASIN):
    reviews = soup.find_all('div',{'data-hook': 'review'})
    try:
        for item in reviews:
            review = {
            'ASIN':ASIN,    
            'Product': soup.title.text.replace('Amazon.co.uk:Customer reviews:','').strip(), 
            'Title' : item.find('a',{'data-hook': 'review-title'}).text.strip(),
            'Helpfulness Rating' : item.find('span',{'data-hook': 'review-voting-widget'}).text.strip().replace('Helpful:','0'),
            'Rating' : float(item.find('i',{'data-hook': 'review-star-rating'}).text.replace('out of 5 stars', '').strip()),
            'Date' : item.find('span',{'data-hook': 'review-date'}).text.replace('Reviewed in the United Kingdom on ', '').replace('Reviewed in the United Kingdom 🇬🇧 on ', '').strip(),
            'Body' : item.find('span',{'data-hook': 'review-body'}).text.replace('\n','').strip(),
            }
            review_list.append(review)
    except:
        pass


for item in ASIN_list:
    for x in range(1,60):
        ASIN = item
        soup = get_soup(f'https://www.amazon.co.uk/product-reviews/{ASIN}/ref=cm_cr_getr_d_paging_btm_prev_1?ie=UTF8&reviewerType=avp_only_reviews&sortBy=recent&pageNumber={x}')
        print(f'getting page:{x}')
        get_reviews(soup,ASIN)
        print(len(review_list))
        if not soup.find('li',{'class': 'a-disabled a-last'}):
            pass
        else:
            break

df = pd.DataFrame(review_list)
df.to_excel('Amazon_Products.xlsx',index=False)

