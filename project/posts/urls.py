from django.urls import path
from . import views
from . import user_views
urlpatterns = [
    path('iternary-details/', views.IternaryDetails.as_view(), name="iternary-details"),
    path('add-destination/', views.AddDestinationView.as_view(), name='add-destination'),
    path('iternary-destinations/<slug:id>', views.GetAllDestinationsDetails.as_view(), name='all-destination-details'),
    path('destination-details/<slug:id>', views.GetDestinationDetails.as_view(), name='destination-details'),
    path('destination-accomodations/<slug:id>', views.AllAccomodationDetails.as_view(), name='all-accomodation-details'),
    path('accomodation-details/<slug:id>', views.AccomodationDetails.as_view(), name='accomodation-details'),
    path('add-accomodation/', views.AddAccomodation.as_view(), name="add-accomodation"),
    path('add-media/', views.MediaAPIView.as_view(), name = "add-media"),
    path('iternary-media/<slug:id>', views.GetIternaryMediaAPIView.as_view(), name = "iternary-media"),
    path('media/<slug:id>', views.GetMediaAPIView.as_view(), name = "get-media"),
    
    path('search/travellor', user_views.SearchTravellor.as_view(), name = "search-travellor"),
    path('search/iternary', user_views.SearchIternary.as_view(), name = "search-iternary"),
    path('view-travellor/<slug:id>', user_views.FetchTravellorDetails.as_view(), name = "view-travellor-profile"),
    path('travellor/iternaries', user_views.FetchTravellorIternaries.as_view(), name = "view-travellor-iternaries"),

    path('', user_views.GetAllIternariesAPIView.as_view(), name = "view-iternaries"),
    
    

]