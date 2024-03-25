from django.shortcuts import render , redirect , reverse
from django.http import HttpRequest , HttpResponse
# Create your views here.
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

#===================================== log in / log out =================================================
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

@csrf_exempt
def admin_logout(request):
    logout(request)
    messages.success(request, "You have been logged out")  # Adds a success message
    return JsonResponse({'success': True})  # Returns a JSON response indicating success


#======================================= User ===================================================================
#-------------------------------------- Show specific user ------------------------------------------------------
@csrf_exempt
def specific_user(request, id):
    try:
        user = User.objects.get(id=id)
        user_data = {
            'ID': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone': user.phone,
            'usertype': user.usertype,
            'ssn': user.ssn,    
            'shopname': user.shopname,
            'Photo_URL': user.imageUrl,
            # 'Image': user.image,
        }
        return JsonResponse({'user': user_data})
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

#---------------------------------------details------------------------------------------------------------------
def userDetails(request):
    users = User.objects.all()
    users_list = []
    for user in users:
        users_list.append({
            'ID': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone': user.phone,
            'usertype': user.usertype,
            'ssn': user.ssn,
            'shopname': user.shopname,
            'Photo': user.imageUrl,
        })
    return JsonResponse({'users': users_list})
#---------------------------------------add------------------------------------------------------------------ 
 
# @csrf_exempt  
# def useradd(request):
#     if request.method == 'POST':
#             email = request.POST.get('email', '')
#             ssn = request.POST.get('ssn', '')

#             # Check if user with the same email already exists
#             if User.objects.filter(email=email).exists():
#                 return JsonResponse({'error': 'email already exists'})
#             elif User.objects.filter(ssn=ssn).exists():
#                 return JsonResponse({'error': 'SSN already exists'})
#             # If user does not exist, create a new user
#             addUser = User.objects.create(
#                 first_name=request.POST.get('first_name', ''),
#                 last_name=request.POST.get('last_name', ''),
#                 email=email,
#                 phone=request.POST.get('phone', ''),
#                 usertype=request.POST.get('usertype', ''),
#                 password=request.POST.get('password', ''),
#                 address=request.POST.get('address', ''),
#                 shopname=request.POST.get('shopname', ''),
#                 ssn=request.POST.get('ssn', ''),
#                 image=request.FILES.get('image', ''),
                
#             )
            
#             addUser.save()
#             return JsonResponse({'message': 'User added successfully'})
#     else:
#         return JsonResponse({'error': 'Only POST requests are allowed'})   

# @csrf_exempt
# def useradd(request):
#     if request.method == 'POST':
#         email = request.POST.get('email', '')
#         usertype = request.POST.get('usertype', '')

#         # Check if user with the same email already exists
#         if User.objects.filter(email=email).exists():
#             return JsonResponse({'error': 'email already exists'})

#         # If user does not exist, create a new user
#         addUser_data = {
#             'first_name': request.POST.get('first_name', ''),
#             'last_name': request.POST.get('last_name', ''),
#             'email': email,
#             'phone': request.POST.get('phone', ''),
#             'usertype': usertype,
#             'password': request.POST.get('password', ''),
#             'address': request.POST.get('address', ''),
#             'shopname': request.POST.get('shopname', ''),
#             'image': request.FILES.get('image', ''),
#         }

#         # Only include SSN if the user type is not 'customer'
#         if usertype != 'customer':
#             addUser_data['ssn'] = request.POST.get('ssn', '')

#         addUser = User.objects.create(**addUser_data)
#         addUser.save()

#         return JsonResponse({'message': 'User added successfully'})
#     else:
#         return JsonResponse({'error': 'Only POST requests are allowed'})

