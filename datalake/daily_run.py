import requests
import boto3
import os
import json
from bs4 import BeautifulSoup
from zipfile import ZipFile
from StringIO import StringIO
from datetime import date

# # A helper function to parse the download file page and extract all the ZIP file URLs
def parse_page():
	# Base URL for the web site
	base_url = 'https://aact.ctti-clinicaltrials.org'
	# URL for downloading files
	download_page_url = base_url + '/pipe_files'
	resp = requests.get(download_page_url)
	soup = BeautifulSoup(resp.content, 'html.parser')
	res = list()
	for link in soup.table.find_all('a'):
		res.append(str(base_url + link['href']))
	return res

# A helper function to retrieve a list of ZIP file names that are already downloaded
def get_downloaded_files_list(bucket_name, key_name):
	'''
	The function will fetch a JSON file from AWS S3, which stored the file names that it has already
	download historically. It assume the JSON file contains a pair with 'downloaded_files' as the key
	and a list of file names as the value.
	'''
	# Extract the file name from the key name
	pos = key_name.rfind('/')
	if pos == -1:
		file_name = key_name
	else:
		file_name = key_name[pos + 1:]
	download_path = '/tmp/' + file_name
	s3 = boto3.resource('s3')
	bucket = s3.Bucket(bucket_name)
	bucket.download_file(key_name, download_path)
	properties = json.load(open(download_path, 'r'))
	return properties['downloaded_files']

# A helper function to update the downloaded file list in S3
def update_downloaded_files_list(bucket_name, key_name, old_list, new_file_url):
	'''
	The function will add the newly downloaded file's URL into the list in the JSON object and update
	the new JSON object to S3.
	'''
	# Add the new file URL to the list
	old_list.append(new_file_url)
	# Make it into a dictionary
	pairs = dict()
	pairs['downloaded_files'] = old_list
	# Create a temporary JSON file for uploading
	json_str = json.dumps(pairs)
	print json_str
	in_mem_obj = StringIO(json_str)
	# Upload the JSON file
	s3 = boto3.resource('s3')
	bucket = s3.Bucket(bucket_name)
	bucket.upload_fileobj(in_mem_obj, key_name)
	in_mem_obj.close()

# A helper function to download a ZIP file from a specified URL
def download_data(zip_url, bucket_name):
	''' 
	The ZIP file URL is in the following format: 
	'https://aact.ctti-clinicaltrials.org/static/exported_files/20180201_pipe-delimited-export.zip'
	The function will store each data file into a coresponding folder with the same name and the data 
	file will be renamed as the date specified in the ZIP file name, under the specified bucket.
	e.g. Every file extracted from the ZIP file in the above URL will be store as 'tablename/20180201' 
	in the specified bucket
	'''
	# Extract the date from the URL
	start_pos = zip_url.rfind('/')
	end_pos = zip_url.find('_', start_pos + 1)
	timestamp = ''
	if start_pos == -1 or end_pos == -1:
		# Failed to locate the date in the URL, use the date of today as a default value
		timestamp = date.today().strftime('%Y%m%d')
	else:
		timestamp = zip_url[start_pos + 1 : end_pos]
	# Download an 50 MB chunk each time
	download_chunk_size = 50 * 1024 * 1024
	# Streaming download, a chunk at a timerr
	zip_resp = requests.get(zip_url, stream=True)
	# Store the ZIP file in memory
	in_mem_file = StringIO()
	for chunk in zip_resp.iter_content(chunk_size=download_chunk_size):
		in_mem_file.write(chunk)
	# Make the download content into a ZIP file
	in_mem_zip = ZipFile(in_mem_file)
	# Upload to S3
	s3 = boto3.resource('s3')
	my_bucket = s3.Bucket(bucket_name)
	# Go through every file in the ZIP file
	for each in in_mem_zip.namelist():
		# Remove possible file extension name to use it as directory name
		test_pos = each.find('.txt')
		if test_pos != -1:
			dir_name = each[:test_pos]
		else:
			dir_name = each
		# Construct an in-memory file object
		in_mem_unzip_file = StringIO(in_mem_zip.read(each))
		# Put each file in its folder and name it as the timestamp
		my_bucket.upload_fileobj(in_mem_unzip_file, dir_name + '/' + timestamp)
		# Release the StringIO to save some space
		in_mem_unzip_file.close()

# The main routine of the script
def main():
	# Names of the S3 buckets
	data_bucket_name = 'tibersolution-datalake'
	config_bucket_name = 'tibersolution-datalake-configuration'
	# The key of the configuration file on S3
	key_name = 'persistent_states/downloaded_files.json'
	# Fetch all the ZIP file URLs on the page
	urls = set(parse_page())
	# Set up the access secret key for AWS API services
	setup_key()
	# Fetch all the downloaded file names from S3
	downloaded_files = set(get_downloaded_files_list(config_bucket_name, key_name))
	# Find out all the files that haven't been download
	new_files = urls - downloaded_files
	# Pick an random file in this set
	zip_url = new_files.pop()
	# Download the file, extract it and upload every table to S3
	download_data(zip_url, data_bucket_name)
	# Update the JSON file on S3
	update_downloaded_files_list(config_bucket_name, key_name, list(downloaded_files), zip_url)

if __name__ == '__main__':
	main()
