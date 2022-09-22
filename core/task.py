from celery import shared_task
from time import sleep
from azure.datalake.store import core, lib, multithread
import pandas as pd
token = lib.auth()
adls_client = core.AzureDLFileSystem(token, store_name='bnlweda04d80242stgadls')

@shared_task
def sleepy(duration):
    sleep(duration)
    return None
    
response_dict = {}

@shared_task
def eda_flow_task(path, mode):
    sleep(30)
    try:
        with adls_client.open(path, mode) as f:
            df = pd.read_csv(f, low_memory=False)
            print('inside while loop')
        print('data loaded in task')
        return 'data load success'
    except Exception as e:
        response_dict.update({'error': str(e)})



