from facebook_scraper import get_posts
import pandas as pd
import time
import datetime
import timestring
from datetime import date
from datetime import datetime
import os.path
from os import path

# params
today = date.today()
n_fb_pages = 50 # number of FB pages to download data for; for testing
n_pages_to_iterate = 50 # number of pages to scrape within one FB page
log_filename = 'logs/' + str(today) + '-error-log.txt'

# reading data with page names
district_data = pd.read_csv("facebook-accounts-from-district-homepages.csv")

# using just the link variable,
links_of_district_accounts = district_data['link_proc'][0:n_fb_pages]

# accessing page information
for page_name in links_of_district_accounts:

    page_filename = 'data/' + page_name + '.csv'

    if path.exists(page_filename):

        print('already exists, skipping: ' + page_filename)

    else:
    
        print('accessing ', page_name, ' at ', str(datetime.now()))
        
        try:

            page = pd.DataFrame()

            for post in get_posts(page_name, pages = n_pages_to_iterate, extra_info = True): # extra info gets reactions

                try: 
                     # sometimes, these don't exist
                    post['reactions'] = str(post['reactions']) # otherwise this causes the df to 'explode' since it's a dict
                    page = page.append(post, ignore_index = True)

                except:
                    page = page.append(post, ignore_index = True)

            p['time'] = [timestring.Date(x) for x in p['time']]

            first_date_we_want = datetime(year = 2020, month = 3, day = 1)

            if any(p['time']) <= first_date_we_want:

                print("accessed " + len(page) + ' rows')

                page.to_csv(page_filename)

            else:

                print("accessed " + len(page) + ' rows, but none before 2020-03-01; accessing more')

                # this is janky and should be recursive, but it will help for a first pass

                for post in get_posts(page_name, pages = n_pages_to_iterate, extra_info = True): # extra info gets reactions

                    try: 
                         # sometimes, these don't exist
                        post['reactions'] = str(post['reactions']) # otherwise this causes the df to 'explode' since it's a dict
                        page = page.append(post, ignore_index = True)

                    except:
                        page = page.append(post, ignore_index = True)

        except:

            # logging errors
            log_file = open(log_filename, "a")
            log_file.writelines(page_name)
            log_file.writelines('\n')
            log_file.close()

            print('timeout error for ' + str(page_name))

    # because this involves web-scraping
    time.sleep(2.5)

# checking_df = pd.read_csv("data/acsbulldogs.csv")