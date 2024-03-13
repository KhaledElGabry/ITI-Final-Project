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
            'prodDescription',
            'prodSubCategory',
            'prodOnSale',
            'prodImageThumbnail',
        ]

class Ratingserializer(serializers.ModelSerializer):
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



class SubCategorySerializer(serializers.ModelSerializer):
     class Meta:
        model = SubCategory
        fields = '__all__'



class ProductImageSerializer(serializers.ModelSerializer):
     class Meta:
        model = ProductImage
        fields = '__all__'


      #   def create(self, validated_data):
     
      #    productImages=ProductImage()
      #    productImages.prodImageProduct=validated_data['prodImageProduct']
      #    productImages.prodImage=validated_data['prodImage']
        


      #    product = Product.objects.create(**validated_data)
      #    product.save()
      #    print(product.prodSubCategory.id)
      #    return product    


      




class ProductSerializer(serializers.ModelSerializer):
      class Meta:
         model = Product
         fields = '__all__'

         
         # prodVendor = UserSerializer()
         # prodCategory = CategorySerializer()
         # prodSubCategory = SubCategorySerializer()
         # prodImages = ProductImageSerializer(many=True)

      def create(self, validated_data):
     
         product=Product()
         # product.prodVendor=self.request.user
         product.prodName=validated_data['prodName']
         product.prodPrice=validated_data['prodPrice']
         product.prodDescription=validated_data['prodDescription']
         product.prodSubCategory=validated_data['prodSubCategory']
         product.prodStock=validated_data['prodStock']
         product.prodOnSale=validated_data['prodOnSale']
         # product.prodImages=validated_data['prodImages']
        #  product.prodFavorite=validated_data['prodFavorite']

         product = Product.objects.create(**validated_data)
         product.save()
         print(product.prodSubCategory.id)
         return product    
      

      def update(self, instance, validated_data):
        instance.prodName = validated_data.get('prodName', instance.prodName)
        instance.prodPrice = validated_data.get('prodPrice', instance.prodPrice)
        instance.prodDescription = validated_data.get('prodDescription', instance.prodDescription)
        instance.prodSubCategory = validated_data.get('prodSubCategory', instance.prodSubCategory)
        instance.prodOnSale = validated_data.get('prodOnSale', instance.prodOnSale)
        instance.prodStock = validated_data.get('prodStock', instance.prodStock)
        instance.prodImageThumbnail = validated_data.get('prodImageThumbnail', instance.prodImageThumbnail)



        instance.save()
        return instance
      
      def delete(self, instance):
        instance.delete()




class PaginatedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'



      
     
