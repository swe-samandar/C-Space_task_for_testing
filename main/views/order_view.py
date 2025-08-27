from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from main.models import Order
from main.serializers import OrderSerializer


class OrdersListView(APIView):
    @swagger_auto_schema(
        tags=['Order'],
        operation_summary="Get all orders",
        responses={200: OrderSerializer(many=True)}
    )
    def get(self, request):
        orders = Order.objects.all()
        serializers = OrderSerializer(orders, many=True)

        return Response({
            'success': True,
            'data': serializers.data,
            'message': 'Orders List' if orders.exists() else 'No orders yet'
        }, status=status.HTTP_200_OK)


class NewOrderView(APIView):
    @swagger_auto_schema(
        tags=['Order'],
        operation_summary='New Order',
        request_body=OrderSerializer,
    )
    def post(self, request):
        serializer = OrderSerializer(data=request.data)

        if serializer.is_valid():
            order = serializer.save()
            return Response({
                "success": True,
                "data": OrderSerializer(order).data,
                "message": "Order created successfully"
            }, status=status.HTTP_201_CREATED)

        return Response({
            "success": False,
            "data": serializer.errors,
            "message": "Invalid data"
        }, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailView(APIView):
    @swagger_auto_schema(
        tags=['Order'],
        operation_summary="Get order by ID",
        responses={200: OrderSerializer()}
    )
    def get(self, request, pk):
        try:
            order = Order.objects.get(id=pk)
        except Order.DoesNotExist:
            return Response({
                "success": False,
                "data": None,
                "message": "Order not found"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(order)
        return Response({
            "success": True,
            "data": serializer.data,
            "message": "Order detail"
        }, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=['Order'],
        operation_summary="Update order by ID",
        request_body=OrderSerializer,
        responses={200: OrderSerializer()}
    )
    def patch(self, request, pk):
        try:
            order = Order.objects.get(id=pk)
        except Order.DoesNotExist:
            return Response({
                "success": False,
                "data": None,
                "message": "Order not found"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "data": serializer.data,
                "message": "Order successfully updated!"
            }, status=status.HTTP_200_OK)

        return Response({
            "success": False,
            "data": serializer.errors,
            "message": "Invalid data!"
        }, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        tags=['Order'],
        operation_summary="Delete order by ID",
        responses={204: "Order successfully deleted"}
    )
    def delete(self, request, pk):
        try:
            order = Order.objects.get(id=pk)
        except Order.DoesNotExist:
            return Response({
                "success": False,
                "data": None,
                "message": "Order not found"
            }, status=status.HTTP_404_NOT_FOUND)

        order.delete()
        return Response({
            "success": True,
            "data": None,
            "message": "Order successfully deleted!"
        }, status=status.HTTP_200_OK)

