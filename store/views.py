from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from store.models import Store


@api_view(['POST'])
def signin(request):
    store_name = request.data['store_name']
    phone_num = request.data['phone_num']
    address = request.data['address']
    password = request.data['password']

    try:
        Store.objects.create(store_name=store_name, phone_num=phone_num, address=address, password=password)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_201_CREATED)
