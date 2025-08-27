from django.contrib.gis.geos.prototypes import create_linearring
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from main.models import CustomUser
from main.serializers import CustomUserSerializer


class ClientsListView(APIView):
    @swagger_auto_schema(
        tags=['Client'],
        operation_summary='Get all clients'
    )
    def get(self, request):
        users = CustomUser.objects.all()
        clients = CustomUserSerializer(users, many=True)

        return Response({
            'success': True,
            'data': clients.data,
            'message': "Clients List" if users.exists() else "No client yet"
        })

class SignInView(APIView):
    @swagger_auto_schema(
        tags=['Authentication'],
        operation_summary="User Registration",
        request_body=CustomUserSerializer,
    )
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'success': True,
                'data': user.format,
                'message': 'You are successfully signed in!'
            }, status=status.HTTP_201_CREATED)

        else:
            return Response({
                'success': False,
                'data': serializer.errors,
                'message': 'Invalid data'
            }, status=status.HTTP_400_BAD_REQUEST)
