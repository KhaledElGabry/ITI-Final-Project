from rest_framework import serializers
from .models import Product, Category, SubCategory, ProductImage , Product , Rating , Product
from account.serializers import UserSerializer
from decimal import Decimal



class ProductSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=[
            'prodVendor',
            'prodName',
            'prodPrice',
            'prodDescription',
            'prodSubCategory',
            'prodOnSale',
            'prodImageThumbnail',
        ]

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Rating
        fields='__all__'

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=[
            'prodVendor',
            'prodName',
            'prodPrice',
            'prodSubCategory',
            'prodOnSale',
            'prodImageThumbnail',
            'prodFavorite',
        ]                        

class CategorySerializer(serializers.ModelSerializer):
      class Meta:
        model = Category
        fields = '__all__'

      def create(self,validated_data):
        category=Category()
        category.cateName=validated_data['name']
      #   category.cateParent=validated_data['price']
        category.cateDescription=validated_data['price']
      #   category.cateImage=validated_data['price']
        return category



class SubCategorySerializer(serializers.ModelSerializer):
     class Meta:
        model = SubCategory
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
     class Meta:
        model = ProductImage
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):

    discounted_price = serializers.SerializerMethodField()
    original_price = serializers.ReadOnlyField(source='prodPrice') 
    class Meta:
      model = Product
      fields = '__all__'

      # prodVendor = UserSerializer()
      # prodCategory = CategorySerializer()
      # prodSubCategory = SubCategorySerializer()


    def create(self, validated_data):
     
        product=Product()
        # product.prodVendor=self.request.user
        product.prodName=validated_data['prodName']
        product.prodPrice=validated_data['prodPrice']
        product.prodDescription=validated_data['prodDescription']
        product.prodSubCategory=validated_data['prodSubCategory']
        product.prodStock=validated_data['prodStock']
        product.prodOnSale=validated_data['prodOnSale']
        product.prodDiscountPercentage=validated_data['prodDiscountPercentage']
        product.prodImageThumbnail = validated_data['prodImageThumbnail']
        product.prodImageOne = validated_data['prodImageOne']
        product.prodImageTwo = validated_data['prodImageTwo']
        product.prodImageThree = validated_data['prodImageThree']
        product.prodImageFour = validated_data['prodImageFour']

        product = Product.objects.create(**validated_data)


        product.save()
        return product    
    
    def update(self, instance, validated_data):

      instance.prodName = validated_data.get('prodName', instance.prodName)
      instance.prodPrice = validated_data.get('prodPrice', instance.prodPrice)
      instance.prodDescription = validated_data.get('prodDescription', instance.prodDescription)
      instance.prodSubCategory = validated_data.get('prodSubCategory', instance.prodSubCategory)
      instance.prodOnSale = validated_data.get('prodOnSale', instance.prodOnSale)
      instance.prodDiscountPercentage = validated_data.get('prodDiscountPercentage', instance.prodDiscountPercentage)
      instance.prodStock = validated_data.get('prodStock', instance.prodStock)
      instance.prodImageThumbnail = validated_data.get('prodImageThumbnail', instance.prodImageThumbnail)
      instance.prodImageOne = validated_data.get('prodImageOne', instance.prodImageOne)
      instance.prodImageTwo = validated_data.get('prodImageTwo', instance.prodImageTwo)
      instance.prodImageThree = validated_data.get('prodImageThree', instance.prodImageThree)
      instance.prodImageFour = validated_data.get('prodImageFour', instance.prodImageFour)
      # instance.prodFavorite = validated_data.get('prodFavorite', instance.prodFavorite)
      
      
      instance.save()
      return instance
      
    def delete(self, instance):
      instance.delete() 
  

    def get_discounted_price(self, instance):
      if instance.prodOnSale:
        try:
            prodPrice_decimal = Decimal(str(instance.prodPrice))
            discount_decimal = Decimal(instance.prodDiscountPercentage) / 100
        except (ValueError, TypeError):
            return instance.prodPrice  
        discounted_price = prodPrice_decimal - (prodPrice_decimal * discount_decimal)
        return discounted_price
      return instance.prodPrice 





class PaginatedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'



      
     