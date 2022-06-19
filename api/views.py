from django.shortcuts import render
from pip import main
from rest_framework.decorators import api_view
from django.views.decorators.cache import cache_page
from rest_framework.response import Response
from rest_framework import status
from pymongo import MongoClient
import requests
import json 



def connect_to_mongo():
    URI = 'mongodb://linroot:Zro65y7El49a93pa@lin-4624-9732.servers.'\
        'linodedb.net/?authMechanism=DEFAULT&tls=true&'\
        'tlsCAFile=./app-db-ca-certificate.crt'

    cluster = MongoClient(URI)
    global db
    db = cluster['api-db']
    print("Connected to mongo successfully")


@cache_page(60*15)
@api_view(['GET'])
def get_accidents_stats(request, year):
    connect_to_mongo()
    if request.method != 'GET':
        return Response({"Error": "Invalid Response Type"})
    cursor_list = [cursor for cursor in db.list_collection_names()]
    print(cursor_list)
    if year not in cursor_list:
        return Response({"Message": f"There is no accident stat in the year {year}"}, status=status.HTTP_400_BAD_REQUEST)
    main_cursor = db[f'{year}']
    main_list = []
    for ele in main_cursor.find({}):
        del ele['_id']
        main_list.append(ele)
    return Response(main_list)


@cache_page(60*15)
@api_view(['GET'])
def get_accidents_stats_with_range(request, year, start_date, end_date):
    if request.method != 'GET':
        return Response({"Error": "Invalid Response Type"})
    url = f'https://api.tfl.gov.uk/AccidentStats/{year}'
    r = requests.get(url)
    if r.status_code != 200:
        return Response({"Message": f"No AccidentStats for the year {year}"})
    text = r.text 
    main_list = json.loads(text)

    return Response(main_list[start_date:(end_date+1)])


@cache_page(60*15)
@api_view(['GET'])
def get_bike_points(request):
    if request.method != 'GET':
        return Response({"Error": "Invalid Request Type"})
    connect_to_mongo()
    cursor = db['bike-point']
    main_list = []
    for ele in cursor.find({}):
        del ele['_id']
        main_list.append(ele)
    
    return Response(main_list, status=status.HTTP_200_OK)


@cache_page(60*15)
@api_view(['GET'])
def get_bike_point_id():
    pass 


@cache_page(60*15)
@api_view(['GET'])
def get_journey_planner_by_points(request, start_point, end_point):
    if request.method != 'GET':
        return Response({"Error": "Invalid Request Type"}, status=status.HTTP_400_BAD_REQUEST)
    url = f'https://api.tfl.gov.uk/journey/journeyresults/{start_point}/to/{end_point}'
    r = requests.get(url)
    if r.status_code != 200:
        return Response({"Error": f"Could not get information on how to plan a route from {start_point} to {end_point}"}, status=status.HTTP_200_OK)
    text = r.text 
    new_dict = json.loads(text)
    
    return Response(new_dict, status=status.HTTP_200_OK)


@cache_page(60*15)
@api_view(['GET'])
def get_journey_planner_by_ics_code(request, start_code, end_code):
    if request.method != 'GET':
        return Response({"Error": "Invalid Request Type"}, status=status.HTTP_400_BAD_REQUEST)
    url = f'https://api.tfl.gov.uk/journey/journeyresults/{start_code}/to/{end_code}'
    r = requests.get(url)
    if r.status_code != 200:
        return Response({"Error": f"Could not get information on how to plan a route from {start_code} to {end_code}"}, status=status.HTTP_200_OK)
    text = r.text 
    new_dict = json.loads(text)
    
    return Response(new_dict, status=status.HTTP_200_OK)


@cache_page(60*15)
@api_view(['GET'])
def get_journey_planner_by_geo_and_postcode(request, lat, log):
    if request.method != 'GET':
        return Response({"Error": "Invalid Request Type"}, status=status.HTTP_400_BAD_REQUEST)
    url = f'https://api.tfl.gov.uk/journey/journeyresults/{lat}/to/{log}'
    r = requests.get(url)
    if r.status_code != 200:
        return Response({"Error": f"Could not get information on how to plan a route from {lat} to {log}"}, status=status.HTTP_200_OK)
    text = r.text 
    new_dict = json.loads(text)

    return Response(new_dict, status=status.HTTP_200_OK)


@cache_page(60*15)
@api_view(['GET'])
def get_all_corridors(request):
    connect_to_mongo()
    if request.method != 'GET':
        return Response({"Error": "Invalid Request Type"}, status=status.HTTP_400_BAD_REQUEST)
    
    cursor = db['roads']
    main_list = []
    for ele in cursor.find({}):
        del ele['_id']
        main_list.append(ele)
    return Response(main_list, status=status.HTTP_200_OK)


@cache_page(60*15)
@api_view(['GET'])
def get_corridor_by_id(request, pk):
    connect_to_mongo()
    if request.method != 'GET':
        return Response({"Error": "Invalid Request Type"}, status=status.HTTP_400_BAD_REQUEST)
    cursor = db['roads']
    corridor = cursor.find_one({"displayName": pk})
    if corridor == None:
        return Response({"Message": f"Could not get Corridor with id {pk}"}, status=status.HTTP_200_OK)
    corridor.pop('_id')
    return Response(corridor, status=status.HTTP_200_OK)


@cache_page(60*15)
@api_view(['GET'])
def get_all_disrupted_roads(request):
    connect_to_mongo()
    if request.method != 'GET':
        return Response({"Error": "Invalid Request Type"}, status=status.HTTP_400_BAD_REQUEST)
    cursor = db['disrupted-roads']
    main_list = []
    for documents in cursor.find({}):
        del documents['_id']
        main_list.append(documents)

    return Response(main_list, status=status.HTTP_200_OK)



@cache_page(60*15)
@api_view(['GET'])
def get_all_serious_disrupted_roads(request):
    if request.method != 'GET':
        return Response({"Error": "Invalid Request Type"}, status=status.HTTP_400_BAD_REQUEST) 
    url = "https://api.tfl.gov.uk/Road/All/Disruption?severities=Serious"
    r = requests.get(url)
    if r.status_code != 200:
        return Response({"Error": "An error occured, try again"}, status=status.HTTP_200_OK)
    text = r.text
    new_list = json.loads(text)

    return Response(new_list, status=status.HTTP_200_OK)


@cache_page(60*15)
@api_view(['GET'])
def get_one_line(request, line):
    if request.method != 'GET':
        return Response({"Error": "Invalid Request Type"}, status=status.HTTP_400_BAD_REQUEST)
    url = f"https://api.tfl.gov.uk/Line/{line}"
    r = requests.get(url)
    text = r.text
    new_list = json.loads(text)

    return Response(new_list, status=status.HTTP_200_OK)