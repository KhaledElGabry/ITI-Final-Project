# from django.shortcuts import render
from .models import Product, Category, SubCategory
from .serializers import ProductSerializer, CategorySerializer, SubCategorySerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics




@api_view(['GET'])
def productListApi(request):
     Products = Product.objects.all()
     data = ProductSerializer(Products, many=True).data
     return Response({'data':data})

@api_view(['GET'])
def productDetailsApi(request, id):
     productDetails = Product.objects.get(id=id)
     data = ProductSerializer(productDetails).data
     return Response({'data':data})



