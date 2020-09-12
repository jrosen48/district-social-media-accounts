import twint
import pandas as pd
import time
import timestring
from datetime import datetime

# reading data with page names
district_data = pd.read_csv("twitter-accounts-from-district-homepages.csv")

# params
pages_to_access = 200
posts_per_page = 100
first_date_we_want = datetime(year = 2020, month = 3, day = 1)

for i in range(0, pages_to_access):

	# setting up 
	username = district_data['username'][i]
	output_filename = "twitter-data/" + str(username) + ".csv"

	c = twint.Config()
	c.Limit = posts_per_page
	c.Store_csv = True
	c.Output = output_filename
	c.Username = str(username)

	# running
	twint.run.Search(c)

	print("accessed data for " + str(username))
	# print("last date was: ", str(output['date'][len(output) - 1]))
	print("now, I take a long rest")
	time.sleep(30)

	# # grabbing output and checking dates
	# output = pd.read_csv(output_filename)

	# output['date'] = [timestring.Date(i) for i in output['date']]

	# print(any(output['date'] <= first_date_we_want))

	# if any(output['date'] <= first_date_we_want):

	# 	print("accessed " + str(len(output)) + ' rows for ' + str(username))
	# 	print("last date was: ", str(output['date'][len(output) - 1]))
	# 	print("now, I rest for a short while")
	# 	time.sleep(10)

	# else:
		
	# 	print('uh oh, need more!')

	# 	c.Limit = pages_to_access * 2.5
	# 	twint.run.Search(c)

	# 	print("accessed " + str(len(output)) + ' rows for ' + str(username))
	# 	print("last date was: ", str(output['date'][len(output) - 1]))

	# 	output = pd.read_csv(output_filename)
	# 	output['date'] = [timestring.Date(i) for i in output['date']]

	# 	if any(output['date'] <= first_date_we_want):

	# 		print("accessed " + str(len(output)) + ' rows for ' + str(username))
	# 		print("last date was: ", str(output['date'][len(output) - 1]))
	# 		print("now, I rest for a bit longer")
	# 		time.sleep(20)

	# 	else:
			
	# 		print('uh oh, need more!')
	# 		c.Limit = pages_to_access * 5s
	# 		twint.run.Search(c)
	# 		print("accessed " + str(len(output)) + ' rows for ' + str(username))
	# 		print("last date was: ", str(output['date'][len(output) - 1]))
	# 		print("now, I take a long rest")
	# 		time.sleep(30)
