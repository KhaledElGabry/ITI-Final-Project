from django.shortcuts import render , redirect , reverse
from django.http import HttpRequest , HttpResponse
from django.http import JsonResponse
from account.models import *
from product.models import *
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate , login , logout
from django. contrib import messages
import os
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from product.models import Product
from order.models import OrderItem , Order
from django.db.models import Sum, Count 
from django.db.models import Q 



from rest_framework import status
from rest_framework.views import APIView
from order.models import Order, OrderItem
from order.serializers import OrderSerializer
from rest_framework.decorators import api_view, permission_classes


# Login

from rest_framework import status
from rest_framework.views import APIView
from order.models import Order, OrderItem
from order.serializers import OrderSerializer
from rest_framework.decorators import api_view, permission_classes

@csrf_exempt
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in")
            return JsonResponse({'success': True})  # Returning JSON response for successful login
        else:
            messages.error(request, "The username or password is incorrect")
            return JsonResponse({'success': False, 'error': 'Invalid credentials'})  # Returning JSON response for failed login
    return render(request, "adminlogin.html")


# Logout

@csrf_exempt
def admin_logout(request):
    logout(request)
    messages.success(request, "You have been logged out")  # Adds a success message
    return JsonResponse({'success': True})  # Returns a JSON response indicating success



# to read image

def get_user_image(request, id):
    try:
        user = User.objects.get(id=id)
        image_data = user.image.read()

        response = HttpResponse(content_type=user.image.content_type)
        response.content = image_data
        return response
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': f'Error retrieving image: {e}'}, status=500)



@csrf_exempt 
def specific_user(request, id):
    try:
        user = User.objects.get(id=id)

        user_data = {
            'ID': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'password': user.password,
            'phone': user.phone,
            'usertype': user.usertype,
            'password': user.password,
            'ssn': user.ssn,
            'shopname': user.shopname,
            'address': user.address,
            'ImageUrl': user.image.url if user.image else None,
        }

        return JsonResponse({'user': user_data})
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)



def userDetails(request):
    users = User.objects.all()
    users_list = []
    for user in users:
        users_list.append({
            'ID': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'password': user.password,
            'phone': user.phone,
            'usertype': user.usertype,
            'ssn': user.ssn,
            'shopname': user.shopname,
            'address': user.address,
            'ImageUrl': user.image.url if user.image else None,
        })
    return JsonResponse({'users': users_list})




# user register 

@csrf_exempt 
def useradd(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already exists'})

        ssn = request.POST.get('ssn', '')
        shopname = request.POST.get('shopname', '')

        # Validate SSN 
        if request.POST.get('usertype', '') == 'vendor':
            if not ssn:
                return JsonResponse({'error': 'SSN is required for vendors'})

            # Check for existing SSN
            if User.objects.filter(ssn=ssn).exists():
                return JsonResponse({'error': 'SSN already exists'})

            if not shopname:
                return JsonResponse({'error': 'Shop name is required'})

        # Create the user object (consider using a serializer for validation)
        user = User.objects.create(
            first_name=request.POST.get('first_name', ''),
            last_name=request.POST.get('last_name', ''),
            email=email,
            phone=request.POST.get('phone', ''),
            usertype=request.POST.get('usertype', ''),
            password=request.POST.get('password', ''),
            address=request.POST.get('address', ''),
            shopname=shopname,
            image=request.FILES.get('image', ''),
        )

        # Set SSN for vendor users only (optional for non-vendor users)
        if ssn:
            user.ssn = ssn
            user.save()

        return JsonResponse({'message': 'User added successfully'})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'})



@csrf_exempt
def deleteUser(request,id):
    delUser=User.objects.get(id=id)
    delUser.delete()
    return JsonResponse({'message': 'User deleted successfully'})



@csrf_exempt
def updateUser(request, id):
    if request.method == 'POST':
        try:
            updateUser = User.objects.get(id=id)  # Use get() instead of filter()
        except User.DoesNotExist:
            return JsonResponse({'message': 'User not found'}, status=404)
        
        if 'image' in request.FILES:
            # Delete old image if it exists
            if updateUser.image:
                media_file = os.path.join(os.getcwd(), updateUser.image.path)
                if os.path.isfile(media_file):
                    os.remove(media_file)
                    print(f"Deleted: {media_file}")

            # Update user with new data including image
            updateUser.image = request.FILES['image']
        
        # Update other fields
        updateUser.first_name = request.POST.get('first_name', '')
        updateUser.last_name = request.POST.get('last_name', '')
        updateUser.email = request.POST.get('email', '')
        updateUser.phone = request.POST.get('phone', '')
        updateUser.usertype = request.POST.get('usertype', '')
        updateUser.password = request.POST.get('password', '')
        updateUser.address = request.POST.get('address', '')
        updateUser.shopname = request.POST.get('shopname', '')
        updateUser.ssn = request.POST.get('ssn', '')
        updateUser.save()

        return JsonResponse({'message': 'User updated successfully'})
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)
    

