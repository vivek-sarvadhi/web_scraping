from django.urls import path
from myapp.views import (IndexAPIView, WebScrapeAPIView, WebScrapeFreelancerAPIView)


urlpatterns = [
    path('', IndexAPIView.as_view(), name='index'),
    path('content', WebScrapeAPIView.as_view(), name='webscrape'),
    path('freelancer', WebScrapeFreelancerAPIView.as_view(), name='freelancer'),
]