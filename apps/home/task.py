

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
    # uuid_no=uuid.uuid4().hex[:5]
    # name_of_file = str(uuid_no) + '_' + file_name
    # file_path = Path(save_path, name_of_file+".html")  
    file_path = os.path.join(save_path, file_name+".html")    
    eda_object.create_report(data=df, filename=file_path)
    return 'eda task complete'


@shared_task
def async__training_task(amz_columns_dict,promo_num_cols,metric,learning_rate,num_layers,
            num_heads,kernel_sizes,d_model,forecast_horizon,loss_type,max_inp_len,num_quantiles,decoder_lags,
            dropout_rate,max_epochs,min_epochs,train_steps_per_epoch,test_steps_per_epoch,patience,
            window_len,fh,batch,min_nz,PARALLEL_DATA_JOBS,PARALLEL_DATA_JOBS_BATCHSIZE):
    sleep(10)
    df = pd.read_csv("/home/satyajit/Desktop/opensource/data/us_amz.csv", low_memory=False)
    df = df.head(1500)
    print("it's here training----->")
    train_till = 202152
    test_till = 202213

    # history/forecast cutoff
    history_till = 202213
    future_till = 202226
    data_obj = ctfrv2.ctfrv2_dataset(col_dict=amz_columns_dict, 
        window_len=window_len, 
        fh=fh, 
        batch=batch, 
        min_nz=min_nz,
        PARALLEL_DATA_JOBS=PARALLEL_DATA_JOBS, 
        PARALLEL_DATA_JOBS_BATCHSIZE=PARALLEL_DATA_JOBS_BATCHSIZE)

    #Create Train/Test Dataset
    trainset, testset = data_obj.train_test_dataset(df, train_till=train_till, test_till=test_till)
    train_steps_per_epoch = 5

    for i, (x,y,s,w) in enumerate(trainset):
        if i > train_steps_per_epoch:
            break
        else:
            print("step: ", i, x.shape, y.shape, s.shape, w.shape)

    # create infer dataset
    infer_dataset, actuals_df = data_obj.infer_dataset(df, history_till=history_till, future_till=future_till)
    # create baseline infer dataset
    baseline_infer_dataset = data_obj.baseline_infer_dataset(df, 
                        history_till=history_till, 
                        future_till=future_till,
                        ignore_cols=promo_num_cols, 
                        ignore_pad_values=[0]*len(promo_num_cols))

    # Additional Model Inputs
    col_index_dict = data_obj.col_index_dict
    vocab = data_obj.vocab_list(df)

    # define loss type & loss function
    #loss_fn = ctfrv2.Normal_NLL_Loss(sample_weights=False)
    #loss_fn = ctfrv2.Poisson_NLL_Loss(sample_weights=False)
    #loss_fn = ctfrv2.Huber(delta=0.8, sample_weights=False)
    #loss_fn = ctfrv2.QuantileLoss_v2(quantiles=[0.6], sample_weights=False)

    #loss_type = 'Point' # ['Point','Quantile','Negbin','Poisson','Normal']
    # sample_weights = ['True','False']
    loss_fn = ctfrv2.RMSE(sample_weights=False) # [ctfrv2.RMSE(sample_weights=sample_weights), ctfrv2.QuantileLoss_v2(quantiles = quantiles, sample_weights=sample_weights)]
    # quantiles = [0.5, 0.6, 0.7, ...] # [0 - 1]

    # build model
    try:
        del var_model
    except:
        pass
    # Training specific parameters
    try:
        var_model = ctfrv2.Feature_Weighted_ConvTransformer(col_index_dict = col_index_dict,
                    vocab_dict = vocab,
                    num_layers = num_layers,
                    num_heads = num_heads,
                    kernel_sizes = kernel_sizes,
                    d_model = d_model,
                    forecast_horizon = forecast_horizon,
                    max_inp_len = max_inp_len,
                    loss_type = loss_type,
                    num_quantiles = num_quantiles,             
                    decoder_lags = decoder_lags,          
                    dropout_rate=dropout_rate)
        var_model.build()
        print('var_model build successfully---------------->')
    except Exception as e:
        print('var_model error is: {}'.format(e))
    try:
        best_var_model = var_model.train(trainset, 
                    testset, 
                    loss_function = loss_fn,              
                    metric=metric,  #['MSE','MAE'] -- selection from menu
                    learning_rate=learning_rate, #0.00003, # explicit entry by user
                    max_epochs=max_epochs,  # rest all user eneters values
                    min_epochs=min_epochs,
                    train_steps_per_epoch=train_steps_per_epoch,
                    test_steps_per_epoch=test_steps_per_epoch,
                    patience=patience,
                    weighted_training=False,
                    model_prefix='/home/satyajit/Documents',
                    logdir='/home/satyajit/Documents')
        print('before train model build successfully---------------->')
        var_model.model.summary()
        print('after train model build successfully---------------->')
    except Exception as e:
        print('training_model error is: {}'.format(e))
    return 'training task complete'