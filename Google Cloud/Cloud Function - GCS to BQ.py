# -*- coding: utf-8 -*-
"""
Created on Fri May 14 17:19:35 2021

@author: Fabian
"""

import pandas as pd
import numpy as np
from google.cloud import storage
from google.cloud import bigquery


def GCS_to_BQ(event, context):
    """Triggered by a change to a Cloud Storage bucket.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    file = event
    print(f"Processing file: {file['name']}.")

    """Background Cloud Function to be triggered by Cloud Storage.
       This generic function logs relevant data when a file is changed.
    Args:
        event (dict):  The dictionary with data specific to this type of event.
                       The `data` field contains a description of the event in
                       the Cloud Storage `object` format described here:
                       https://cloud.google.com/storage/docs/json_api/v1/objects#resource
        context (google.cloud.functions.Context): Metadata of triggering event.
    Returns:
        None; the output is written to Stackdriver Logging
    """
    # Print Metadata
    print('Event ID: {}'.format(context.event_id))
    print('Event type: {}'.format(context.event_type))
    print('Bucket: {}'.format(event['bucket']))
    print('File: {}'.format(event['name']))
    print('Metageneration: {}'.format(event['metageneration']))
    print('Created: {}'.format(event['timeCreated']))
    print('Updated: {}'.format(event['updated']))

    # Create storage client
    client = storage.Client()
    
    if event['name'].split('.')[1] == 'csv':
        # Read csv. Specify separator and decimal.
        df = pd.read_csv('gs://' + event['bucket'] + '/' + event['name'], sep=';', decimal=",")
    elif event['name'].split('.')[1] == 'xlsx':
        # Read excel.
        df = pd.read_excel('gs://' + event['bucket'] + '/' + event['name'])
    else:
        # Only csv or excel accepted
        print('File format not accepted.')
        quit()
    
    # Add creation timestamp to datafram
    df['created'] = event['timeCreated'].strftime('%Y-%m-%d %H:%M:%S')


    #################################################################################
    # Do any transformation that is needed to get the df into desired table format.
    #################################################################################

    
    # list of columns to transform into integer and float format
    integer_columns = [['integer_column']]
    float_columns = [['float_column']]
    
    # Change format for BigQuery
    df['created'] = df['created'].astype({'created' : 'datetime64'})
    df[integer_columns] = df[integer_columns].replace(0,np.nan)
    df[integer_columns] = pd.to_numeric(df[integer_columns], errors='coerce').astype(pd.Int64Dtype())
    df[float_columns] = df[float_columns].astype({float_columns : 'float64'})

    # Save transformed csv in other bucket
    destination_bucket = 'destination_bucket'
    df.to_csv('gs://' + destination_bucket + '/' + event['name'] + '_processed.csv')
    
    bqclient = bigquery.Client()
    job_config = bigquery.LoadJobConfig()

    tablename = 'Table'
    datasetname = 'Dataset'
    dataset_ref = bqclient.dataset(datasetname)
    load_job = bqclient. load_table_from_dataframe(df, dataset_ref.table(tablename))

    load_job.result()