# London-Unified-API-V2

I came across an API from [**Transport for London Unified API**](https://api.tfl.gov.uk/) that gives insightfull data for transportation in London.

However, upon using this API, I found out that it did not return the normal ```json``` response types, instead it returned other data types like ```bytes``` and ```strings```.

I then decided to build off of this API, making it more developer friendly.

## Overview

This is an ope source project, aimed at improving the API from [**Transport for London Unified API**](https://api.tfl.gov.uk/), i.e correcting as much incorrect response types. It is open to contributions of any kind.

You can checkout my blog post where I described my thought process on how I handled building some endpoints, and other delicate aspects of this project

## Tooling 
 - Django rest framework 
 - MongoDB 
 - Django rest framework simplejwt (Token Authentication)
 - Postman
 - Linode Linux server

## API Endpoints 

Here are some of the endpoints I have worked on
 - Get Yearly Accident Stats ```http://172.105.148.112/v2/api/accident-stats/{year}```
 - Get Yearly Accident Stats with range ```http://172.105.148.112/v2/api/accident-stats/{year}/range/{star t_range}/{end_range}```
 - GetAll BikePoints ```http://172.105.148.112/v2/api/all-bike-points```
 - Get One BikePoint ```http://172.105.148.112/v2/api/get-one-bike-point/{bike_pont_id}```

**This project is in line for the [Linode](https://cloud.linode.com) X [Hashnode](https://hashnode.com) Hackathon**