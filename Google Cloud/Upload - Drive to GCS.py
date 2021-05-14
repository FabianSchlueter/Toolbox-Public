# -*- coding: utf-8 -*-
"""
Created on Fri May 14 21:41:14 2021

@author: Fabian Schlueter
"""

from google.cloud import storage

# Set Client for GCP - Create and download key file (json) for service account that is used
key_path = r'\.json'
storage_client = storage.Client.from_service_account_json(
    key_path
    )

buckets = []
# list existing buckets
def list_buckets():

    # If you don't specify credentials when constructing the client, the
    # client library will look for credentials in the environment.
    storage_client = storage.Client()

    # Make an authenticated API request
    buckets= list(storage_client.list_buckets())
    return buckets

# upload file to bucket
def upload_blob(destination_bucket, source_file, destination_file):

    bucket = storage_client.get_bucket(destination_bucket)
    blob = bucket.blob(destination_file)
    blob.upload_from_filename(source_file)

    print("File {} uploaded to {}.".format(source_file, destination_file))

# Get list of existing buckets
list_buckets()

# Upload
destination_bucket = "Bucket"
source_filename = r'\.csv'
destination_file_name = source_filename

upload_blob(destination_bucket, source_filename, destination_file_name)