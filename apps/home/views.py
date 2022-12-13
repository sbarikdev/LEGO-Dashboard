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
from apps.home.task import async_task, async__training_task

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

# @login_required(login_url="/login/")
# def eda_flow(request):
#     data = None
#     user = request.user
#     username = user.username
#     #token = lib.auth()
#     # adls_client = core.AzureDLFileSystem(token, store_name='bnlweda04d80242stgadls')
#     # path = '/Unilever/satyajit/us_amz.csv'
#     # mode = 'rb'
#     # df = eda_flow_task.delay(path, mode)
#     df = pd.read_csv("/home/satyajit/Desktop/opensource/data/us_amz.csv", low_memory=False)
#     # with adls_client.open(path, mode) as f:
#     #     df = pd.read_csv(f, low_memory=False)
#     df = df.head(10)
#     json_records = df.reset_index()
#     data = []
#     data = json.loads(json_records.to_json(orient ='records'))
#     context = {'data': data, 'message': 'data loaded successfully.'}
#     if request.method == 'POST':
#         id_col = request.POST.get('id_col')
#         target_col = request.POST.get('target_col')
#         time_index_col = request.POST.get('time_index_col')
#         file_name = request.POST.get('file_name')
#         static_cat_col_list = request.POST.getlist('static_cat_col_list')
#         temporal_known_num_col_list = request.POST.getlist('temporal_known_num_col_list')
#         temporal_known_cat_col_list = request.POST.getlist('temporal_known_cat_col_list')
#         sort_col_list = request.POST.getlist('sort_col_list')
#         amz_columns_dict = {'id_col': id_col,
#                         'target_col': target_col,
#                         'time_index_col': time_index_col,
#                         'static_num_col_list': [],
#                         'static_cat_col_list': static_cat_col_list,
#                         'temporal_known_num_col_list':  temporal_known_num_col_list,
#                         'temporal_unknown_num_col_list': [],
#                         'temporal_known_cat_col_list': temporal_known_cat_col_list,
#                         'temporal_unknown_cat_col_list': [],
#                         'strata_col_list': [],
#                         'sort_col_list': sort_col_list,
#                         'wt_col': None,
#                         }
#         print('amz_columns_dict-------->', amz_columns_dict)
#         import os
#         from core.settings import BASE_DIR
#         download_path = os.path.join(BASE_DIR, "projects/eda/%s/" % username)
#         if not os.path.exists(download_path):
#             try:
#                 os.makedirs(download_path)
#                 print('folder created----->')
#             except FileExistsError:
#             # directory already exists
#                 pass
#         import uuid
#         download_path = str(download_path)
#         print('download_path------------->', download_path)
#         uuid_no=uuid.uuid4().hex[:5]
#         name_of_file =  file_name + '_' + str(uuid_no)         
#         save_path = download_path
#         # file_path = Path(save_path, name_of_file+".html")  
#         file_path = os.path.join(save_path, name_of_file+".html")
#         print('file_path--------->', file_path)
#         file1 = open(file_path, "w")
#         toFile = 'training_param'
#         file1.write(toFile)
#         file1.close()
#         try:   
#             status = async_task.delay(amz_columns_dict, download_path, file_name)
#             print('status--------------->', status)
#             # user = request.user
#             # if user.email:
#             #     from_email = settings.FROM_EMAIL
#             #     recipient_email = user.email
#             #     subject = 'EDA file generated'
#             #     message = 'Your EDA file is generated successfully.'
#             #     try:
#             #         from django.core.mail import send_mail
#             #         status = send_mail(subject, message, from_email, [recipient_email, ], fail_silently=False)
#             #     except Exception as e:
#             #         print('email error is ------>', e)
#             #         return render(request,'home/index.html', {'message': 'email error'})
#             # else:
#             #     recipient_email = None 
#             return render(request,'home/index.html', {'message': 'Eda Generated Complete'})
#         except Exception as e:
#             print('error is---->', e)
#             return render(request,'home/index.html', {'message': 'Error while generating EDA'})
#     return render(request, "home/data/eda-flow.html", context)



