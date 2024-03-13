
from .models import Product, Category, SubCategory , Rating
from .models import Product, Category, SubCategory
from account.models import User
from .serializers import ProductSerializer, CategorySerializer, SubCategorySerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import permissions
from django.shortcuts import get_object_or_404,get_list_or_404
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from account.models import CustomToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.pagination import PageNumberPagination
from .serializers import PaginatedProductSerializer
from account.app import upload_photo,delete_photos
import os
from django.http import HttpRequest , HttpResponse

from functools import reduce
import operator
from django.db.models import Q
from rest_framework import viewsets , mixins
from .serializers import ProductSearchSerializer , Ratingserializer ,FavoriteSerializer
from django.http import JsonResponse
from django.core import serializers
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer , ChatterBotCorpusTrainer
import time
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist


# Products Pagination
class CustomPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000
    
    def get_page_size(self, request):
        # Adjust the page size if specified in the query parameters
        if self.page_size_query_param:
            try:
                page_size = int(request.query_params[self.page_size_query_param])
                if page_size > 0:
                    return page_size
            except (KeyError, ValueError):
                pass



        return self.page_size

    def paginate_queryset(self, queryset, request, view=None):
        # Get the page size and number from query parameters
        self.page_size = self.get_page_size(request)
        self.page_number = request.query_params.get(self.page_query_param, 1)

        # Calculate the offset based on page size and number
        if self.page_number == 'last':
            self.page_number = self.page.paginator.num_pages
        try:
            self.page_number = max(int(self.page_number), 1)
        except (TypeError, ValueError):
            self.page_number = 1

        # Skip records based on offset
        self.offset = (self.page_number - 1) * self.page_size
        
        self.request = request
        if not self.page_size:
            return None

        # Perform pagination
        queryset = super().paginate_queryset(queryset, request, view)
        if not queryset:
            return None

        return list(queryset)
    




# Products List and Details API's and Paginator 

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def productListApi(request):
    token = CustomToken.objects.get(user=request.user)
    if token.expires and token.is_expired():
        raise AuthenticationFailed({"data": "expired_token.", "message": 'Please login again.'})
    
    paginator = CustomPagination()
    products = Product.objects.all()
    
    limit = request.query_params.get('limit')
    skip = request.query_params.get('skip')
    
    if limit is not None:
        try:
            limit = int(limit)
            if limit < 0:
                limit = 0
        except ValueError:
            limit = None
    
    if skip is not None:
        try:
            skip = int(skip)
            if skip < 0:
                skip = 0
        except ValueError:
            skip = None
    
    if limit is not None and skip is not None:
        products = products[skip:skip+limit]
    elif limit is not None:
        products = products[:limit]
    elif skip is not None:
        products = products[skip:]
    
    # Paginate the products
    paginated_products = paginator.paginate_queryset(products, request)
    
    # Serialize paginated products
    serializer = ProductSerializer(paginated_products, many=True)
    
    # Return paginated response
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def productDetailsApi(request, id):
    token = CustomToken.objects.get(user=request.user)
    if token.expires and token.is_expired():
        raise AuthenticationFailed({"data":"expired_token.", "message":'Please login again.'})
    productDetails = Product.objects.get(id=id)
    data = ProductSerializer(productDetails).data
    return Response({'data':data})






# List all Products that belonging to the specified Vendor

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def productVendorApi(request):
    if request.user.usertype != "vendor":
         raise AuthenticationFailed({"message":'only vendor can access.'})
         
    token = CustomToken.objects.get(user=request.user)
    if token.expires and token.is_expired():
            raise AuthenticationFailed({"data":"expired_token.", "message":'Please login again.'})
    vendor = get_object_or_404(User, id=request.user.id, usertype='vendor')
    vendorProducts = Product.objects.filter(prodVendor=vendor)
    serializer = ProductSerializer(vendorProducts, many=True)
    return Response(serializer.data)