@csrf_exempt
def specific_product(request, id):
    try:
        product = Product.objects.get(id=id)
        product_dict = {
            'id': product.id,
            'prodName': product.prodName,
            'prodPrice': product.prodPrice,
            'prodDescription': product.prodDescription,
            'prodStock': product.prodStock,
            'prodOnSale': product.prodOnSale,
            'prodDiscountPercentage': product.prodDiscountPercentage,
            'prodImageUrl': product.prodImageUrl,
            'created_at': product.created_at,
        }
        # Accessing fields from related User object
        if product.prodVendor:
            product_dict['prodVendor'] = {
                'username': product.prodVendor.username,
                'email': product.prodVendor.email,
                # Add more fields as needed
            }
        if product.prodSubCategory:
            product_dict['prodSubCategory'] = {
                'subCateName': product.prodSubCategory.subCateName,  # Assuming SubCategory has a 'name' attribute
                # Add more fields as needed
            }
        return JsonResponse({'Product': product_dict})
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

@csrf_exempt
def productDetails(request):

    products = Product.objects.all()
    product_list = []
    for prod in products:
        product_dict = {
            'id': prod.id,
            'prodName': prod.prodName,
            'prodPrice': prod.prodPrice,
            'prodDescription': prod.prodDescription,
            'prodStock': prod.prodStock,
            'prodOnSale': prod.prodOnSale,
            'prodDiscountPercentage': prod.prodDiscountPercentage,
            'prodImageUrl': prod.prodImageUrl,
            'created_at': prod.created_at,
        }
        # Accessing fields from related User object
        if prod.prodVendor:
            product_dict['prodVendor'] = {
                'username': prod.prodVendor.username,
                'email': prod.prodVendor.email,
                # Add more fields as needed
            }
        if prod.prodSubCategory:
            product_dict['prodSubCategory'] = {
                'subCateName': prod.prodSubCategory.subCateName,  # Assuming SubCategory has a 'name' attribute
                # Add more fields as needed
            }
        product_list.append(product_dict)

    return JsonResponse({'Products': product_list})


@csrf_exempt
def productadd(request):
    if request.method == 'POST':
        try:
            # Fetch the user instance based on the provided username or ID
            prod_vendor_id = request.POST.get('prodVendor') 
            prod_vendor = User.objects.get(id=prod_vendor_id)
            
            prod_categ_id = request.POST.get('prodSubCategory')
            prod_categ = SubCategory.objects.get(id=prod_categ_id)
            
            addprod = Product.objects.create(
                prodVendor=prod_vendor,  # Assign the user instance
                prodName=request.POST.get('prodName'),
                prodPrice=request.POST.get('prodPrice'),
                prodDescription=request.POST.get('prodDescription'),
                prodSubCategory=prod_categ,
                prodStock=request.POST.get('prodStock'),
                prodOnSale=request.POST.get('prodOnSale'),
                prodDiscountPercentage=request.POST.get('prodDiscountPercentage'),
                prodImageThumbnail=request.FILES.get('prodImageThumbnail'),
                prodImageOne=request.FILES.get('prodImageOne'),
                prodImageTwo=request.FILES.get('prodImageTwo'),
                prodImageThree=request.FILES.get('prodImageThree'),
                prodImageFour=request.FILES.get('prodImageFour'),
                prodImageUrl=request.FILES.get('prodImageUrl'),
                
                created_at=timezone.now()  # or parse the provided date string
            )
            addprod.save()
            return JsonResponse({'message': 'product added successfully'})
        except ValidationError as e:
            return JsonResponse({'error': f'Validation Error: {e}'})
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {e}'})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'})


