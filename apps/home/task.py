from __future__ import absolute_import,unicode_literals
from celery import shared_task
from time import sleep
import os
import eda, ctfrv2
from pathlib import Path
import pandas as pd
import uuid
env = 'LOCAL'

@shared_task
def async_task(amz_columns_dict,file_name,username,data2):
    sleep(10)
    data = pd.DataFrame(data2)
    eda_object = eda.eda(col_dict=amz_columns_dict)
    import os
    from core.settings import BASE_DIR
    if env == 'LOCAL':
        download_path = os.path.join(BASE_DIR, "projects/eda/%s/" % username)
    else:
        pass
        # download_path = ('/Unilever/satyajit/projects/eda/%s/' % username)
        # with adls_client.open('/Unilever/satyajit/projects/eda/%s/' % username, 'wb') as o:
        #     o.write(str.encode(output_str))
        #     o.close()
    download_path = str(download_path)
    if env == 'LOCAL' and not os.path.exists(download_path):
        try:
            os.makedirs(download_path)
            print('folder created----->')
        except FileExistsError:
        # directory already exists
            pass
    elif env == 'REMOTE' and not os.path.exists(download_path):
        print('remote')
        pass
    uuid_no=uuid.uuid4().hex[:5]
    name_of_file =  file_name + '_' + str(uuid_no)         
    save_path = download_path 
    if env == 'LOCAL':
        file_path = os.path.join(save_path, name_of_file+".html")
    else:
        # file_path = os.path.join(save_path, name_of_file+".html")
        # output_str = data.to_csv(mode = 'w', index=False)
        # with adls_client.open('/Unilever/satyajit/', 'wb') as o:
        #     o.write(str.encode(output_str))
        #     o.close()
        file_path = None
        print('adls path create')
        pass
    eda_object.create_report(data=data, filename=file_path)
    return 'eda task complete'


@shared_task
def async__training_task(amz_columns_dict,promo_num_cols,metric,learning_rate,num_layers,
            num_heads,kernel_sizes,d_model,forecast_horizon,loss_type,max_inp_len,num_quantiles,decoder_lags,
            dropout_rate,max_epochs,min_epochs,train_steps_per_epoch,test_steps_per_epoch,patience,
            window_len,fh,batch,min_nz,PARALLEL_DATA_JOBS,PARALLEL_DATA_JOBS_BATCHSIZE,username, data2):
    sleep(10)
    data = pd.DataFrame(data2)
    df = data.head(1500)
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
        import os
        from core.settings import BASE_DIR
        download_path = os.path.join(BASE_DIR, "projects/training/%s/" % username)
        if not os.path.exists(download_path):
            try:
                os.makedirs(download_path)
                print('folder created----->')
            except FileExistsError:
            # directory already exists
                pass
        download_path = str(download_path)
        print('download_path------------->', download_path)
        uuid_no=uuid.uuid4().hex[:6]
        name_of_file =  str(uuid_no)         
        save_path = download_path
        # file_path = Path(save_path, name_of_file+".html")  
        file_path = os.path.join(save_path, name_of_file) 

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
                    model_prefix=file_path,
                    logdir=file_path)
        print('before train model build successfully---------------->')
        var_model.model.summary()
        print('after train model build successfully---------------->')
    except Exception as e:
        print('training_model error is: {}'.format(e))
    return 'training task complete'




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