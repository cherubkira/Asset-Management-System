from rest_framework.decorators import api_view
from rest_framework.response import Response
from asset1.models import Asset
from .serializers import AssetSerializer
from rest_framework import status


@api_view(['GET'])
def getRoutes(request):

    routes = [
        {'GET': '/api'},
        {'GET': '/api/assets/'},
        {'GET': '/api/assets/<id>/'},
    ]
    return Response(routes)

@api_view(['GET'])
def getAssets(request,pk):
    
    try:
        asset =  Asset.objects.get(pk = id)
    except Asset.DoesNotExist:
        return Response(status  = status.HTTP_404_NOT_FOUND)
    
    asset = Asset.objects.all()
    serializer = AssetSerializer(asset, many=True)
    return Response(serializer.data)