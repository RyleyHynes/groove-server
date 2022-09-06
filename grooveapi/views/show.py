from dataclasses import fields
from datetime import datetime, timedelta
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from grooveapi.models import Show, Artist, GrooveUser
from django.db.models import Q
from django.core.files.base import ContentFile


from grooveapi.models.stage import Stage


class ShowSerializer(serializers.ModelSerializer):
    """JSON serializer for posts
    """

    class Meta:
        model = Show
        fields = ('id', 'artist', 'stage', 'date', 'start_time')
        depth = 2


class ShowView(ViewSet):
    """Show View"""

    def retrieve(self, request, pk):
        """Handle GET requests for single post

        Returns:
            Response -- JSON serialized show
            """
        try:
            show = Show.objects.get(pk=pk)
            serializer = ShowSerializer(show)
            return Response(serializer.data)
        except Show.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all shows

        Returns:
        Response -- JSON serialized list of shows
        """

        show_artist = request.query_params.get('artist', None)
        
        # start_date = request.query_params.get('start_date', None)
        # end_date = request.query_params.get('end_date', None)
        show_date = request.query_params.get('show_date', None)

        show_date_date_time = datetime(int(show_date[0:4]), int(
            show_date[5:7]), int(show_date[8:10]))
        tomorrow = show_date_date_time+timedelta(days=1)
        print(show_date_date_time.year)
        # shows = Show.objects.all().order_by('date').filter(date__range=[start_date, end_date] | )
        shows = Show.objects.all().order_by('date','start_time',).filter(
            Q(date=show_date)|Q(date=tomorrow,start_time__hour__in=(1,2)))
        if show_artist is not None:
            shows=shows.filter(artist_id=show_artist)
        serializer=ShowSerializer(shows, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response --JSON serialized show instance
            """

        artist=Artist.objects.get(pk=request.data["artist"])
        stage=Stage.objects.get(pk=request.data["stage"])
        show=Show.objects.create(
            artist=artist,
            stage=stage,
            date=request.data["date"],
            start_time=request.data["start_time"]
        )

        serializer=ShowSerializer(show)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a show

        Returns:
            Response -- Empty body with 204 status code
            """
        show=Show.objects.get(pk=pk)
        show.artist=request.data["artist"]
        show.stage=request.data["stage"]
        show.date=request.data["date"]
        show.start_time=request.data["start_time"]

        show.save()

        return Response(None, status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        show=Show.objects.get(pk=pk)
        show.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
