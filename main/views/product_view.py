from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from main.models import Product
from main.serializers import ProductSerializer


class ProductsListView(APIView):
    @swagger_auto_schema(
        tags=['Product'],
        operation_summary='Get all products',
        responses={
            200: openapi.Response(
                description="Products list",
                examples={
                    "application/json": {
                        "success": True,
                        "data": [
                            {
                                "id": 1,
                                "title": "book",
                                "price": 10000.00,
                                "quantity": "20"
                            },
                            {
                                "id": 2,
                                "title": "pencil",
                                "price": 1000.00,
                                "quantity": "10"
                            }
                        ],
                        "message": "Products List"
                    }
                }
            )
        }
    )
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)

        if products.exists():
            return Response({
                "success": True,
                "data": serializer.data,
                "message": "Products List"
            }, status=status.HTTP_200_OK)

        return Response({
            "success": True,
            "data": None,
            "message": "No products yet"
        }, status=status.HTTP_200_OK)


class NewProductView(APIView):
    @swagger_auto_schema(
        tags=['Product'],
        operation_summary='New product',
        request_body=ProductSerializer
    )
    def post(self, request):
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            product = serializer.save()
            return Response({
                "success": True,
                "data": ProductSerializer(product).data,
                "message": "Product created successfully"
            }, status=status.HTTP_201_CREATED)

        return Response({
            "success": False,
            "data": serializer.errors,
            "message": "Invalid data!"
        }, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    @swagger_auto_schema(
        tags=['Product'],
        operation_summary="Get product by ID",
        responses={
            200: ProductSerializer,
            404: openapi.Response("Product not found")
        }
    )
    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product)
            return Response({
                "success": True,
                "data": serializer.data,
                "message": "Product retrieved successfully"
            }, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({
                "success": False,
                "data": None,
                "message": "Product not found"
            }, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        tags=['Product'],
        operation_summary="Update product (partial)",
        request_body=ProductSerializer,
        responses={
            200: ProductSerializer,
            400: "Invalid data",
            404: "Product not found"
        }
    )
    def patch(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({
                "success": False,
                "data": None,
                "message": "Product not found"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            product = serializer.save()
            return Response({
                "success": True,
                "data": ProductSerializer(product).data,
                "message": "Product updated successfully"
            }, status=status.HTTP_200_OK)

        return Response({
            "success": False,
            "data": serializer.errors,
            "message": "Invalid data!"
        }, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        tags=['Product'],
        operation_summary="Delete product",
        responses={
            204: "Product deleted successfully",
            404: "Product not found"
        }
    )
    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            product.delete()
            return Response({
                "success": True,
                "data": None,
                "message": "Product deleted successfully"
            }, status=status.HTTP_200_OK)

        except Product.DoesNotExist:
            return Response({
                "success": False,
                "data": None,
                "message": "Product not found"
            }, status=status.HTTP_404_NOT_FOUND)


