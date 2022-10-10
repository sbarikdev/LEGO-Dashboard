# -*- encoding: utf-8 -*-


from django.test import TestCase

# Create your tests here.
import os.path
import pandas as pd
import dask.dataframe as dd 
import eda
import json

from azure.datalake.store import core, lib, multithread
import pandas as pd

# token = lib.auth()
# adls_client = core.AzureDLFileSystem(token, store_name='bnlweda04d80242stgadls')


#parent class
class DataLoad:
    
    def __init__(self, save_path, name_of_file):
        self.save_path = save_path
        self.name_of_file = name_of_file
    def file_load(self):
        file_path = os.path.join(self.save_path, self.name_of_file+".html")
        return file_path
    def data_display(request,*args, **kwargs):
        #path = '/Unilever/satyajit/us_amz.csv'
        #mode = 'rb'
        #with adls_client.open(path, mode) as f:
            #df = pd.read_csv(f, low_memory=False)
            #json_records = df.reset_index().to_json(orient ='records')
            #data = []
            #data = json.loads(json_records)
            #context = {'data': data}
        #return df
        df = pd.read_csv("us_amz.csv", low_memory=False)
        return df
        
#child class
class EdaFlow(DataLoad):
    def __init__(self,id_col,target_col,time_index_col,save_path, name_of_file):
        self.id_col = id_col
        self.target_col = target_col
        self.time_index_col = time_index_col
        DataLoad.__init__(self,save_path, name_of_file)
        
    def eda_flow(request,*args, **kwargs):
        name = 'hello'
        amz_columns_dict = {'id_col': 'cpf',
                    'target_col': 'PHY_CS',
                    'time_index_col': 'G_WEEK',
                    'wt_col': None}
        eda_object = eda.eda(col_dict=amz_columns_dict)
        return eda_object
    
    def eda_create(self):
        f = DataLoad.data_display(self)
        eda_object = EdaFlow.eda_flow(self)
        file_path = DataLoad.file_load(self)
        eda_object.create_report(data=f, filename=file_path) 

if __name__ == "__main__":
    save_path = '/home/satyajit/Desktop/'
    name_of_file = input("What is the name of the file: ")
    id_col = 'cpf'
    target_col = 'PHY_CS'
    time_index_col = 'G_WEEK'
    a = EdaFlow(id_col,target_col,time_index_col,save_path, name_of_file) #initialize object

    # #calling a functuon of the class DataLoad using it's instance
    a.eda_create()
#     a.eda_flow()
    # a2 = DataLoad()
    # a2.data_display()  
else:
    print('error')
