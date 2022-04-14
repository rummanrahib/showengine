from django.urls import include, path
from rest_framework.routers import DefaultRouter
from showlist.api.views import (ReviewCreateView, ReviewDetailsView,
                                ReviewListView, ShowDetailsView, ShowListView, ShowListViewDF,
                                StreamPlatformDetailsView, StreamPlatformView,
                                StreamPlatformViewVS, UserReviewView)

# from showlist.api.views import movie_details, movie_list

# ViewSet router
router = DefaultRouter()
router.register('stream-platforms', StreamPlatformViewVS,
                basename='stream_platforms')
# ...

urlpatterns = [
    path('show-list/', ShowListView.as_view(), name='show_list'),
    path('test-show-list/', ShowListViewDF.as_view(), name='test_show_list'),
    path('show-list/<int:pk>/', ShowDetailsView.as_view(), name='show_details'),

    path('', include(router.urls)),
    # path('stream-platforms/', StreamPlatformView.as_view(), name='stream_platforms'),
    # path('stream-platforms/<int:pk>/',
    #      StreamPlatformDetailsView.as_view(), name='stream_platforms_details'),

    # path('reviews/', ReviewListView.as_view(), name='review_list'),
    # path('reviews/<int:pk>/', ReviewDetailsView.as_view(), name='review_details'),

    path('show-list/<int:pk>/create-review/',
         ReviewCreateView.as_view(), name='create_review'),
    path('show-list/<int:pk>/reviews/',
         ReviewListView.as_view(), name='review_list'),
    path('show-list/reviews/<int:pk>/',
         ReviewDetailsView.as_view(), name='review_details'),
    path('show-list/reviews/',
         UserReviewView.as_view(), name='user_review_details'),
]
