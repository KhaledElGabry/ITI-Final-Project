
from .models import Product, Category, SubCategory
from account.models import User
from .serializers import ProductSerializer, CategorySerializer, SubCategorySerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from rest_framework import status



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

# Vendor API's

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def productVendorApi(request, id):
    # GET: List all products belonging to the specified vendor
    vendor = get_object_or_404(User, id=id, usertype='vendor')
    vendorProducts = Product.objects.filter(prodVendor=vendor)
    serializer = ProductSerializer(vendorProducts, many=True)
    return Response(serializer.data)



@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def productCreateVendorApi(request):
    # POST: Create a new product for the authenticated vendor
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(prodVendor=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def productUpdateDeleteApi(request, id):
    try:
        isProdExist = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    # Check if the authenticated user is the owner of the product
    if request.user != isProdExist.prodVendor:
        return Response({'error': 'You do not have permission to update/delete this product'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PUT':
        # PUT: Update the existing product belonging to the authenticated vendor
        serializer = ProductSerializer(isProdExist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # DELETE: Delete the existing product belonging to the authenticated vendor
        isProdExist.delete()
        return Response({'message': 'Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)





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
