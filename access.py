from facebook_scraper import get_posts
import pandas as pd

district_data = pd.read_csv("facebook-accounts-from-district-homepages.csv")

links_of_district_accounts = district_data['link'][1:50]

for i in links_of_district_accounts:

    p = pd.DataFrame({
        "post_id": 'NA',
        "text": 'NA',
        "time": 'NA',
        "likes": 'NA',
        "comments": 'NA',
        "shares": 'NA',
        "post_url":'NA',
        "link":'NA'}, index=[0])

    for post in get_posts('knoxschools', pages=50):
        p['post_id'] = post['post_id'],
        p['text'] = post['text'],
        p['time'] = post['time'],
        p['likes'] = post['likes'],
        p['comments'] = post['comments'],
        p['shares'] = post['shares'],
        p['post_url'] = post['post_url'],
        p['link'] = post['link']

    f = links_of_district_accounts[i] + '.csv'

    p.to_csv(f, index=False)