@csrf_exempt
def delproduct(request,id):
    delProduct=Product.objects.get(id=id)
    delProduct.delete()
    return JsonResponse({'message': 'Product deleted successfully'})



@csrf_exempt
def updateproduct(request, id):
    if request.method == 'POST':
        product = Product.objects.filter(id=id)
        
        if product.exists():
            if 'image' in request.FILES:
                if product.image and os.path.exists(product.image.path):
                    os.remove(product.image.path)
                product.image = request.FILES['image']


            product.update(
                prodVendor=request.POST.get('prodVendor'),
                prodName=request.POST.get('prodName'),
                prodPrice=request.POST.get('prodPrice'),
                prodDescription=request.POST.get('prodDescription'),
                prodSubCategory=request.POST.get('prodSubCategory'),
                prodStock=request.POST.get('prodStock'),
                prodOnSale=request.POST.get('prodOnSale'),
                prodDiscountPercentage=request.POST.get('prodDiscountPercentage'),
                prodImageThumbnail=request.FILES.get('prodImageThumbnail'),
                prodImageOne=request.FILES.get('prodImageOne'),
                prodImageTwo=request.FILES.get('prodImageTwo'),
                prodImageThree=request.FILES.get('prodImageThree'),
                prodImageFour=request.FILES.get('prodImageFour'),
                # prodImageUrl=request.FILES.get('prodImageUrl'),
            )            

            return JsonResponse({'message': 'product updated successfully'})
        else:
            return JsonResponse({'message': 'product not found'}, status=404)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)





@csrf_exempt
def specific_category(request, id):
    category = Category.objects.filter(id=id).first()  # Retrieve a single category by ID
    if category:
        category_data = {
            'ID': category.id,
            'cateName': category.cateName,
            'cateDescription': category.cateDescription,
            'cateImage': category.cateImage.url if category.cateImage else None,
        }
        return JsonResponse({'Category': category_data})
    else:
        return JsonResponse({'error': 'Category not found'}, status=404) 



def categoryDetails(request):
    category = Category.objects.all()
    category_list = []
    for categ in category:
        category_list.append({
            'ID': categ.id,
            'cateName': categ.cateName,
            'cateDescription': categ.cateDescription,
            'cateImage': categ.cateImage.url if categ.cateImage else None,  # Accessing the URL property
        })
    return JsonResponse({'Categories': category_list})    



@csrf_exempt
def categoryadd(request):
    if request.method == 'POST':
        try:
            addcategory = Category.objects.create(
                cateName=request.POST.get('cateName'),
                cateDescription=request.POST.get('cateDescription'),
                cateImage=request.FILES.get('cateImage'),
            )
            addcategory.save()
            return JsonResponse({'message': 'Category added successfully'})
        except ValidationError as e:
            return JsonResponse({'error': f'Validation Error: {e}'})
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {e}'})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'})



@csrf_exempt
def delCategory(request,id):
    delCategory=Category.objects.get(id=id)
    delCategory.delete()
    return JsonResponse({'message': 'category deleted successfully'})    