@csrf_exempt
def useradd(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')

        # Check if user with the same email already exists
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already exists'})

        # If user does not exist, create a new user
        addUser = User.objects.create(
            first_name=request.POST.get('first_name', ''),
            last_name=request.POST.get('last_name', ''),
            email=email,
            phone=request.POST.get('phone', ''),
            usertype=request.POST.get('usertype', ''),
            password=request.POST.get('password', ''),
            address=request.POST.get('address', ''),
            shopname=request.POST.get('shopname', ''),
            image=request.FILES.get('image', ''),
        )

        # Check if user type is 'vendor'
        if request.POST.get('usertype', '') == 'vendor':
            # Check if SSN is provided
            ssn = request.POST.get('ssn', '')
            if not ssn:  # If SSN is not provided, return an error
                addUser.delete()  # Remove the user created without SSN
                return JsonResponse({'error': 'SSN is required for vendors'})
            shopname = request.POST.get('shopname', '')
            if not shopname:
                addUser.delete()  # Remove the user created without shopname (optional)
                return JsonResponse({'error': 'Shop name is required'})

            # Set the SSN for the user and save
            addUser.ssn = ssn
            addUser.save()

        return JsonResponse({'message': 'User added successfully'})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'})

#---------------------------------------delete------------------------------------------------------------------ 
@csrf_exempt
def delete(request,id):
    delUser=User.objects.get(id=id)
    delUser.delete()
    return JsonResponse({'message': 'User deleted successfully'})
#---------------------------------------update------------------------------------------------------------------ 
@csrf_exempt
def update(request, id):
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
#------------------------------------------------------------------------------------------------
    








#================================================= Product =============================================================  
#---------------------------------------specific product------------------------------------------------------------------
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




#---------------------------------------details------------------------------------------------------------------
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

#---------------------------------------add------------------------------------------------------------------

# @csrf_exempt
# def productadd(request):
#     if request.method == 'POST':
#         try:
#             # Fetch the user instance based on the provided username or ID
#             prod_vendor_email = request.POST.get('prodVendor') 
#             prod_vendor = User.objects.filter(email=prod_vendor_email)[0] 
            
#             prod_categ_name = request.POST.get('prodSubCategory')
#             prod_categ = SubCategory.objects.filter(subCateName=prod_categ_name)[0]
            
#             addprod = Product.objects.create(
#                 prodVendor=prod_vendor,  # Assign the user instance
#                 prodName=request.POST.get('prodName'),
#                 prodPrice=request.POST.get('prodPrice'),
#                 prodDescription=request.POST.get('prodDescription'),
#                 prodSubCategory=prod_categ,
#                 prodStock=request.POST.get('prodStock'),
#                 prodOnSale=request.POST.get('prodOnSale'),
#                 prodDiscountPercentage=request.POST.get('prodDiscountPercentage'),
#                 prodImageThumbnail=request.FILES.get('prodImageThumbnail'),
#                 prodImageOne=request.FILES.get('prodImageOne'),
#                 prodImageTwo=request.FILES.get('prodImageTwo'),
#                 prodImageThree=request.FILES.get('prodImageThree'),
#                 prodImageFour=request.FILES.get('prodImageFour'),
#                 prodImageUrl=request.FILES.get('prodImageUrl'),
                
#                 created_at=timezone.now()  # or parse the provided date string
#             )
#             addprod.save()
#             return JsonResponse({'message': 'product added successfully'})
#         except ValidationError as e:
#             return JsonResponse({'error': f'Validation Error: {e}'})
#         except Exception as e:
#             return JsonResponse({'error': f'An error occurred: {e}'})
#     else:
#         return JsonResponse({'error': 'Only POST requests are allowed'})


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

#---------------------------------------delete------------------------------------------------------------------ 
def delproduct(request,id):
    delProduct=Product.objects.get(id=id)
    delProduct.delete()
    return JsonResponse({'message': 'Product deleted successfully'})
#---------------------------------------update------------------------------------------------------------------ 



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
                prodImageUrl=request.FILES.get('prodImageUrl'),
                
            )
            return JsonResponse({'message': 'product updated successfully'})
        else:
            return JsonResponse({'message': 'product not found'}, status=404)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)


