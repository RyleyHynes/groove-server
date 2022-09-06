from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from grooveapi.models.artist import Artist


class ArtistSerializer(serializers.ModelSerializer):
    """JSON serializer for reactions"""
    class Meta:
        model = Artist
        fields = ('id','artist_name', 'genre', 'artist_description', 'artist_image')


class ArtistView(ViewSet):
    """Artist View"""

    def retrieve(self, request, pk):
        """Handle GET requests for single Artist
        Returns:
            Response -- JSON serialized Artist"""
        try:
            artist = Artist.objects.get(pk=pk)
            serializer = ArtistSerializer(artist)
            return Response(serializer.data)
        except Artist.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all artists
        
        Returns:
            Response -- JSON serialized list of artists"""

        artists = Artist.objects.all()
        artist_show = request.query_params.get('show', None)
        if artist_show is not None:
            artists = artists.filter(show_id=artist_show)
        serializer = ArtistSerializer(artists, many = True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations
        
        Returns:
            Response -- JSON serialized artist instance
            """
        artist = Artist.objects.create(
            artist_name=request.data["artist_name"],
            genre = request.data["genre"],
            artist_description = request.data["artist_description"],
            artist_image = request.data["artist_image"]
        )

        serializer= ArtistSerializer(artist)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    
    def update(self, request, pk):
        """Handle PUT requests for a reaction
        
        Returns: 
            Response -- Empty body with 204 status code
            """
        artist= Artist.objects.get(pk=pk)
        artist.artist_name = request.data["artist_name"]
        artist.genre=request.data["genre"]
        artist.artist_description=request.data["artist_description"]
        artist.artist_image = request.data["artist_image"]

        artist.save()
        return Response(None, status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        artist = Artist.objects.get(pk=pk)
        artist.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)