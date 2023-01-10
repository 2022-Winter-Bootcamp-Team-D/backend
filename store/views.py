from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from store.models import Store
from waiting.models import Waiting
from .serializer import StoreJoinSerializer
from .serializer import StoreBreaktimeSerializer
from .serializer import StoreDetailSerializer
from .serializer import StoreWaitingsSerializer


@api_view(['POST'])
def signin(request):
    store_name = request.data['store_name']
    phone_num = request.data['phone_num']
    latitude = request.data['latitude']
    longitude = request.data['longitude']
    password = request.data['password']

    try:
        object = Store.objects.create(store_name=store_name, phone_num=phone_num, latitude=latitude, longitude=longitude,
                                      password=password)
        response = StoreJoinSerializer(object)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(data=response.data, status=status.HTTP_201_CREATED)


@api_view(['PATCH'])
def breaktime(request):
    store_id = request.data['store_id']

    try:
        object = Store.objects.get(store_id=store_id)
        object.is_waiting = not object.is_waiting
        object = object.save()

    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)


@api_view(['PATCH'])
def detail(request):
    store_id = request.data['store_id']
    information = request.data['information']

    try:
        object = Store.objects.get(store_id=store_id)
        object.information = information
        object = object.save()

    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def waitings(request):
    store_id = request.data['store_id']

    try:
        object = Store.objects.get(store_id=store_id)
        object = Waiting.objects.filter(store_id=object, status='WA')

        response = StoreWaitingsSerializer(object)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)
