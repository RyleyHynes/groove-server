from dataclasses import fields
from datetime import datetime, timedelta
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from grooveapi.models import Show, Artist, GrooveUser
from django.db.models import Q


from grooveapi.models.stage import Stage


class ShowSerializer(serializers.ModelSerializer):
    """JSON serializer for posts
    """

    class Meta:
        model = Show
        fields = ('id', 'artist', 'stage', 'date', 'start_time', 'end_time',
                  'readable_start_time', 'readable_end_time', 'get_lineup_day')
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

        show_date = request.query_params.get('show_date', None)
        search = self.request.query_params.get('search', None)
        shows = Show.objects.all().order_by('date', 'start_time')
        if show_artist is not None:
            shows = shows.filter(artist_id=show_artist)

        if show_date is not None:
            show_date_date_time = datetime(int(show_date[0:4]), int(
                show_date[5:7]), int(show_date[8:10]))
            tomorrow = show_date_date_time+timedelta(days=1)
            shows = shows.filter(
                Q(date=show_date) | Q(date=tomorrow, start_time__hour__in=(0, 1, 2)))

        serializer = ShowSerializer(shows, many=True)
        if search is not None:
            schedule = shows.filter(
                Q(artist__artist_name__contains=search) |
                Q(stage__stage_name__contains=search) |
                Q(start_time__contains=search)
            )
            schedule_serializer=ShowSerializer(schedule, many=True)
            serializer.data[0]['shows']=schedule_serializer.data
        
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response --JSON serialized show instance
            """

        artist = Artist.objects.get(pk=request.data["artist"])
        stage = Stage.objects.get(pk=request.data["stage"])
        show = Show.objects.create(
            artist=artist,
            stage=stage,
            date=request.data["date"],
            start_time=request.data["start_time"]
        )

        serializer = ShowSerializer(show)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a show

        Returns:
            Response -- Empty body with 204 status code
            """
        artist = Artist.objects.get(pk=request.data["artist"]["id"]) #because its coming back as an object
        stage = Stage.objects.get(pk=request.data["stage"])

        show = Show.objects.get(pk=pk)
        show.artist = artist
        show.stage = stage
        show.date = request.data["date"]
        show.start_time = request.data["start_time"]

        show.save()

        return Response(None, status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        show = Show.objects.get(pk=pk)
        show.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
