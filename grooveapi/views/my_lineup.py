from datetime import datetime, timedelta
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from grooveapi.models import GrooveUser
from grooveapi.models import my_lineup
from grooveapi.models.my_lineup import MyLineup
from grooveapi.views.show import ShowSerializer
from django.db.models import Q




class MyLineupSerializer(serializers.ModelSerializer):
    """JSON serializer for my_lineup"""
    shows=ShowSerializer(many=True)
    class Meta:
        model= MyLineup
        fields = ('id','groove_user','shows')
        depth = 2


class MyLineupView(ViewSet):
    """MyLineup View"""

    def list(self, request):
        """Handle GET requests to get all """
        

        show_date = request.query_params.get('show_date', None)
        # show_artist = request.query_params.get('artist', None)
        groove_user=GrooveUser.objects.get(user=request.auth.user)

        shows = MyLineup.objects.all()

        # shows = MyLineup.objects.all()  #.order_by('date', 'start_time')
        # if show_artist is not None:
        #     shows = shows.filter(artist_id=show_artist)
        
                
        serializer=MyLineupSerializer(shows, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handles Post for shows in my lineup"""

        groove_user=GrooveUser.objects.get(user=request.auth.user)

        my_lineup,_ = MyLineup.objects.get_or_create(
            groove_user=groove_user
        )
        my_lineup.shows.add(request.data["show_id"])
        return Response({'message': 'show added'}, status=status.HTTP_201_CREATED)

    
    def destroy(self, request, pk):
        groove_user=GrooveUser.objects.get(user=request.auth.user)
        my_lineup_show= MyLineup.objects.get(groove_user=groove_user)
        my_lineup_show.shows.remove(pk)
        return Response(None, status=status.HTTP_204_NO_CONTENT)

