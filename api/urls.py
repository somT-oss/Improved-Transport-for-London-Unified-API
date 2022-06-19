from django.urls import path 
from . import views 

urlpatterns = [
    path('accident-stats/<str:year>', views.get_accidents_stats, name='accident-stats'),
    path('accident-stats/<int:year>/range/<int:start_date>/<int:end_date>', views.get_accidents_stats_with_range, name='accident-stats-with-range'),
    path('all-bike-points', views.get_bike_points, name='all-bike-points'),
    path('journey-planner/<str:start_point>/<str:end_point>', views.get_journey_planner_by_points, name="journey-planner-by-names"),
    path('all-corridors', views.get_all_corridors, name="all-roads"),
    path('get-corridor/<str:pk>', views.get_corridor_by_id, name="get-one-corridor"),
    path('all-disrupted-roads', views.get_all_disrupted_roads, name="all-disrupted-roads"),
    path('all-serious-disrupted-roads', views.get_all_serious_disrupted_roads, name='serious-disrupted-roads'),
    path('get-one-line/<str:line>', views.get_one_line, name='get-one-line')
]