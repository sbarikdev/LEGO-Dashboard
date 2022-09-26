# -*- encoding: utf-8 -*-

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render

from databricks_cli.sdk.api_client import ApiClient
from databricks_cli.dbfs.api import DbfsApi
from databricks_cli.dbfs.dbfs_path import DbfsPath
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import pandas as pd
# pd.set_option("display.max_columns", 200)
import eda
try:
    import dask.dataframe as dd
except Exception as e:
    print(e)
import os.path
# from azure.datalake.store import core, lib, multithread
from core.task import *
from .forms import EdaDropdownForm

from core.settings import DATABRICKS_HOST,DATABRICKS_TOKEN

api_client = ApiClient(host = DATABRICKS_HOST, token = DATABRICKS_TOKEN)


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
def tables_data(request):
    path = '/Unilever/satyajit/data1.parquet'
    mode = 'rb'
    with adls_client.open(path, mode) as f:
        data = pd.read_parquet(f,  engine='pyarrow')
    data = data.head(50)
    json_records = data.reset_index().to_json(orient ='records')
    data = []
    data = json.loads(json_records)
    context = {'data': data}
    df = pd.DataFrame(data)
    df.set_index('index', inplace=True)
    sns.barplot(data=df, x='Year_Week', y='SalesCSVolume')
    plt.savefig('apps/static/assets/pic.png')
    return render(request, "home/tables-data.html", context)

def eda_flow(request):
    path = '/Unilever/satyajit/us_amz.csv'
    mode = 'rb'
    # df = eda_flow_task.delay(path, mode)
    # df = pd.set_option("display.max_columns", 50)
    with adls_client.open(path, mode) as f:
        data = pd.read_csv(f, low_memory=False)
    data = data.head(50)
    json_records = data.reset_index().to_json(orient ='records')
    data = []
    data = json.loads(json_records)
    context = {'data': data}
    if request.method == 'POST':
        id_col = request.POST.get('id_col')
        target_col = request.POST.get('target_col')
        time_index_col = request.POST.get('time_index_col')
        static_cat_col_list = request.POST.getlist('static_cat_col_list')
        temporal_known_num_col_list = request.POST.getlist('temporal_known_num_col_list')
        temporal_known_cat_col_list = request.POST.getlist('temporal_known_cat_col_list')
        sort_col_list = request.POST.getlist('sort_col_list')
        amz_columns_dict = {'id_col': id_col,
                        'target_col': target_col,
                        'time_index_col': time_index_col,
                        'static_cat_col_list': static_cat_col_list,
                        'temporal_known_num_col_list':  temporal_known_num_col_list,
                        'temporal_known_cat_col_list': temporal_known_cat_col_list,
                        # 'sort_col_list': sort_col_list,
                        'wt_col': None}
        print('amz_columns_dict------>', amz_columns_dict)
        eda_object = eda.eda(col_dict=amz_columns_dict)
        save_path = '/home/'
        name_of_file = 'eda_test_local'
        file_path = os.path.join(save_path, name_of_file+".html")
        try:
            # eda_object.create_report(data=data, filename=file_path) 
            eda_object.create_report(data=data, filename=file_path) 
        except Exception as e:
            print('error is------>',e)
        return HttpResponse('eda created successfully')
    return render(request, "home/tables-simple.html", context)