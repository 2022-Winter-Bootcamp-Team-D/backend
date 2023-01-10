from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from store.models import Store
from .serializer import StoreJoinSerializer
from .notification import notify


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


@api_view(['POST'])
def enter_notify(request):
    # result = notify.enter_notify(request)
    notify.enter_notify(token=request.data['token'])

    return Response('호출에 성공했습니다!', status=status.HTTP_200_OK)





