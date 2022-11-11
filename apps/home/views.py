# -*- encoding: utf-8 -*-

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render

# from databricks_cli.sdk.api_client import ApiClient
# from databricks_cli.dbfs.api import DbfsApi
# from databricks_cli.dbfs.dbfs_path import DbfsPath
import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
# pd.set_option("display.max_columns", 200)
import eda, ctfrv2
import numpy as np
from pyspark.sql import functions as F
from IPython.display import set_matplotlib_formats
# set_matplotlib_formats('retina')
# pd.set_option("display.max_columns", 100)
# pd.set_option("display.max_rows", 100)



# try:
#     import dask.dataframe as dd
# except Exception as e:
#     print(e)
from azure.datalake.store import core, lib, multithread
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render

# from core.settings import DATABRICKS_HOST,DATABRICKS_TOKEN

# api_client = ApiClient(host = DATABRICKS_HOST, token = DATABRICKS_TOKEN)
import pandas as pd
from apps.home.task import async_task

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

import json
# def tables_data(request):
#     path = '/Unilever/satyajit/data1.parquet'
#     mode = 'rb'
#     with adls_client.open(path, mode) as f:
#         data = pd.read_parquet(f,  engine='pyarrow')
#     #data = pd.read_parquet("/home/satyajit/Desktop/opensource/data/data1.parquet")
#     data = data.head(50)
#     json_records = data.reset_index().to_json(orient ='records')
#     data = []
#     data = json.loads(json_records)
#     context = {'data': data}
#     df = pd.DataFrame(data)
#     df.set_index('index', inplace=True)
#     sns.barplot(data=df, x='Year_Week', y='SalesCSVolume')
#     plt.savefig('apps/static/assets/pic.png')
#     return render(request, "home/tables-data.html", context)

@login_required(login_url="/login/")
def eda_flow(request):
    data = None
    #token = lib.auth()
    # adls_client = core.AzureDLFileSystem(token, store_name='bnlweda04d80242stgadls')
    # path = '/Unilever/satyajit/us_amz.csv'
    # mode = 'rb'
    # df = eda_flow_task.delay(path, mode)
    df = pd.read_csv("/home/satyajit/Desktop/opensource/data/us_amz.csv", low_memory=False)
    # with adls_client.open(path, mode) as f:
    #     df = pd.read_csv(f, low_memory=False)
    df = df.head(100)
    json_records = df.reset_index()
    data = []
    data = json.loads(json_records.to_json(orient ='records'))
    context = {'data': data, 'message': 'data loaded successfully.'}
    if request.method == 'POST':
        id_col = request.POST.get('id_col')
        target_col = request.POST.get('target_col')
        time_index_col = request.POST.get('time_index_col')
        file_name = request.POST.get('file_name')
        download_path = request.POST.get('download_path')
        static_cat_col_list = request.POST.getlist('static_cat_col_list')
        temporal_known_num_col_list = request.POST.getlist('temporal_known_num_col_list')
        temporal_known_cat_col_list = request.POST.getlist('temporal_known_cat_col_list')
        sort_col_list = request.POST.getlist('sort_col_list')
        amz_columns_dict = {'id_col': id_col,
                        'target_col': target_col,
                        'time_index_col': time_index_col,
                        'static_num_col_list': [],
                        'static_cat_col_list': static_cat_col_list,
                        'temporal_known_num_col_list':  temporal_known_num_col_list,
                        'temporal_unknown_num_col_list': [],
                        'temporal_known_cat_col_list': temporal_known_cat_col_list,
                        'temporal_unknown_cat_col_list': [],
                        'strata_col_list': [],
                        'sort_col_list': sort_col_list,
                        'wt_col': None,
                        }
        print('amz_columns_dict-------->', amz_columns_dict)
        from core.settings import BASE_DIR
        import os
        download_path = os.path.join(BASE_DIR, "input_files/")
        try:   
            from pathlib import Path
            if os.path.exists(download_path):
                status = async_task.delay(amz_columns_dict, download_path, file_name)
                print('status--------------->', status)
                user = request.user
                # if user.email:
                #     from_email = settings.FROM_EMAIL
                #     recipient_email = user.email
                #     subject = 'EDA file generated'
                #     message = 'Your EDA file is generated successfully.'
                #     try:
                #         from django.core.mail import send_mail
                #         status = send_mail(subject, message, from_email, [recipient_email, ], fail_silently=False)
                #     except Exception as e:
                #         print('email error is ------>', e)
                #         return render(request,'home/index.html', {'message': 'email error'})
                # else:
                #     recipient_email = None 
                return render(request,'home/index.html', {'message': 'Save Complete'})
            else:
                return render(request,'home/index.html', {'message': 'download path is not exist'})
        except Exception as e:
            print('error is---->', e)
            return render(request,'home/index.html', {'message': 'Error while generating EDA'})
    return render(request, "home/tables-simple.html", context)



