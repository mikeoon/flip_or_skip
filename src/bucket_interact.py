import boto3
import pickle
import numpy as np



def download_imgs(brand):
	s3 = boto3.client('s3')
	shoe_set = set()
	bucket_name = 'mikeoon-galvanize-bucket'
	first = True
	st_point = None
	# Hard coded to the max number of jordans
	while len(shoe_set) != 29655:
		# Can only take 1000 (0-999) requests at a time
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


# For only image directory that is local
def find_broken_imgs(brand):
	shoe_paths=dict()
	for k,v in img_names.items():
		temp_paths = []
		if v[1]:
			for i in range(1,37):
				try:
					if i < 10:
						shoe = io.imread(f'data/{brand}/{v[0]}_img0{i}.jpg')
					else:
						shoe = io.imread(f'data/{brand}/{v[0]}_img{i}.jpg')
				except:
					if i < 10:
						temp_paths.append(f'data/{brand}/{v[0]}_img0{i}.jpg')
					else:
						temp_paths.append(f'data/{brand}/{v[0]}_img{i}.jpg')
						print('Error, shoe does not have this many imgs')
		else:
			try:
				shoe = io.imread(f'data/{brand}/{v[0]}_img01.jpg')
			except:
				print('Error, shoe does not have this many imgs')
				temp_paths.append(f'data/{brand}/{v[0]}_img01.jpg')
		if len(temp_paths) != 0:
			shoe_paths[k] = temp_paths
		print(f'{k} has broken files \n')
	
	with open(f'data/{brand}/broken_imgs.pkl', 'wb') as f:
		pickle.dump(shoe_paths, f)




def delete_broken_imgs(brand):
	s3 = boto3.client('s3')
	shoe_set = set()
	bucket_name = 'mikeoon-galvanize-bucket'





