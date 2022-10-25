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
        

        # show_date = request.query_params.get('show_date', None)
        groove_user=GrooveUser.objects.get(user=request.auth.user)
        search = self.request.query_params.get('search', None)

        lineup = MyLineup.objects.filter(groove_user=groove_user)

        serializer=MyLineupSerializer(lineup, many=True)
        if search is not None:
            shows = lineup[0].shows.filter(
                Q(artist__artist_name__icontains=search) |
                Q(stage__stage_name__icontains=search) |
                Q(start_time__icontains=search)
            )
            show_serializer=ShowSerializer(shows, many=True)
            serializer.data[0]['shows']=show_serializer.data
        
                
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

