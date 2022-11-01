from __future__ import absolute_import,unicode_literals
from celery import shared_task
from time import sleep
import os
import eda
from pathlib import Path
import pandas as pd

@shared_task
def async_task(amz_columns_dict, download_path, file_name):
    sleep(10)
    df = pd.read_csv("/home/satyajit/Desktop/opensource/data/us_amz.csv", low_memory=False)
    df = df.head(3500)
    print("it's here----->")
    print('task amz_columns_dict---->', amz_columns_dict)
    eda_object = eda.eda(col_dict=amz_columns_dict)
    save_path = download_path
    name_of_file = file_name
    # file_path = Path(save_path, name_of_file+".html")  
    file_path = os.path.join(save_path, name_of_file+".html")     
    eda_object.create_report(data=df, filename=file_path)
    return 'task complete'