@csrf_exempt
def updatecategory(request, id):
    if request.method == 'POST':
        categories = Category.objects.filter(id=id)
        if categories.exists():
            category = categories.first()  # Get the first category object
            # Delete old image if it exists
            if 'cateImage' in request.FILES:
                if category.cateImage:  # Use category.cateImage instead of categories.cateImage
                    media_file = os.path.join(os.getcwd(), category.cateImage.path)
                    if os.path.isfile(media_file):
                        os.remove(media_file)
                        print(f"Deleted: {media_file}")

                category.cateName = request.POST.get('cateName')
                category.cateDescription = request.POST.get('cateDescription')
                category.cateImage = request.FILES['cateImage']
                category.save()  # Save the changes to the category object
                return JsonResponse({'message': 'Category updated successfully'})
            else:
                return JsonResponse({'message': 'Please provide an image'}, status=400)
        else:
            return JsonResponse({'message': 'Category not found'}, status=404)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)


@csrf_exempt
def spcific_subcategory(request, id):
    try:
        sub_category = SubCategory.objects.get(id=id)  # Retrieve the specific SubCategory
        sub_category_data = {  # Construct a dictionary containing the data of the specific subcategory
            'ID': sub_category.id,
            'subCateName': sub_category.subCateName,
            'subCateDescription': sub_category.subCateDescription,
            'subCateParent': sub_category.subCateParent.id if sub_category.subCateParent else None,
            'subCateImage': sub_category.subCateImage.url if sub_category.subCateImage else None,
        }
        return JsonResponse({'sub_category': sub_category_data})
    except SubCategory.DoesNotExist:
        return JsonResponse({'error': 'SubCategory does not exist'}, status=404)    

@csrf_exempt
def subcategoryDetails(request):
    sub_category = SubCategory.objects.all()
    sub_category_list = []

    for categ in sub_category:
        # Include subCateParent details (if desired)
        sub_category_parent_data = None
        if categ.subCateParent:
            sub_category_parent_data = {
                'ID': categ.subCateParent.id,
                'CateName': categ.subCateParent.cateName,  # Assuming 'name' field exists in Category
            }

        sub_category_list.append({
            'ID': categ.id,
            'subCateName': categ.subCateName,
            'subCateDescription': categ.subCateDescription,
            'subCateImage': categ.subCateImage.url if categ.subCateImage else None,
            'subCateParent': sub_category_parent_data,  # Include parent details as a dictionary
        })

    return JsonResponse({'sub_categories': sub_category_list})



      
@csrf_exempt
def addsub_category(request):
    if request.method == 'POST':
        try:
            # Get the Category instance corresponding to the provided subCateParent
            category_name = request.POST.get('subCateParent')
            category_instance = Category.objects.get(id=category_name)

            # Create the SubCategory instance
            sub_category = SubCategory.objects.create(
                subCateName=request.POST.get('subCateName'),
                subCateParent=category_instance,  # Assign the Category instance
                subCateDescription=request.POST.get('subCateDescription'),
                subCateImage=request.FILES.get('subCateImage'),
            )
            sub_category.save()
            return JsonResponse({'message': 'sub_category added successfully'})
        except ValidationError as e:
            return JsonResponse({'error': f'Validation Error: {e}'})
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {e}'})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'})

@csrf_exempt
def delsub_category(request,id):
    sub_category=SubCategory.objects.get(id=id)
    sub_category.delete()
    return JsonResponse({'message': 'category deleted successfully'})


@csrf_exempt
def updatesub_CateName(request, id):
    if request.method == 'POST':
        try:
            sub_category = SubCategory.objects.get(id=id)
        except SubCategory.DoesNotExist:
            return JsonResponse({'message': 'Subcategory not found'}, status=404)

        sub_category_name = request.POST.get('subCateName')
        sub_category_description = request.POST.get('subCateDescription')
        subCateParent_id = request.POST.get('subCateParent')

        # Retrieve the Category instance
        subCateParent = get_object_or_404(Category, id=subCateParent_id)

        if 'subCateImage' in request.FILES:
            # Delete old image if it exists
            if sub_category.subCateImage:
                media_file = os.path.join(os.getcwd(), sub_category.subCateImage.path)
                if os.path.isfile(media_file):
                    os.remove(media_file)
                    print(f"Deleted: {media_file}")

            # Update user with new image
            sub_category.subCateImage = request.FILES['subCateImage']

        # Update other fields
        sub_category.subCateName = sub_category_name
        sub_category.subCateDescription = sub_category_description
        sub_category.subCateParent = subCateParent
        sub_category.save()

        return JsonResponse({'message': 'Subcategory updated successfully'})
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)
    
    
    
    
    
