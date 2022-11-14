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
def async__training_task(amz_columns_dict,promo_num_cols,metric,learning_rate):
    sleep(10)
    df = pd.read_csv("/home/satyajit/Desktop/opensource/data/us_amz.csv", low_memory=False)
    df = df.head(10)
    print("it's here training----->")
    train_till = 202152
    test_till = 202213

    # history/forecast cutoff
    history_till = 202213
    future_till = 202226
    data_obj = ctfrv2.ctfrv2_dataset(col_dict=amz_columns_dict, 
        window_len=26, 
        fh=13, 
        batch=16, 
        min_nz=0,
        PARALLEL_DATA_JOBS=2, 
        PARALLEL_DATA_JOBS_BATCHSIZE=128)

    # Create Train/Test Dataset
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

    loss_type = 'Point' # ['Point','Quantile','Negbin','Poisson','Normal']
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
        print('var_model build successfully---------------->')
        # best_var_model = var_model.train(trainset, 
        #             testset, 
        #             loss_function = loss_fn,              
        #             metric=metric,  #['MSE','MAE'] -- selection from menu
        #             learning_rate=learning_rate, #0.00003, # explicit entry by user
        #             max_epochs=1,  # rest all user eneters values
        #             min_epochs=1,
        #             train_steps_per_epoch=10,
        #             test_steps_per_epoch=5,
        #             patience=10,
        #             weighted_training=False,
        #             model_prefix='/home/satyajit/Music/test',
        #             logdir='/home/satyajit/Music/test')
        # var_model.model.summary()
        print('train model build successfully---------------->')
    except Exception as e:
        print('error is: {}'.format(e))
    return 'training task complete'


