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
import eda
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
    # token = lib.auth()
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
    # data2 = pd.DataFrame(data)
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
        try:   
            from pathlib import Path
            import os
            if os.path.exists(download_path):
                # eda_object = eda.eda(col_dict=amz_columns_dict)
                # save_path = download_path
                # name_of_file = file_name
                # file_path = Path(save_path, name_of_file+".html")     
                # eda_object.create_report(data=df, filename=file_path)
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
