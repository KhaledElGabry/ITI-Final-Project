from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from .models import Product, Favorite
from account.models import CustomToken

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def remove_from_Favorite(request, id):
    if request.user.usertype != "customer":
        raise AuthenticationFailed({"message": 'Only customers can access.'})
    
    token = CustomToken.objects.get(user=request.user)
    if token.expires and token.is_expired():
        raise AuthenticationFailed({"data": "expired_token.", "message": 'Please login again.'})
    
    try:
        favorite = Favorite.objects.get(user=request.user, product_id=id)
        favorite.delete()
        return JsonResponse({'message': 'Product was removed from favorites.'})
    except Favorite.DoesNotExist:
        return JsonResponse({'message': 'Product is not in favorites.'}, status=400)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
# def add_to_Favorite(request, id):
#     if request.user.usertype != "customer":
#         raise AuthenticationFailed({"message": 'Only customers can access.'})
    
#     token = CustomToken.objects.get(user=request.user)
#     if token.expires and token.is_expired():
#         raise AuthenticationFailed({"data": "expired_token.", "message": 'Please login again.'})
    
#     try:
#         Favorite.objects.create(user=request.user, product_id=id)
#         return JsonResponse({'message': 'Product was added to favorites.'})
#     except:
#         return JsonResponse({'message': 'Product not found.'}, status=404)

def add_to_Favorite(request, id):
    if request.user.usertype != "customer":
        raise AuthenticationFailed({"message": 'Only customers can access.'})
    
    token = CustomToken.objects.get(user=request.user)
    if token.expires and token.is_expired():
        raise AuthenticationFailed({"data": "expired_token.", "message": 'Please login again.'})
    
    # Check if the product already exists in the user's favorites
    if Favorite.objects.filter(user=request.user, product_id=id).exists():
        return JsonResponse({'message': 'Product is already in favorites.'})
    
    try:
        Favorite.objects.create(user=request.user, product_id=id)
        return JsonResponse({'message': 'Product was added to favorites.'})
    except:
        return JsonResponse({'message': 'Product not found.'}, status=404)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_favorite(request):
    if request.user.usertype != "customer":
        raise AuthenticationFailed({"message": 'Only customers can access.'})
    
    token = CustomToken.objects.get(user=request.user)
    if token.expires and token.is_expired():
        raise AuthenticationFailed({"data": "expired_token.", "message": 'Please login again.'})
    
    user_favorites = Favorite.objects.filter(user=request.user)
    favorite_products_list = [{
                                'id': favorite.product.id,
                                'name': favorite.product.prodName,
                                'price': favorite.product.prodPrice,
                                'prodDescription': favorite.product.prodDescription,
                                'prodStock': favorite.product.prodStock,
                                'prodImageUrl': favorite.product.prodImageUrl,
                                
                                } for favorite in user_favorites]
    return JsonResponse({'favorite_products': favorite_products_list})
