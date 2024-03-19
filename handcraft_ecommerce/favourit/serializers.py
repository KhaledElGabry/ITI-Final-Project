from rest_framework import serializers
from .models import Product, Rating, Category, SubCategory, ProductImage
from account.models import User
from .models import Favorite

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']  # Add more fields if needed


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'prodVendor', 'prodName', 'prodPrice', 'prodDescription', 'prodSubCategory', 'prodStock', 'prodImageThumbnail']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'rateProduct', 'rateCustomer', 'rateRating', 'rateSubject', 'rateReview', 'rateCreatedDate']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'prodImgsForProduct', 'prodImages']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'cateName', 'cateDescription', 'cateImage']


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'subCateName', 'subCateParent', 'subCateDescription', 'subCateImage']


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'product']
