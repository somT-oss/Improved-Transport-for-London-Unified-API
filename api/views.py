from rest_framework.decorators import api_view
from django.views.decorators.cache import cache_page
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
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


year = openapi.Parameter('test', openapi.IN_QUERY, description="year parameter for accident stats", type=openapi.TYPE_STRING)
@swagger_auto_schema(method='GET', manual_parameters=[year])
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


year = openapi.Parameter('year', openapi.IN_QUERY, description="year parameter for accident stats", type=openapi.TYPE_STRING)
start_range = openapi.Parameter('start_range', openapi.IN_QUERY, description='start range of data in a year\'s accident stat', type=openapi.TYPE_INTEGER)
end_range = openapi.Parameter('end_range', openapi.IN_QUERY, description='end range of data in a year\'s accident stat', type=openapi.TYPE_INTEGER)
@swagger_auto_schema(method='GET', manual_parameters=[year, start_range, end_range])
@cache_page(60*15)
@api_view(['GET'])
def get_accidents_stats_with_range(request, year, start_range, end_range):
    if request.method != 'GET':
        return Response({"Error": "Invalid Response Type"})
    url = f'https://api.tfl.gov.uk/AccidentStats/{year}'
    r = requests.get(url)
    if r.status_code != 200:
        return Response({"Message": f"No AccidentStats for the year {year}"})
    text = r.text 
    main_list = json.loads(text)

    return Response(main_list[start_range:(end_range+1)])


@swagger_auto_schema(method='GET')
@cache_page(60*60)
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
def get_bike_point_id(request, bike_point_id):
    connect_to_mongo()
    if request.method != 'GET':
        return Response({"Error": "Invalid Request Type"}, status=status.HTTP_400_BAD_REQUEST)
    cursor = db['bike-point']
    bike_point = cursor.find_one({"id": bike_point_id})
    if bike_point == None:
        return Response({"Message": f"Could not get BikePoint with id {bike_point_id}"}, status=status.HTTP_200_OK)
    bike_point.pop('_id')
    return Response(bike_point, status=status.HTTP_200_OK)



start_point = openapi.Parameter('start_pint', openapi.IN_QUERY, description='start point of your journey', type=openapi.TYPE_NUMBER)
end_point = openapi.Parameter('end_point', openapi.IN_QUERY, description='end point of your journey', type=openapi.TYPE_NUMBER)
@swagger_auto_schema(method='GET', manual_parameters=[start_point, end_point])
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


start_code = openapi.Parameter('start_code', openapi.IN_QUERY, description='start code of your journey', type=openapi.TYPE_NUMBER)
end_code = openapi.Parameter('end_code', openapi.IN_QUERY, description='end code of your journey', type=openapi.TYPE_NUMBER)
@swagger_auto_schema(method='GET', manual_parameters=[start_code, end_code])
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

 
lat = openapi.Parameter('lat', openapi.IN_QUERY, description='latitude point of your journey', type=openapi.TYPE_NUMBER)
log = openapi.Parameter('log', openapi.IN_QUERY, description='longitude point of journey', type=openapi.TYPE_NUMBER)
@swagger_auto_schema(method='GET', manual_parameters=[lat, log])
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


pk = openapi.Parameter('pk', openapi.IN_QUERY, description="id of corridor", type=openapi.TYPE_STRING)
@swagger_auto_schema(method='GET', manual_parameters=[pk])
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


@swagger_auto_schema(method='GET')
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


@swagger_auto_schema(method='GET')
@cache_page(60*60)
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

line = openapi.Parameter('line', openapi.IN_QUERY, description="a specific London line", type=openapi.TYPE_STRING)
@swagger_auto_schema(method='GET', manual_parameters=[line])
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