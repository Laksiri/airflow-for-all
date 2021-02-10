import os
import json
import uuid
import requests
import datetime
import configparser

def get_news_headlines_by_source(source,api_key):
	# This function is to get news headlines for a given news source. 

	config = configparser.ConfigParser()
	config.read('creds.ini')
	
	url= 'https://newsapi.org/v2/top-headlines' 
	parameters_dict =  {'apikey': api_key, 'sources': source }
	response = requests.get(url,params=parameters_dict)

	if response.status_code == 200:
		news_data = json.loads(response.content.decode('utf-8'))
		return news_data
	else:
		print("Error in API call: {api}".format(api=url))
		return None


def save_headlines_data(data_dir,source,ts,data):
	# This function is to write the output of news headlines API in to a given location.
	# Output file naming conventions is : [source]_[timestamp].txt

	if not os.path.exists(data_dir):
		os.makedirs(data_dir)

	file_name = '{base}/{src}_{ts}.txt'.format(base=data_dir,src=source,ts=ts)
	with open(file_name, 'w') as f:
		json.dump(data, f)


def worker(source):
	# This is the worker funtion of this app. 
	# A wrapper for get_news_headlines_by_source and save_headlines_data.

	config = configparser.ConfigParser()
	config.read('config.ini')
	api_key= config['NEWSAPI']['apikey']
	data_dir= config['SETTINGS']['datadir']
	
	ts = datetime.datetime.now().strftime("%d_%m_%y_%H%M%S")

	news_data = get_news_headlines_by_source(source,api_key)
	if news_data:
		save_headlines_data(data_dir,source,ts,news_data)


if __name__ == "__main__":
	# This is for local testing
	worker('cnn')