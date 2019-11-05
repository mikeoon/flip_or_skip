import boto3
import pickle
import numpy as np



def download_imgs(brand):
	s3 = boto3.client('s3')
	shoe_set = set()
	bucket_name = 'mikeoon-galvanize-bucket'
	first = True
	st_point = None
	while len(shoe_set) != 29655:
		if first:
			request_shoes = s3.list_objects_v2(Bucket=bucket_name, Prefix=f'data/{brand}/')
			first=False
		else:
			request_shoes = s3.list_objects_v2(Bucket=bucket_name, Prefix=f'data/{brand}/',StartAfter=st_point)
		
		keys = [shoe['Key'] for shoe in request_shoes['Contents']]
		for i,k in enumerate(keys):	
			if k not in shoe_set:
				shoe_set.add(k)
			if i >= (len(keys) - 1):
				print(f'{k} is where it stopped')
				st_point = k
		print('Last stopping point')
		print(len(shoe_set))

	for s in shoe_set:
		s3.download_file(bucket_name, s, s)
		print(f'Downloaded {s}')

def delete_broken_imgs(brand):
	s3 = boto3.client('s3')
	shoe_set = set()
	bucket_name = 'mikeoon-galvanize-bucket'





