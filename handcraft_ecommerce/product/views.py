from .models import Product, Category, SubCategory
from account.models import User
from .serializers import ProductSerializer, CategorySerializer, SubCategorySerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
import jwt


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














# Vendor API's FunctionBased

# List all Products belonging to the specified Vendor
@api_view(['GET'])
# @permission_classes([permissions.IsAuthenticated])
def productVendorApi(request, id):
    vendor = get_object_or_404(User, id=id, usertype='vendor')
    vendorProducts = Product.objects.filter(prodVendor=vendor)
    serializer = ProductSerializer(vendorProducts, many=True)
    return Response(serializer.data)



# @api_view(['POST'])
# # @permission_classes([permissions.IsAuthenticated])
# def productCreateVendorApi(request):
#     # POST: Create a new product for the authenticated vendor
#     serializer = ProductSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save(prodVendor=request.user)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([AllowAny])
def productCreateVendorApi(request):

    # token = request.headers.get('userToken')  
    # if not token:
    #     return Response({'error': 'Token not provided'}, status=status.HTTP_400_BAD_REQUEST)

    # try:
    #     payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    #     userID = payload.get('id')
    #     user = User.objects.get(id=userID)
    #     print("user",user)
    #     print("userID",userID)

    # except jwt.ExpiredSignatureError:
    #     return Response({'error': 'Token has expired'}, status=status.HTTP_401_UNAUTHORIZED)
    # except jwt.InvalidTokenError:
    #     return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
    # except User.DoesNotExist:
    #     return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    # if user.usertype == 'vendor' and user.is_active:
    
    # products = Product.objects.create()
    # data = request.data


    serializer = ProductSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    product = serializer.save()
    serializer = ProductSerializer(product)
    return Response({"product" : serializer.data}, status=status.HTTP_201_CREATED)
    # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






@api_view(['PUT', 'DELETE'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def productUpdateDeleteApi(request, id):
    product = get_object_or_404(Product, id=id)

    # if request.user != product.prodVendor:
    #     return Response({'error': 'You do not have permission to update/delete this product'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PUT':
        # PUT: Update the existing product belonging to the authenticated vendor
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"product": serializer.data}, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        # DELETE: Delete the existing product belonging to the authenticated vendor
        product.delete()
        return Response({'message': 'Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)





# Vendor API's ClassBased


class ProductCreate(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer  # Corrected attribute name
    # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):  # Corrected method name
        # Set the product's vendor to the authenticated user
        serializer.save(prodVendor=self.request.user)



class ProductUpdate(UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        # Ensure the user updating the product is the product's vendor
        if serializer.instance.prodVendor != self.request.user:
            raise PermissionDenied("You do not have permission to update this product.")
        serializer.save()

class ProductDelete(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        # Ensure the user deleting the product is the product's vendor
        if instance.prodVendor != self.request.user:
            raise PermissionDenied("You do not have permission to delete this product.")
        instance.delete()
































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