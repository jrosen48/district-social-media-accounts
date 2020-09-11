from facebook_scraper import get_posts
import pandas as pd
import time
import datetime
from datetime import date
from datetime import datetime

# params
today = date.today()
n_fb_pages = 50 # number of FB pages to download data for; for testing
n_pages_to_iterate = 25 # number of pages to scrape within one FB page
log_filename = 'logs/' + str(today) + '-error-log.txt'

# reading data with page names
district_data = pd.read_csv("facebook-accounts-from-district-homepages.csv")

# using just the link variable,
# links_of_district_accounts = district_data['link_proc'][0:n_fb_pages]
links_of_district_accounts = ['knoxschools', 'clay-county-board-of-education']

# accessing page information
for page_name in links_of_district_accounts:

    print('accessing ', page_name, ' at ', str(datetime.now()))
    
    try:

        page = pd.DataFrame()

        for post in get_posts(page_name, pages = n_pages_to_iterate, extra_info = True): # extra info gets reactions

            post['']

            try: 
                 # sometimes, these don't exist
                post['reactions'] = str(post['reactions']) # otherwise this causes the df to 'explode' since it's a dict
                page = page.append(post, ignore_index = True)
            except:
                page = page.append(post, ignore_index = True)

        page_filename = 'data/' + page_name + '.csv'

        page.to_csv(page_filename)

    except:

        # logging errors
        log_file = open(log_filename, "a")
        log_file.writelines(page_name)
        log_file.writelines('\n')
        log_file.close()

        print('timeout error for ' + str(page_name))

    # because this involves web-scraping
    time.sleep(2.5)