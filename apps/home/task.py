from __future__ import absolute_import,unicode_literals
from celery import shared_task
from time import sleep
import os
import eda, ctfrv2
from pathlib import Path
import pandas as pd
import uuid

@shared_task
def async_task(amz_columns_dict, download_path, file_name):
    sleep(10)
    df = pd.read_csv("/home/satyajit/Desktop/opensource/data/us_amz.csv", low_memory=False)
    df = df.head(1500)
    print("it's here----->")
    eda_object = eda.eda(col_dict=amz_columns_dict)
    save_path = download_path
    uuid_no=uuid.uuid4().hex[:5]
    name_of_file = str(uuid_no) + '_' + file_name
    # file_path = Path(save_path, name_of_file+".html")  
    file_path = os.path.join(save_path, name_of_file+".html")    
    eda_object.create_report(data=df, filename=file_path)
    return 'eda task complete'


@shared_task
def async__training_task(trainset, testset, loss_fn, vocab, loss_type):
    sleep(10)
    print("it's here training----->")
    try:
        var_model = ctfrv2.Feature_Weighted_ConvTransformer(
                    vocab_dict = vocab,
                    num_layers = 1,
                    num_heads = 1,
                    kernel_sizes = [1],
                    d_model = 16,
                    forecast_horizon = 13,
                    max_inp_len = 13,
                    loss_type = loss_type,
                    num_quantiles = 1,             
                    decoder_lags = 1,          
                    dropout_rate=0.1)
        var_model.build()
        best_var_model = var_model.train(trainset, 
                    testset, 
                    loss_function = loss_fn,              
                    metric='MSE',  #['MSE','MAE'] -- selection from menu
                    learning_rate=0.00003, # explicit entry by user
                    max_epochs=1,  # rest all user eneters values
                    min_epochs=1,
                    train_steps_per_epoch=10,
                    test_steps_per_epoch=5,
                    patience=10,
                    weighted_training=False,
                    model_prefix='/home/satyajit/Desktop/opensource/data/test',
                    logdir='/home/satyajit/Desktop/opensource/data/test')
        var_model.model.summary()
    except Exception as e:
        print('error is: {}'.format(e))
    return 'training task complete'


