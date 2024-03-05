# from django.shortcuts import render

from .models import Product, Category, SubCategory
from .serializers import ProductSerializer, CategorySerializer, SubCategorySerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404



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


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def addProductApi(request):
     if request.user.usertype != 'vendor':
        return Response({'error': 'Only vendors are allowed to add products'}, status=403)
     
     productData = request.data
     newProduct = Product.objects.create(vendor=request.user, **productData)
     newProduct.save()
     return Response({'message': 'Product added successfully'})

@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])
def updateProductApi(request, id):
     if request.user.usertype != 'vendor':
      return Response({'error': 'Only vendors are allowed to update products'}, status=403)
     
     theProductInstance = get_object_or_404(Product, id=id)

     productData = request.data
     serializer = ProductSerializer(theProductInstance, data=productData, partial=True)
     if serializer.is_valid():
         serializer.save()
         return Response({'message': 'Product updated successfully'})
     else:
         return Response(serializer.errors, status=400)
     return Response({'message': 'Product updated successfully'})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def removeProductApi(request, id):
     if request.user.usertype != 'vendor':
        return Response({'error': 'Only vendors are allowed to remove products'}, status=403)
    

     theProductInstance = get_object_or_404(Product, id=id)
     theProductInstance.delete()
     return Response({'message': 'Product removed successfully'})





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