#------------------------------------------------------------------------------------------------
    











#=============================================Category======================================================
#---------------------------------------specific category------------------------------------------------------------------
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

#---------------------------------------details------------------------------------------------------------------
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
#---------------------------------------add------------------------------------------------------------------
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
#---------------------------------------delete------------------------------------------------------------------ 
def delcategory(request,id):
    delCategory=Category.objects.get(id=id)
    delCategory.delete()
    return JsonResponse({'message': 'category deleted successfully'})    
#---------------------------------------update------------------------------------------------------------------ 

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
#-------------------------------------------------------------------------------------------------------------------------
















#=============================================sub Category======================================================
#---------------------------------------specific subcategory------------------------------------------------------------------
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

#---------------------------------------details------------------------------------------------------------------
def subcategoryDetails(request):
    sub_category = SubCategory.objects.all()
    sub_category_list = []
    for categ in sub_category:
        sub_category_list.append({
            'ID': categ.id,
            'subCateName': categ.subCateName,
            'subCateDescription': categ.subCateDescription,
            # 'subCateParent': categ.subCateParent,
            'subCateImage': categ.subCateImage.url if categ.subCateImage else None,  # Accessing the URL property
        })
    return JsonResponse({'sub_categories': sub_category_list})  


    
       
#---------------------------------------add------------------------------------------------------------------
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







# @csrf_exempt
# def addsub_category(request):
#     if request.method == 'POST':
#         try:
#             # Get the Category instance corresponding to the provided subCateParent
#             category_name = request.POST.get('subCateParent')
#             category_instance = Category.objects.get(cateName=category_name)

#             # Create the SubCategory instance
#             sub_category = SubCategory.objects.create(
#                 subCateName=request.POST.get('subCateName'),
#                 subCateParent=category_instance,  # Assign the Category instance
#                 subCateDescription=request.POST.get('subCateDescription'),
#                 subCateImage=request.FILES.get('subCateImage'),
#             )
#             sub_category.save()
#             return JsonResponse({'message': 'sub_category added successfully'})
#         except ValidationError as e:
#             return JsonResponse({'error': f'Validation Error: {e}'})
#         except Exception as e:
#             return JsonResponse({'error': f'An error occurred: {e}'})
#     else:
#         return JsonResponse({'error': 'Only POST requests are allowed'})
#---------------------------------------delete------------------------------------------------------------------ 
def delsub_category(request,id):
    sub_category=SubCategory.objects.get(id=id)
    sub_category.delete()
    return JsonResponse({'message': 'category deleted successfully'})
#---------------------------------------update------------------------------------------------------------------ 

# @csrf_exempt
# def updatesub_CateName(request, id):
#     if request.method == 'POST':
#         try:
#             sub_category = SubCategory.objects.get(id=id)
#         except SubCategory.DoesNotExist:
#             return JsonResponse({'message': 'Subcategory not found'}, status=404)

#         sub_category_name = request.POST.get('subCateName')
#         sub_category_description = request.POST.get('subCateDescription')
#         subCateParent = request.POST.get('subCateParent')

#         if 'subCateImage' in request.FILES:
#             # Delete old image if it exists
#             if sub_category.subCateImage:
#                 media_file = os.path.join(os.getcwd(), sub_category.subCateImage.path)
#                 if os.path.isfile(media_file):
#                     os.remove(media_file)
#                     print(f"Deleted: {media_file}")

#             # Update user with new image
#             sub_category.subCateImage = request.FILES['subCateImage']

#         # Update other fields
#         sub_category.subCateName = sub_category_name
#         sub_category.subCateDescription = sub_category_description
#         sub_category.subCateParent = subCateParent
#         sub_category.save()

#         return JsonResponse({'message': 'Subcategory updated successfully'})
#     else:
#         return JsonResponse({'message': 'Invalid request method'}, status=405)

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