# from django.shortcuts import render

from .models import Product, Category, SubCategory
from .serializers import ProductSerializer, CategorySerializer, SubCategorySerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics



# All Products List and Details 

@api_view(['GET'])
def productListApi(request):
     products = Product.objects.all()
     data = ProductSerializer(products, many=True).data
     return Response({'data':data})


@api_view(['GET'])
def productDetailsApi(request, id):
     productDetails = Product.objects.get(id=id)
     data = ProductSerializer(productDetails).data
     return Response({'data':data})






# All Category List and Details 


@api_view(['GET'])
def categoryListApi(request):
     categories = Category.objects.all()
     data = CategorySerializer(categories, many=True).data
     return Response({'data':data})



@api_view(['GET'])
def categoryDetailsApi(request, id):
     categoryDetails = Category.objects.get(id=id)
     data = CategorySerializer(categoryDetails).data
     return Response({'data':data})




# All SubCategory List and Details 


@api_view(['GET'])
def subCategoryListApi(request):
     subCategories = SubCategory.objects.all()
     data = SubCategorySerializer(subCategories, many=True).data
     return Response({'data':data})



@api_view(['GET'])
def subCategoryDetailsApi(request, id):
     subCategoriesDetails = SubCategory.objects.get(id=id)
     data = SubCategorySerializer(subCategoriesDetails).data
     return Response({'data':data})




