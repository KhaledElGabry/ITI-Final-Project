from rest_framework import serializers
from .models import Product, Category, SubCategory, ProductImage
from account.serializers import UserSerializer


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
         # product.prodCategory=validated_data['prodCategory']
         # prod_sub_category_id = validated_data['prodSubCategory']
         # print(prod_sub_category_id)
         product.prodSubCategory=validated_data['prodSubCategory']
         product.prodOnSale=validated_data['prodOnSale']
         product.prodImageThumbnail=validated_data['prodImageThumbnail']
         # product.prodImages=validated_data['prodImages']


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
        instance.prodImageThumbnail = validated_data.get('prodImageThumbnail', instance.prodImageThumbnail)



        instance.save()
        return instance
      
      def delete(self, instance):
        instance.delete()




   




      # prod_sub_category_data = validated_data.pop('prodSubCategory_data', None)
      # if prod_sub_category_data:
      #       prod_sub_category, _ = SubCategory.objects.get_or_create(**prod_sub_category_data)
      # elif prod_sub_category_id:
      #       prod_sub_category = SubCategory.objects.get(id=prod_sub_category_id)
      # else:
      #       prod_sub_category = None

      #   # Create the Product instance
      # product = Product.objects.create(**validated_data)

      #   # Set the prodSubCategory if available
      # if prod_sub_category:
      #       product.prodSubCategory = prod_sub_category
      #       product.save()

      # return product




      
     



















      # product.prodRating=validated_data.get('rating', 0.0)
      # prodSlug
