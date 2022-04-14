from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import (AnonRateThrottle, ScopedRateThrottle,
                                       UserRateThrottle)
from rest_framework.views import APIView
from showlist.api.pagination import ShowListPagination
from showlist.api.permissions import IsAdminOrReadOnly, IsReviewOwnerOrReadOnly
from showlist.api.serializers import (ReviewSerializer, ShowListSerializer,
                                      StreamPlatformSerializer)
from showlist.api.throttling import CreateReviewThrottle, ReviewListThrottle
from showlist.models import Review, ShowList, StreamPlatform


class UserReviewView(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [ReviewListThrottle, AnonRateThrottle]

    # Filtering against the URL
    # def get_queryset(self):
    #     username = self.kwargs['username']
    #     return Review.objects.filter(author__username=username)
    # ...

    # Filtering against query parameters
    def get_queryset(self):
        username = self.request.query_params.get('username')
        return Review.objects.filter(author__username=username)
    # ...


# using Concrete View Classes
# ReviewCreateView
class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [CreateReviewThrottle]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        show = ShowList.objects.get(pk=pk)
        author = self.request.user
        queryset = Review.objects.filter(show_list=show, author=author)

        if queryset.exists():
            raise ValidationError(
                "You have already reviewed this show")

        if show.total_ratings == 0:
            show.average_rating = serializer.validated_data['rating']

        else:
            show.average_rating = (
                show.average_rating + serializer.validated_data['rating']) / 2

        show.total_ratings += 1
        show.save()

        serializer.save(show_list=show, author=author)
# ...


# ReviewListView
class ReviewListView(generics.ListAPIView):
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Review.objects.filter(show_list=pk)

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['author__username', 'is_valid']
# ...


# ReviewDetailsView
class ReviewDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewOwnerOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'
# ...


# ShowListView for testing django-filter, search
class ShowListViewDF(generics.ListAPIView):
    queryset = ShowList.objects.all()
    serializer_class = ShowListSerializer
    pagination_class = ShowListPagination

    # filter_backends = [filters.SearchFilter]
    # search_fields = ['title', 'platform__name']

    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['title', 'platform__name']

    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['average_rating', 'total_ratings']
# ...


# using class based views (APIView)
# ShowListView
class ShowListView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):

        try:
            show = ShowList.objects.all()
            serializer = ShowListSerializer(show, many=True)

            return Response(serializer.data)

        except ShowList.DoesNotExist:
            return Response(
                {'error': 'show list does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )

    def post(self, request):
        serializer = ShowListSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# ...


# ShowDetailsView
class ShowDetailsView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get_object(self, pk):
        try:
            return ShowList.objects.get(pk=pk)

        except ShowList.DoesNotExist:
            return None

    def get(self, request, pk):
        show = self.get_object(pk)

        if show != None:
            serializer = ShowListSerializer(show)
            return Response(serializer.data)

        else:
            return Response(
                {'error': f'Show with id: {pk} does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, pk):
        show = self.get_object(pk)

        if show != None:
            serializer = ShowListSerializer(show, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(
                {'error': f'Show with id: {pk} does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, pk):
        show = self.get_object(pk)

        if show != None:
            show.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            return Response(
                {'error': f'Show with id: {pk} does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )
# ...


# StreamPlatformView using ModelViewSet
class StreamPlatformViewVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = [IsAdminOrReadOnly]
# ...


# StreamPlatformView
class StreamPlatformView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        try:
            platform = StreamPlatform.objects.all()
            serializer = StreamPlatformSerializer(platform, many=True)

            return Response(serializer.data)

        except StreamPlatform.DoesNotExist:
            return Response(
                {'error': 'stream platform does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )

    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# ...


# StreamPlatformDetailsView
class StreamPlatformDetailsView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get_object(self, pk):
        try:
            return StreamPlatform.objects.get(pk=pk)

        except StreamPlatform.DoesNotExist:
            return None

    def get(self, request, pk):
        platform = self.get_object(pk)

        if platform != None:
            serializer = StreamPlatformSerializer(platform)
            return Response(serializer.data)

        else:
            return Response(
                {'error': f'Stream platform with id: {pk} does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, pk):
        platform = self.get_object(pk)

        if platform != None:
            serializer = StreamPlatformSerializer(platform, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(
                {'error': f'Stream platform with id: {pk} does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, pk):
        platform = self.get_object(pk)

        if platform != None:
            platform.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            return Response(
                {'error': f'Stream platform with id: {pk} does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )
# ...


# using @api_view decorator to define the views
"""

@api_view(['GET', 'POST'])
def movie_list(request):

    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = MovieSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def movie_details(request, pk):

    try:
        movie = Movie.objects.get(pk=pk)
    except Movie.DoesNotExist:
        return Response(
            {'error': f'Movie with id: {pk} does not exist'},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        serializer = MovieSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = MovieSerializer(movie, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

"""
