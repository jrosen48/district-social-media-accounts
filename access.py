from facebook_scraper import get_posts
import pandas as pd
import time
import datetime
import timestring
from datetime import date, datetime
import os.path
from os import path

# params
today = date.today()
n_fb_pages_start = 1 # number of FB pages to download data for; for testing
n_fb_page_end = 4999
n_pages_to_iterate = 100 # number of pages to scrape within one FB page
log_filename = 'logs/' + str(today) + '-error-log-running-all-first-half.txt'

# reading data with page names
district_data = pd.read_csv("facebook-accounts-from-district-homepages.csv")

# using just the link variable,
links_of_district_accounts = district_data['link_proc'][n_fb_pages_start:n_fb_page_end]

# accessing page information
for page_name in links_of_district_accounts:

    page_filename = 'data/' + str(page_name) + '.csv'

    if path.exists(page_filename):

        print('already exists, skipping: ' + page_filename)

    else:
    
        print('accessing ', str(page_name), ' at ', str(datetime.now()))
        
        try:

            page = pd.DataFrame()

            for post in get_posts(str(page_name), pages = n_pages_to_iterate): # extra info gets reactions

                page = page.append(post, ignore_index = True)

            page['time'] = [timestring.Date(i) for i in page['time']]

            first_date_we_want = datetime(year = 2020, month = 3, day = 1)

            if any(page['time'] <= first_date_we_want):

                print("accessed " + str(len(page)) + ' rows')

                page.to_csv(page_filename)

            else:

                print("accessed " + str(len(page)) + " rows, but zero rows before 2020-03-01; accessing more")

                # this is janky and should be recursive, but it will help for a first pass

                page = pd.DataFrame()

                for post in get_posts(str(page_name), pages = n_pages_to_iterate * 2): # extra info gets reactions

                    page = page.append(post, ignore_index = True)

                print("accessed " + str(len(page)) + ' rows')

                page.to_csv(page_filename)

                log_file = open(log_filename, "a")
                log_file.writelines(str(page_name) + ' - incomplete')
                log_file.writelines('\n')
                log_file.close()

                print('incomplete search for ' + str(page_name))

        except BaseException as e:
            print(e)

            # logging errors
            log_file = open(log_filename, "a")
            log_file.writelines(str(page_name) + ' - attempt to get posts failed')
            log_file.writelines('\n')
            log_file.close()

            print('timeout error for ' + str(page_name))

    # because this involves web-scraping
    time.sleep(29)

# checking_df = pd.read_csv("data/acsbulldogs.csv")