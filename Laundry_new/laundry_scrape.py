import urllib, json
from bs4 import BeautifulSoup
from urllib.request import urlopen
#from pandas import json
import time

laundry_id = {
    "ALLEN49": 589877048,
    "101DRYERS": 589877054,
    "103WASHERS": 589877017,
    "ROOM8": 589877019,
}

url_laundry_id="http://api.laundryview.com/room/?api_key=o1cc9fc66e519404f25c5e2fb6571632&method=getNumAvailable&location="

def get_laundry_id(laundry_name):
    return laundry_id[laundry_name]

def get_laundry(laundry):
	
	results = []
	url = url_laundry_id + str(laundry)
	#response = urlopen(url)
	#print(response)
	request = urlopen(url)
	soup = BeautifulSoup(request, 'html.parser')
	washers = soup.find_all('washer') 
	dryers = soup.find_all('dryer') 
	#print(washer.text)
	for washer in washers:
		washer_value = washer.text
	results.append(washer_value)
	for dryer in dryers:
		dry_value = dryer.text
	results.append(dry_value)
	return results
	#washer_cnt = washer.contents.string
	#print(washer_cnt)

def scrape():
	current_time = time.localtime()
	today = time.strftime('%Y-%-m-%-d-%Hh-%Mm-%Ss', current_time)
	print(today)
	request = urlopen('http://wmon.cites.illinois.edu/listbuilding.html')
	soup = BeautifulSoup(request, 'html.parser')
	table = soup.find_all('table')[1] # Grab the 2 table
	retval = []
	for x in table.find_all('tr'):
    		ret = {}
    		ret['buildingnumber'] = x.contents[1].string
    		ret['buildingname'] = x.contents[3].string
    		if (x.contents[5] is None):
        		ret['totalAP'] = None
    		else:
        		ret['totalAP'] = x.contents[5].string
    		if (x.contents[11] is None):
        		ret['clientdevices'] = None
    		else:
        		ret['clientdevices'] = x.contents[11].string
    		retval.append(ret)
	#return retval
	finalreturn = {}
	#finalreturn['data'] = scrape()
	finalreturn['data'] = retval[1:]
	#finalreturn['data'] = retval
	file_name = today + ".json"
	with open(file_name, 'w') as outfile:
    		json.dump(finalreturn, outfile, sort_keys = True, indent = 4)



# if __name__== "__main__":
# s = ""
print("OK")
#laundry_name = "ALLEN49"
#laundry = get_laundry_id(laundry_name)
#print(get_laundry(laundry))








   	
