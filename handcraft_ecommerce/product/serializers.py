from rest_framework import serializers
from .models import Product, Category, SubCategory, ProductImage


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

     prodCategory = CategorySerializer()
     prodSubCategory = SubCategorySerializer()
     prodImages = ProductImageSerializer(many=True)