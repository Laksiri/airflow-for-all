import os
import json
import uuid
import requests
import datetime
import configparser

def get_news_headlines_by_source(source,api_key):
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

def save_headlines_data(data_dir,source,ts,data,run_id):
	if not os.path.exists(data_dir):
		os.makedirs(data_dir)

	file_name = '{base}/{run}_{src}_{ts}.txt'.format(base=data_dir,run=run_id,src=source,ts=ts)
	with open(file_name, 'w') as f:
		json.dump(data, f)

def worker(source,run_id=False):
	config = configparser.ConfigParser()
	config.read('config.ini')
	api_key= config['NEWSAPI']['apikey']
	data_dir= config['SETTINGS']['datadir']
	
	ts = datetime.datetime.now().strftime("%d_%m_%y_%H%M%S")
	if run_id == False:
		run_id = str(uuid.uuid4())

	news_data = get_news_headlines_by_source(source,api_key)
	if news_data:
		save_headlines_data(data_dir,source,ts,news_data,run_id)

if __name__ == "__main__":
	# This is for local testing
	worker('cnn')




