from rest_framework import serializers
from .models import Product, Category, SubCategory, ProductImage , Product , Rating , Product
from account.serializers import UserSerializer


class ProductSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=[
            'prodVendor',
            'prodName',
            'prodPrice',
            'prodQuantity',
            'prodDescription',
            'prodCategory',
            'prodSubCategory',
            'prodOnSale',
            'prodRating',
            'prodImages',
        ]

class Ratingserializer(serializers.ModelSerializer):
    class Meta:
        model=Rating
        fields=[
            'product',
            'user',
            'rating',
            'subject',
            'review',
            'createdDate',
        ]

class Productserializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=[
            'prodVendor',
            'prodName',
            'prodPrice',
            'prodCategory',
            'prodSubCategory',
            'prodImages',
            'favorite',
        ]                        

class CategorySerializer(serializers.ModelSerializer):
     class Meta:
        model = Category
        fields = '__all__'



class SubCategorySerializer(serializers.ModelSerializer):
     class Meta:
        model = SubCategory
        fields = '__all__'



class ProductImageSerializer(serializers.ModelSerializer):
     class Meta:
        model = ProductImage
        fields = '__all__'




class ProductSerializer(serializers.ModelSerializer):
     class Meta:
          model = Product
          fields = '__all__'

     prodVendor = UserSerializer()
     prodCategory = CategorySerializer()
     prodSubCategory = SubCategorySerializer()
     prodImages = ProductImageSerializer(many=True)