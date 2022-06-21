from django.urls import path 
from . import views



urlpatterns = [
    path('accident-stats/<str:year>', views.get_accidents_stats, name='accident-stats'),
    path('accident-stats/<int:year>/range/<int:start_range>/<int:end_range>', views.get_accidents_stats_with_range, name='accident-stats-with-range'),
    path('all-bike-points', views.get_bike_points, name='all-bike-points'),
    path('journey-planner-by-points/<int:start_point>/<int:end_point>', views.get_journey_planner_by_points, name="journey-planner-by-points"),
    path('journey-planner-by-ics-code/<int:stop_point>/<int:ics_code>', views.get_journey_planner_by_ics_code, name='journey-planner-by-ics-points'),
    path('journey-planner-by-geocode/<int:lat>,<int:log>/<str:post_code>', views.get_journey_planner_by_geo_and_postcode, name='journey-planner-by-lat-and-log'),
    path('all-corridors', views.get_all_corridors, name="all-roads"),
    path('get-corridor/<str:pk>', views.get_corridor_by_id, name="get-one-corridor"),
    path('all-disrupted-roads', views.get_all_disrupted_roads, name="all-disrupted-roads"),
    path('all-serious-disrupted-roads', views.get_all_serious_disrupted_roads, name='serious-disrupted-roads'),
    path('get-one-line/<str:line>', views.get_one_line, name='get-one-line'),
]