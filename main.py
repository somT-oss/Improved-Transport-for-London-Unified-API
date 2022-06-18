from gc import collect
import requests
import json
from pymongo import MongoClient


URI = 'mongodb://linroot:Zro65y7El49a93pa@lin-4624-9732.servers.'\
        'linodedb.net/?authMechanism=DEFAULT&tls=true&'\
        'tlsCAFile=/home/somtochukwu/Downloads/app-db-ca-certificate.crt'

cluster = MongoClient(URI)

global db 
db = cluster['api-db']

def get_accident_stat():
    # Gets stat of accidents in the uk in a whole year  FIXED!!!
    """
    url = f'https://api.tfl.gov.uk/AccidentStats/{2005}'
    r = requests.get(url)
    text = r.text 
    """
    #----------------------------------------------------#

    # Coversion from string to list
    """
    new_dict = json.loads(text)
    print(new_dict[1].get('id'))
    """
    #----------------------------------------------------#


    # Removing the $type key 
    """
    new_list = [ ]
    for ele in new_dict:
        del ele['$type']
        new_list.append(ele)
    """
    #--------------------------------------------------#
    # print(new_list)
    # collection.insert_many(new_list)
    # print(len(new_list))


# Gets stat for bikepoints
def get_all_bike_points():
    """    
    url = f'https://api.tfl.gov.uk/BikePoint/'
    r = requests.get(url)
    main_string = ""
    for ele in r:
        string_ele = ele.decode("utf-8")
        main_string+=string_ele

    new_list = json.loads(main_string)
    main_list = []
    for ele in new_list:
        del ele['$type']
        main_list.append(ele)

    collection2.insert_many(main_list)
    print("done")
    """

# Get bikepoints by id
def get_bike_points_by_id():
    """
    bike_point_id = "BikePoints_1"

    result = collection2.find_one({"id": bike_point_id})
    print(result)
    """


# Gets Journey planner
def get_journey_planner_by_name():
    """
    start_point = "westminster"
    end_point = "bank"
    url = f'https://api.tfl.gov.uk/journey/journeyresults/{start_point}/to/{end_point}'
    r = requests.get(url)
    text = r.text 
    new_dict = json.loads(text)
    print(new_dict)
    """

#  Get Journey planner ICS code
def get_journey_planner_by_ics_code():
    """ 
    start_code = '1000266'
    end_code = '1000013'
    url = f'https://api.tfl.gov.uk/journey/journeyresults/{start_code}/to/{end_code}'
    r = requests.get(url)
    text = r.text 
    new_dict = json.loads(text)
    print(new_dict)
    """

# Get Journey planner Geo and PostCode
def get_journet_planner_by_geo_and_postcode():
    """
    lat = 51.501
    log = -0.123
    post_code = 'n225nb'
    url = f"https://api.tfl.gov.uk/journey/journeyresults/{lat},{log}/to/{post_code}"
    r = requests.get(url)
    text = r.text 
    new_dict = json.loads(text)
    print(new_dict)
    """

# Make new Collection for All Corridors
def get_all_coridors():
    """
    url = 'https://api.tfl.gov.uk/Road'
    r = requests.get(url)
    text = r.text
    new_list = json.loads(text)
    """

# Get corridor by id
def get_corridor_by_id():
    """
    url = 'https://api.tfl.gov.uk/Road/A2'
    r = requests.get(url)
    text = r.text
    new_list = json.loads(text)
    """

# Gets all disrupted roads
def get_disrupted_roads():
    """
    url = 'https://api.tfl.gov.uk/Road/All/Disruption/'
    r = requests.get(url)
    text = r.text
    new_list = json.loads(text)
    """

# Get Road Disruption by Corridor id
def get_road_disruption_by_corridor_id():
    """
    corridor_id = 'A2'
    url = 'https://api.tfl.gov.uk/Road/{corridor_id}/Disruption'
    r = requests.get(url)
    text = r.text
    new_dict = json.loads(text)
    """

# Get Road Disruptions by severity 
def get_road_diruptions_by_severity():
    """
    url = "https://api.tfl.gov.uk/Road/All/Disruption?severities=Serious"
    r = requests.get(url)
    text = r.text
    new_list = json.loads(text)
    """

# Get Lines by id
def get_lines_by_id():
    """
    line = "victoria"
    url = f"https://api.tfl.gov.uk/Line/{line}"
    r = requests.get(url)
    text = r.text
    new_list = json.loads(text)
    """

# line = "victoria"
# url = f"https://api.tfl.gov.uk/Line/{line}/Status"
# r = requests.get(url)
# text = r.text
# new_list = json.loads(text)


url = f'https://api.tfl.gov.uk/AccidentStats/{2005}'
r = requests.get(url)
print(r.headers)
# text = r.text 
# new_dict = json.loads(text)
# print(new_dict[0:12])