# @login_required(login_url="/login/")
# def training_model(request):
#     data = None
#     df = pd.read_csv("/home/satyajit/Desktop/opensource/data/us_amz.csv", low_memory=False)
#     # with adls_client.open(path, mode) as f:
#     #     df = pd.read_csv(f, low_memory=False)
#     df = df.head(10)
#     json_records = df.reset_index()
#     data = []
#     data = json.loads(json_records.to_json(orient ='records'))
#     context = {'data': data, 'message': 'data loaded successfully.'}
#     if request.method == 'POST':
#         id_col = request.POST.get('id_col')
#         target_col = request.POST.get('target_col')
#         time_index_col = request.POST.get('time_index_col')
#         static_cat_col_list = request.POST.getlist('static_cat_col_list')
#         temporal_known_num_col_list = request.POST.getlist('temporal_known_num_col_list')
#         temporal_known_cat_col_list = request.POST.getlist('temporal_known_cat_col_list')
#         sort_col_list = request.POST.getlist('sort_col_list')
#         promo_num_cols = request.POST.getlist('promo_num_cols')
#         strata_cols = request.POST.getlist('strata_cols')
#         amz_columns_dict = {'id_col': id_col,
#                         'target_col': target_col,
#                         'time_index_col': time_index_col,
#                         'static_num_col_list': [],
#                         'static_cat_col_list': static_cat_col_list,
#                         'temporal_known_num_col_list':  temporal_known_num_col_list,
#                         'temporal_unknown_num_col_list': [],
#                         'temporal_known_cat_col_list': temporal_known_cat_col_list,
#                         'temporal_unknown_cat_col_list': [],
#                         'strata_col_list': [],
#                         'sort_col_list': sort_col_list,
#                         'wt_col': None,
#                         }
#         #data_obj parameter
#         window_len=int(request.POST.get('window_len'))
#         fh=int(request.POST.get('fh'))
#         batch=int(request.POST.get('batch'))
#         min_nz=int(request.POST.get('min_nz'))
#         PARALLEL_DATA_JOBS=int(request.POST.get('PARALLEL_DATA_JOBS'))
#         PARALLEL_DATA_JOBS_BATCHSIZE=int(request.POST.get('PARALLEL_DATA_JOBS_BATCHSIZE'))

#         data_obj_param = {'window_len': window_len,
#                         'fh': fh,
#                         'batch': batch,
#                         'min_nz': min_nz,
#                         'PARALLEL_DATA_JOBS': PARALLEL_DATA_JOBS,
#                         'PARALLEL_DATA_JOBS_BATCHSIZE':  PARALLEL_DATA_JOBS_BATCHSIZE,
#                         }

#         #build model
#         num_layers =int(request.POST.get('num_layers'))
#         num_heads = int(request.POST.get('num_heads'))
#         kernel_sizes = list(map(int, request.POST.get('kernel_sizes').split(',')))
#         print('kernel_sizes------>', kernel_sizes)
#         d_model = int(request.POST.get('d_model'))
#         forecast_horizon = int(request.POST.get('forecast_horizon'))
#         max_inp_len = int(request.POST.get('max_inp_len'))
#         loss_type = request.POST.get('loss_type')
#         num_quantiles = int(request.POST.get('num_quantiles'))      
#         decoder_lags = int(request.POST.get('decoder_lags'))   
#         dropout_rate= float(request.POST.get('dropout_rate'))

