from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from pymongo import MongoClient
import requests
import json 


URI = 'mongodb://linroot:Xk4PjRNWIUe26Lqb@lin-4605-9707.servers.'\
    'linodedb.net/?authMechanism=DEFAULT&tls=true&'\
    'tlsCAFile=/home/somtochukwu/Downloads/app-db-ca-certificate.crt'

cluster = MongoClient(URI)
global db 
db = cluster['api-db']

@api_view(['GET'])
def get_accidents_stats(request, year):
    if request.method != 'GET':
        return Response({"Error": "Invalid Response Type"})
    url = f'https://api.tfl.gov.uk/AccidentStats/{year}'
    r = requests.get(url)
    text = r.text 
    main_list = json.loads(text)
    
    return Response(main_list)

@api_view(['GET'])
def get_accidents_stats_with_range(request, year, start_date, end_date):
    if request.method != 'GET':
        return Response({"Error": "Invalid Response Type"})
    url = f'https://api.tfl.gov.uk/AccidentStats/{year}'
    r = requests.get(url)
    text = r.text 
    main_list = json.loads(text)

    return Response(main_list[start_date:(end_date+1)])