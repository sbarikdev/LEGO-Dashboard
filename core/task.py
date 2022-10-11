# from __future__ import absolute_import
# from celery import shared_task
# from time import sleep
# from azure.datalake.store import core, lib, multithread
# from django.core.mail import send_mail
# import pandas as pd
# # token = lib.auth()
# # adls_client = core.AzureDLFileSystem(token, store_name='bnlweda04d80242stgadls')

# @shared_task
# def sleepy(duration):
#     sleep(duration)
#     return None
    
# @shared_task
# def send_email_task(subject,message,from_email,recipient_email,fail_silently):
#     sleep(30)
#     send_mail(
#         subject,message,from_email,recipient_email,fail_silently
#     )
#     return 'Mail sent success'
    
# # response_dict = {}

# # @shared_task
# # def eda_flow_task(path, mode):
# #     sleep(30)
# #     try:
# #         with adls_client.open(path, mode) as f:
# #             df = pd.read_csv(f, low_memory=False)
# #             print('inside while loop')
# #         print('data loaded in task')
# #         return 'data load success'
# #     except Exception as e:
# #         response_dict.update({'error': str(e)})