@login_required(login_url="/login/")
def training_model(request):
    data = None
    df = pd.read_csv("/home/satyajit/Desktop/opensource/data/us_amz.csv", low_memory=False)
    # with adls_client.open(path, mode) as f:
    #     df = pd.read_csv(f, low_memory=False)
    df = df.head(100)
    json_records = df.reset_index()
    data = []
    data = json.loads(json_records.to_json(orient ='records'))
    context = {'data': data, 'message': 'data loaded successfully.'}
    if request.method == 'POST':

        key_col = 'cpf'
        time_index_col = 'G_WEEK'
        target_col = 'PHY_CS'
        event_cols = ['prime_day']
        date_cols = ['W']
        promo_num_cols = [ 'Percent_Discount']
        static_cat_cols = ['BrandCode']
        known_num_cols = ['Holidays']
        unknown_num_cols = []
        strata_cols = ['TrainGroup']

        amz_columns_dict = {'id_col': key_col,
                    'target_col': target_col,
                    'time_index_col': time_index_col,
                    'static_num_col_list': [],
                    'static_cat_col_list': static_cat_cols,
                    'temporal_known_num_col_list': event_cols + known_num_cols + promo_num_cols,
                    'temporal_unknown_num_col_list': [],
                    'temporal_known_cat_col_list': date_cols,
                    'temporal_unknown_cat_col_list': [],
                    'strata_col_list': [],
                    'sort_col_list': [key_col,time_index_col],
                    'wt_col': None}
        print('amz_columns_dict-------->', amz_columns_dict)

        data_obj = ctfrv2.ctfrv2_dataset(col_dict=amz_columns_dict, 
                window_len=26, 
                fh=13, 
                batch=16, 
                min_nz=0,
                PARALLEL_DATA_JOBS=2, 
                PARALLEL_DATA_JOBS_BATCHSIZE=128)

        train_till = 202152
        test_till = 202213

        # history/forecast cutoff
        history_till = 202213
        future_till = 202226

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
        print('var model----------------------------->', var_model)

        var_model.build()

        # Training specific parameters
        # try:
        #     best_var_model = var_model.train(trainset, 
        #                             testset, 
        #                             loss_function = loss_fn,              
        #                             metric='MSE',  #['MSE','MAE'] -- selection from menu
        #                             learning_rate=0.00003, # explicit entry by user
        #                             max_epochs=1,  # rest all user eneters values
        #                             min_epochs=1,
        #                             train_steps_per_epoch=10,
        #                             test_steps_per_epoch=5,
        #                             patience=10,
        #                             weighted_training=False,
        #                             model_prefix='/home/satyajit/Desktop/opensource/session',
        #                             logdir='/home/satyajit/Desktop/opensource/session')


        #     var_model.model.summary()

        # except Exception as e:
        #     print('error is: {}'.format(e))

    return render(request, "home/data/training-model.html", context)