#         build_model_param = {'num_layers': num_layers,
#                         'num_heads': num_heads,
#                         'kernel_sizes': kernel_sizes,
#                         'd_model': d_model,
#                         'forecast_horizon': forecast_horizon,
#                         'max_inp_len':  max_inp_len,
#                         'loss_type': loss_type,
#                         'num_quantiles': num_quantiles,
#                         'decoder_lags': decoder_lags,
#                         'dropout_rate': dropout_rate,
#                         }
#         # Training specific parameters
#         metric = request.POST.get('metric')
#         learning_rate = float(request.POST.get('learning_rate'))
#         max_epochs=int(request.POST.get('max_epochs'))
#         min_epochs=int(request.POST.get('min_epochs'))
#         train_steps_per_epoch=int(request.POST.get('train_steps_per_epoch'))
#         test_steps_per_epoch=int(request.POST.get('test_steps_per_epoch'))
#         patience=int(request.POST.get('patience'))

#         training_spec_param = {'metric': metric,
#                         'learning_rate': learning_rate,
#                         'max_epochs': max_epochs,
#                         'min_epochs': min_epochs,
#                         'train_steps_per_epoch': train_steps_per_epoch,
#                         'test_steps_per_epoch':  test_steps_per_epoch,
#                         'patience': patience,
#                         }
#         # from collections import ChainMap  
#         # training_param = str(dict(ChainMap(amz_columns_dict, data_obj_param, build_model_param, training_spec_param)))
#         # print('training_param-------->', training_param)
#         # import os.path
#         # from core.settings import BASE_DIR
#         # import os
#         # download_path = os.path.join(BASE_DIR, "input_files/")
#         # save_path = download_path
#         # if os.path.exists(save_path):
#         #     name_of_file = 'training_param'
#         #     completeName = os.path.join(save_path, name_of_file+".txt")         
#         #     file1 = open(completeName, "w")
#         #     toFile = training_param
#         #     file1.write(toFile)
#         #     file1.close()
#         # else:
#         #     print('path error')
#         #     return render(request,'home/index.html', {'message': 'enter the correct path'})
#         # try:
#         #     status = async__training_task.delay(amz_columns_dict,promo_num_cols,metric,learning_rate,num_layers,
#         #     num_heads,kernel_sizes,d_model,forecast_horizon,loss_type,max_inp_len,num_quantiles,decoder_lags,
#         #     dropout_rate,max_epochs,min_epochs,train_steps_per_epoch,test_steps_per_epoch,patience,
#         #     window_len,fh,batch,min_nz,PARALLEL_DATA_JOBS,PARALLEL_DATA_JOBS_BATCHSIZE
#         #     )
#         #     print('status--------------->', status)
#         #     print('welcome---------->')
#         #     return render(request,'home/index.html', {'message': 'Save Complete'})
#         # except Exception as e:
#         #     print('error is: {}'.format(e))
#     return render(request, "home/data/training-model.html", context)






