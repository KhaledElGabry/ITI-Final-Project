from rest_framework import serializers
from .models import Product, Category, SubCategory, ProductImage
from account.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
     class Meta:
        model = Category
        fields = ['id']



class SubCategorySerializer(serializers.ModelSerializer):
     class Meta:
        model = SubCategory
        fields = ['id']



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