# Create Product API

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def productCreateVendorApi(request):
    if request.user.usertype != "vendor":
         raise AuthenticationFailed({"message":'only vendor can access.'})
         
    token = CustomToken.objects.get(user=request.user)
    if token.expires and token.is_expired():
            raise AuthenticationFailed({"data":"expired_token.", "message":'Please login again.'})
    


    serializer = ProductSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    product = serializer.save()
    product.prodVendor=request.user
    
    if serializer.is_valid():
        prod = ProductSerializer(product)
        # if user send new image
        if 'prodImageThumbnail' in request.data and request.data['prodImageThumbnail'] is not None:
                # if user has already image on drive
                if serializer.validated_data.get('prodImageThumbnail') is not None:
                    delete_photos(f"{product.id}.png", "1bzm8Xuenx4NVyxmJUTV6n5mpmbFrVqg1")
                           
                # upload new image
                media_folder = os.path.join(os.getcwd(), "media/product")
                # save new url
                Url_Image = upload_photo(os.path.join(media_folder, os.path.basename(serializer['prodImageThumbnail'].value)),f"{product.id}.png", "1bzm8Xuenx4NVyxmJUTV6n5mpmbFrVqg1")
                product.prodImageUrl = Url_Image
                product.save()
                
                # remove image from server
                if os.path.exists(media_folder):
                    for file_name in os.listdir(media_folder):
                        file_path = os.path.join(media_folder, file_name)
                        try:
                            if os.path.isfile(file_path):
                                os.remove(file_path)
                                print(f"Deleted: {file_path}")
                            else:
                                print(f"Skipped: {file_path} (not a file)")
                        except Exception as e:
                            print(f"Error deleting {file_path}: {e}")
                else:
                    print("Folder does not exist.")


        return Response({"product" : prod.data}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





# Update and Delete Product API

@api_view(['PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def productUpdateDeleteApi(request, id):
    if request.user.usertype != "vendor":
         raise AuthenticationFailed({"message":'only vendor can access.'})
         
    token = CustomToken.objects.get(user=request.user)
    if token.expires and token.is_expired():
            raise AuthenticationFailed({"data":"expired_token.", "message":'Please login again.'})
    



    product = get_object_or_404(Product, id=id)

    if request.user != product.prodVendor:
        return Response({'error': 'You do not have permission to access this product'}, status=status.HTTP_403_FORBIDDEN)

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






# Category List and Details API's


@api_view(['GET'])
def categoryListApi(request):
    #  categories = Category.objects.all()
     categories = get_list_or_404(Category)
     data = CategorySerializer(categories, many=True).data
     return Response({'data':data})



@api_view(['GET'])
def categoryDetailsApi(request, id):
     categoryDetails = get_object_or_404(Category, id=id)
     
    #  categoryDetails = Category.objects.get(id=id)
     data = CategorySerializer(categoryDetails).data
     return Response({'data':data})




# SubCategory List and Details API's


@api_view(['GET'])
def subCategoryListApi(request):
     subCategories = get_list_or_404(SubCategory)
     data = SubCategorySerializer(subCategories, many=True).data
     return Response({'data':data})



@api_view(['GET'])
def subCategoryDetailsApi(request, id):
     
     subCategoriesDetails = get_object_or_404(SubCategory, id=id)
     data = SubCategorySerializer(subCategoriesDetails).data

     return Response({'data':data})











#================================ API for search =================================================================
class AllProductSearch(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset=Product.objects.all()
    serializer_class = ProductSearchSerializer

    def get_queryset(self):
        text=self.request.query_params.get('query',None)
        if not text:
            return self.queryset
        
        text_seq=text.split(' ')
        text_qs=reduce(operator.and_,
                       (Q(prodName__icontains=x)for x in text_seq))
        

        return self.queryset.filter(text_qs)
#================================ API for rating =================================================================

#--------------------------------- averege rating ---------------------------
def product_rat(request,id):
    rate=Rating.objects.filter(rateProduct__id=id)
    product=Product.objects.get(id=id)
    sum=0
    for i in rate:
        sum += i.rateRating
    result=sum/len(rate)
    return JsonResponse({'id':product.id,'product':product.prodName,'averege Rate':result})

#-------------------------------------------Rate product------------------------------------------------------

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
@csrf_exempt
def submit_review(request, product_id):
    if request.user.usertype == "vendor":
        raise AuthenticationFailed({"message": 'only customer can access.'})
    
    token = CustomToken.objects.get(user=request.user)
    if token.expires and token.is_expired():
        raise AuthenticationFailed({"data": "expired_token.", "message": 'Please login again.'})
    
    if request.method == 'POST':
        try:
            rating = Rating.objects.get(rateCustomer=request.user, rateProduct__id=product_id)
            rating.rateRating = request.data.get('rateRating')
            rating.rateSubject = request.data.get('rateSubject')
            rating.rateReview = request.data.get('rateReview')
            rating.save()
        except Rating.DoesNotExist:
            try:
                product = Product.objects.get(id=product_id)
                rating = Rating.objects.create(rateCustomer=request.user, rateProduct=product,
                                               rateRating=request.data.get('rateRating'),
                                               rateSubject=request.data.get('rateSubject'),
                                               rateReview=request.data.get('rateReview'))
            except ObjectDoesNotExist:
                return Response({'message': 'Product not found'}, status=404)
            
        return JsonResponse({'reviews': rating.id})

#================================ API for favorite =================================================================

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def remove_from_Favorite(request,id):

    if request.user.usertype == "vendor":
         raise AuthenticationFailed({"message":'only customer can access.'})
         
    token = CustomToken.objects.get(user=request.user)
    if token.expires and token.is_expired():
            raise AuthenticationFailed({"data":"expired_token.", "message":'Please login again.'})
    
    product=Product.objects.get(id=id)
    if product.prodFavorite.filter(id=request.user.id).count() > 0:
        product.prodFavorite.remove(request.user)
        product.save()      
        return JsonResponse({'message': 'Product was removed from favorites.'}) 
    return JsonResponse({})



@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_to_Favorite(request, id):

    if request.user.usertype == "vendor":
         raise AuthenticationFailed({"message": 'Only customers can access.'})
         
    token = CustomToken.objects.get(user=request.user)
    if token.expires and token.is_expired():
        raise AuthenticationFailed({"data": "expired_token.", "message": 'Please login again.'})
    
    try:
        product = Product.objects.get(id=id)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Product does not exist'}, status=404)

    if product.prodFavorite.filter(id=request.user.id).exists():
        return JsonResponse({'message': 'Product is already in favorites.'})

    product.prodFavorite.add(request.user)
    product.save()
    return JsonResponse({'message': 'Product was added to favorites.'})



@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def user_favorite(request):

    if request.user.usertype == "vendor":
         raise AuthenticationFailed({"message":'only customer can access.'})
         
    token = CustomToken.objects.get(user=request.user)
    if token.expires and token.is_expired():
            raise AuthenticationFailed({"data":"expired_token.", "message":'Please login again.'})
    
    user_favorites=Product.objects.filter(prodFavorite=request.user)
    # favSer=FavoriteSerializer
    favorite_products_list = [{
                                'id': product.id,
                                'name': product.prodName,
                                'price': product.prodPrice , 
                                # 'prodVendor': product.prodVendor , 
                                'prodDescription':product.prodDescription,
                                # 'prodDescription':product.prodSubCategory,
                                'prodOnSale':product.prodOnSale,
                                'prod in Stock':product.prodStock,
                                # 'prodDescription':product.prodImageThumbnail,
                                'prod Image':product.prodImageUrl,
                                
                                } for product in user_favorites]
    return JsonResponse({'favorite_products': favorite_products_list})

#==========================================================Chat Bot====================================================
bot = ChatBot(
    'chatbot',
    read_only=False,
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'Sorry, I don\'t understand.',
            'maximum_similarity_threshold': 0.90
        }
    ]
)
list_to_train = [
   
   
    "Hello",
    "Hello,friend",
     
    "could you explain to me this website",
    "this website for handmade , the seller will display the product on website, and you have the option to choose one of the products you like",
    
    "how can i buy",
    "first you need to register as a customer then search for the product after that choose it , pay the amount and it will reach to you on time",
    
    "how to know the quality of this product",
    "there is an averege review for each product and also after you get the product you can submit a review",
    
    "i need to display my product", 
    "register on website as a vendor , fillout you data , you will be able to find add products , click on it and you will be able to add any products that you need", 
     
    
]
list_trainer = ListTrainer(bot)
list_trainer.train(list_to_train)

@csrf_exempt
def get_response(request):
    user_message = request.POST.get('userMessage')
    if user_message:
        chat_response = str(bot.get_response(user_message))
    else:
        chat_response = "Please provide a 'userMessage' parameter."
    return JsonResponse({'response': chat_response})