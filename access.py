from facebook_scraper import get_posts
import pandas as pd
import time
from datetime import date

# params
today = date.today()
n_pages = 49 # number of pages; for testing
n_posts = 1 # number of posts per page 

# setting up log
log = pd.DataFrame()
log_filename = str(today) + '-error-log.txt'
log.to_csv(log_filename)

# reading data with page names
district_data = pd.read_csv("facebook-accounts-from-district-homepages.csv")

# using just the link variable,
links_of_district_accounts = district_data['link'][0:n_pages]

# accessing page information
for page_name in links_of_district_accounts:

    print('accessing ', page_name)
    
    try:

        page = pd.DataFrame()

        for post in get_posts(page_name, pages = n_posts):
            page['post_id'] = post['post_id'],
            page['text'] = post['text'],
            page['time'] = post['time'],
            page['likes'] = post['likes'],
            page['comments'] = post['comments'],
            page['shares'] = post['shares'],
            page['post_url'] = post['post_url'],
            page['link'] = post['link']

        page_filename = 'data/' + page_name + '.csv'

        page.to_csv(page_filename)

    except:

        # logging errors
        log = pd.read_csv(log_filename)
        new_row = {"page": page_name}
        log.append(new_row)
        log.to_csv(log_filename)

        print('timeout error for ' + str(page_name))

    # because this involves web-scraping
    time.sleep(2.5)