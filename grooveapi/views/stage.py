from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from grooveapi.models import Stage


class StageSerializer(serializers.ModelSerializer):
    """JSON serializer for stages"""
    class Meta:
        model = Stage
        fields = ('id', 'stage_name')
        depth = 2


class StageView(ViewSet):
    """groove stage view"""

    def list(self, request):
        """Handle GET requests to get all stages

        Returns:
            Response -- JSON serialized list of stages
        """
        stages = Stage.objects.all()
        serializer = StageSerializer(stages, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """Handles GET requests for a single stage
        Returns:
            Response -- JSON serialized stage"""
        try:
            stage = Stage.objects.get(pk=pk)
            serializer = StageSerializer(stage)
            return Response(serializer.data)
        except Stage.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized stage instance
        """
        stage = Stage.objects.create(
            stage_name=request.data["stage_name"]
        )

        serializer = StageSerializer(stage)
        return Response(serializer.data)

    def destroy(self, request, pk):
        stage = Stage.objects.get(pk=pk)
        stage.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)