# count all products and users for Chart

@csrf_exempt
def countAllProductsAndUsers(request):
    if request.method != 'GET':
        return JsonResponse({'message': 'Invalid request method. Use GET'}, status=405)

    products = Product.objects.all().count()
    vendor_count = User.objects.filter(usertype='vendor').count()
    customer_count = User.objects.filter(usertype='customer').count()

    data = {
        'total_products': products,
        'total_users': {
            'vendors': vendor_count,
            'customers': customer_count,
        },
    }
    return JsonResponse(data)



# count most selling products for Chart

def mostSellingProducts(request):
    top_n = request.GET.get('top_n', 10)
    try:
        top_n = int(top_n)  # Ensure top_n is an integer
    except ValueError:
        return JsonResponse({'error': 'Invalid top_n parameter'}, status=400)

    if top_n <= 0:
        return JsonResponse({'error': 'top_n must be a positive integer'}, status=400)
    product_quantities = OrderItem.objects.values('product_id').annotate(quantity=Sum('quantity'))

    top_selling_products = (
        product_quantities.order_by('-quantity')[:top_n]
    )

    product_data = []
    for entry in top_selling_products:
        product_id = entry['product_id']
        quantity = entry['quantity']
        try:
            product = Product.objects.get(pk=product_id)  
            product_data.append({
                'id': product.id, 
                'name': product.prodName,
                'quantity_sold': quantity,
            })
        except Product.DoesNotExist:
            pass
    return JsonResponse({'most_selling_products': product_data})



# count most frequent customers for Chart

def mostFrequentCustomers(request, top_n=10):
    try:
        top_n = int(top_n)  
    except ValueError:
        return JsonResponse({'error': 'Invalid top_n parameter'}, status=400)

    if top_n <= 0:
        return JsonResponse({'error': 'top_n must be a positive integer'}, status=400)
    
    customer_order_counts = User.objects.filter(usertype='customer').annotate(
        order_count=Count('order', filter=Q(order__status='D'))
    ).order_by('-order_count')[:top_n]

    customer_data = []
    for user in customer_order_counts:
        customer_data.append({
            'id': user.id,
            'name': f"{user.first_name} {user.last_name}" if user.first_name or user.last_name else user.username,
            'order_count': user.order_count,
        })

    return JsonResponse({'most_frequent_customers': customer_data})




# All Orders

@api_view(['GET'])
def get_orders(request):
    orders = Order.objects.all()
    orders_data = []

    for order in orders:
        order_data = {
            'order_id': order.id,
            'address': order.address,
            'phone_number': order.phone_number,
            'payment_status': order.payment_status,
            'payment_mode': order.payment_mode,
            'is_paid': order.is_paid,
            'user': order.user.id if order.user else None,
            'status': order.status,
            'total_price': order.total_price,
            'created_at': order.created_at,
            'products': []
        }

        # Include product details for each order item
        for order_item in order.orderitems.all():
            product_data = {
                'product_id': order_item.product.id,
                'product_name': order_item.product.prodName,
                'product_price': order_item.product.prodPrice,
                'quantity': order_item.quantity
            }
            order_data['products'].append(product_data)

        orders_data.append(order_data)

    return JsonResponse({'orders': orders_data})



# All Shipped Orders

@api_view(['PUT'])
def shipped_order(request, pk):
    order = get_object_or_404(Order, id=pk)
    
    if order.status == Order.PENDING_STATE:
        order.status = Order.SHIPPED_STATE
        order.save()
        return JsonResponse({'details': "Order is shipped"})
    else:
        return JsonResponse({'error': "Cannot cancel order with 'shipped' status."}, status=status.HTTP_403_FORBIDDEN)

