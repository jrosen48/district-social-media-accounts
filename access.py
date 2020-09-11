from facebook_scraper import get_posts
import pandas as pd
import time

district_data = pd.read_csv("facebook-accounts-from-district-homepages.csv")

links_of_district_accounts = district_data['link'][0:50]

for page_name in links_of_district_accounts:

    print('accessing ', page_name)
    p = pd.DataFrame({
        "post_id": 'NA',
        "text": 'NA',
        "time": 'NA',
        "likes": 'NA',
        "comments": 'NA',
        "shares": 'NA',
        "post_url":'NA',
        "link":'NA'}, index=[0])

    for post in get_posts(page_name, pages=3):
        p['post_id'] = post['post_id'],
        p['text'] = post['text'],
        p['time'] = post['time'],
        p['likes'] = post['likes'],
        p['comments'] = post['comments'],
        p['shares'] = post['shares'],
        p['post_url'] = post['post_url'],
        p['link'] = post['link']

    f = 'data/' + page_name + '.csv'

    try:
        p.to_csv(f)
    except:
        print('timeout error for ' + page_name)

    time.sleep(2.5)