# @login_required(login_url="/login/")
# def inference_flow(request):
#     data = None
#     user = request.user
#     username = user.username
#     #token = lib.auth()
#     # adls_client = core.AzureDLFileSystem(token, store_name='bnlweda04d80242stgadls')
#     # path = '/Unilever/satyajit/us_amz.csv'
#     # mode = 'rb'
#     # df = eda_flow_task.delay(path, mode)
#     df = pd.read_csv("/home/satyajit/Desktop/opensource/data/us_amz.csv", low_memory=False)
#     # with adls_client.open(path, mode) as f:
#     #     df = pd.read_csv(f, low_memory=False)
#     df = df.head(10)
#     json_records = df.reset_index()
#     data = []
#     data = json.loads(json_records.to_json(orient ='records'))
#     context = {'data': data, 'message': 'data loaded successfully.'}
#     if request.method == 'POST':
#         id_col = request.POST.get('id_col')
#         target_col = request.POST.get('target_col')
#         time_index_col = request.POST.get('time_index_col')
#         file_name = request.POST.get('file_name')
#         static_cat_col_list = request.POST.getlist('static_cat_col_list')
#         temporal_known_num_col_list = request.POST.getlist('temporal_known_num_col_list')
#         temporal_known_cat_col_list = request.POST.getlist('temporal_known_cat_col_list')
#         sort_col_list = request.POST.getlist('sort_col_list')
#         amz_columns_dict = {'id_col': id_col,
#                         'target_col': target_col,
#                         'time_index_col': time_index_col,
#                         'static_num_col_list': [],
#                         'static_cat_col_list': static_cat_col_list,
#                         'temporal_known_num_col_list':  temporal_known_num_col_list,
#                         'temporal_unknown_num_col_list': [],
#                         'temporal_known_cat_col_list': temporal_known_cat_col_list,
#                         'temporal_unknown_cat_col_list': [],
#                         'strata_col_list': [],
#                         'sort_col_list': sort_col_list,
#                         'wt_col': None,
#                         }
#         print('amz_columns_dict-------->', amz_columns_dict)
#         import os
#         from core.settings import BASE_DIR
#         download_path = os.path.join(BASE_DIR, "projects/eda/%s/" % username)
#         if not os.path.exists(download_path):
#             try:
#                 os.makedirs(download_path)
#                 print('folder created----->')
#             except FileExistsError:
#             # directory already exists
#                 pass
#         import uuid
#         download_path = download_path 
#         print('download_path------------->', download_path)
#         uuid_no=uuid.uuid4().hex[:5]
#         name_of_file =  file_name + '_' + str(uuid_no)         
#         save_path = download_path
#         # file_path = Path(save_path, name_of_file+".html")  
#         file_path = os.path.join(save_path, name_of_file+".html")
#         print('file_path--------->', file_path)
#         file1 = open(file_path, "w")
#         toFile = 'training_param'
#         file1.write(toFile)
#         file1.close()
#         try:   
#             status = async_task.delay(amz_columns_dict)
#             print('status--------------->', status)
#             # user = request.user
#             # if user.email:
#             #     from_email = settings.FROM_EMAIL
#             #     recipient_email = user.email
#             #     subject = 'EDA file generated'
#             #     message = 'Your EDA file is generated successfully.'
#             #     try:
#             #         from django.core.mail import send_mail
#             #         status = send_mail(subject, message, from_email, [recipient_email, ], fail_silently=False)
#             #     except Exception as e:
#             #         print('email error is ------>', e)
#             #         return render(request,'home/index.html', {'message': 'email error'})
#             # else:
#             #     recipient_email = None 
#             return render(request,'home/index.html', {'message': 'Eda Generated Complete'})
#         except Exception as e:
#             print('error is---->', e)
#             return render(request,'home/index.html', {'message': 'Error while generating EDA'})
#     return render(request, "home/data/eda-flow.html", context)




##############################################################################

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
        #download_path = request.POST.get('download_path')
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
        # from core.settings import BASE_DIR
        import os
        # download_path = os.path.join(BASE_DIR, "input_files/")
        try:   
            user = request.user
            username = user.username
            print('usernameeeeeeeeeeeeee------------>', username)
            status = async_task.delay(amz_columns_dict, file_name, username)
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
        except Exception as e:
            print('error is---->', e)
            return render(request,'home/index.html', {'message': 'Error while generating EDA'})
    return render(request, "home/data/eda-flow.html", context)



@login_required(login_url="/login/")
def training_model(request):
    data = None
    df = pd.read_csv("/home/satyajit/Desktop/opensource/data/us_amz.csv", low_memory=False)
    # with adls_client.open(path, mode) as f:
    #     df = pd.read_csv(f, low_memory=False)
    df = df.head(10)
    json_records = df.reset_index()
    data = []
    data = json.loads(json_records.to_json(orient ='records'))
    context = {'data': data, 'message': 'data loaded successfully.'}
    if request.method == 'POST':
        id_col = request.POST.get('id_col')
        target_col = request.POST.get('target_col')
        time_index_col = request.POST.get('time_index_col')
        static_cat_col_list = request.POST.getlist('static_cat_col_list')
        temporal_known_num_col_list = request.POST.getlist('temporal_known_num_col_list')
        temporal_known_cat_col_list = request.POST.getlist('temporal_known_cat_col_list')
        sort_col_list = request.POST.getlist('sort_col_list')
        promo_num_cols = request.POST.getlist('promo_num_cols')
        strata_cols = request.POST.getlist('strata_cols')
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

        #data_obj parameter
        window_len=int(request.POST.get('window_len'))
        fh=int(request.POST.get('fh'))
        batch=int(request.POST.get('batch'))
        min_nz=int(request.POST.get('min_nz'))
        PARALLEL_DATA_JOBS=int(request.POST.get('PARALLEL_DATA_JOBS'))
        PARALLEL_DATA_JOBS_BATCHSIZE=int(request.POST.get('PARALLEL_DATA_JOBS_BATCHSIZE'))

        data_obj_param = {'window_len': window_len,
                        'fh': fh,
                        'batch': batch,
                        'min_nz': min_nz,
                        'PARALLEL_DATA_JOBS': PARALLEL_DATA_JOBS,
                        'PARALLEL_DATA_JOBS_BATCHSIZE':  PARALLEL_DATA_JOBS_BATCHSIZE,
                        }
        print('data_obj_param-------->', data_obj_param)

        #build model
        num_layers =int(request.POST.get('num_layers'))
        num_heads = int(request.POST.get('num_heads'))
        kernel_sizes = list(map(int, request.POST.get('kernel_sizes').split(',')))
        d_model = int(request.POST.get('d_model'))
        forecast_horizon = int(request.POST.get('forecast_horizon'))
        max_inp_len = int(request.POST.get('max_inp_len'))
        loss_type = request.POST.get('loss_type')
        num_quantiles = int(request.POST.get('num_quantiles'))      
        decoder_lags = int(request.POST.get('decoder_lags'))   
        dropout_rate= float(request.POST.get('dropout_rate'))

        build_model_param = {'num_layers': num_layers,
                        'num_heads': num_heads,
                        'kernel_sizes': kernel_sizes,
                        'd_model': d_model,
                        'forecast_horizon': forecast_horizon,
                        'max_inp_len':  max_inp_len,
                        'loss_type': loss_type,
                        'num_quantiles': num_quantiles,
                        'decoder_lags': decoder_lags,
                        'dropout_rate': dropout_rate,
                        }
        print('build_model_param-------->', build_model_param)
        # Training specific parameters
        metric = request.POST.get('metric')
        learning_rate = float(request.POST.get('learning_rate'))
        max_epochs=int(request.POST.get('max_epochs'))
        min_epochs=int(request.POST.get('min_epochs'))
        train_steps_per_epoch=int(request.POST.get('train_steps_per_epoch'))
        test_steps_per_epoch=int(request.POST.get('test_steps_per_epoch'))
        patience=int(request.POST.get('patience'))

        training_spec_param = {'metric': metric,
                        'learning_rate': learning_rate,
                        'max_epochs': max_epochs,
                        'min_epochs': min_epochs,
                        'train_steps_per_epoch': train_steps_per_epoch,
                        'test_steps_per_epoch':  test_steps_per_epoch,
                        'patience': patience,
                        }
        print('training_spec_param-------->', training_spec_param)
        try:
            user = request.user
            username = user.username
            print('usernameeeeeeeeeeeeee------------>', username)
            status = async__training_task.delay(amz_columns_dict,promo_num_cols,metric,learning_rate,num_layers,
            num_heads,kernel_sizes,d_model,forecast_horizon,loss_type,max_inp_len,num_quantiles,decoder_lags,
            dropout_rate,max_epochs,min_epochs,train_steps_per_epoch,test_steps_per_epoch,patience,
            window_len,fh,batch,min_nz,PARALLEL_DATA_JOBS,PARALLEL_DATA_JOBS_BATCHSIZE, username
            )
            print('status--------------->', status)
            print('welcome---------->')
            return render(request,'home/index.html', {'message': 'Save Complete'})
        except Exception as e:
            print('error is: {}'.format(e))
    return render(request, "home/data/training-model.html", context)