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
#---------------------------------------details------------------------------------------------------------------
def userDetails(request):
    users = User.objects.all()
    users_list = []
    for user in users:
        users_list.append({
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone': user.phone,
            'usertype': user.usertype,
            'Photo': user.imageUrl,
        })
    return JsonResponse({'users': users_list})
#---------------------------------------add------------------------------------------------------------------ 
 
@csrf_exempt  
def useradd(request):
    if request.method == 'POST':
            email = request.POST.get('email', '')
            ssn = request.POST.get('ssn', '')

            # Check if user with the same email already exists
            if User.objects.filter(email=email).exists() or User.objects.filter(ssn=ssn).exists():
                return JsonResponse({'error': 'User already exists'})
            
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
                ssn=request.POST.get('ssn', ''),
                # imageUrl=request.POST.get('imageUrl', ''),
                image=request.FILES.get('image', ''),
                
            )
            addUser.save()
            return JsonResponse({'message': 'User added successfully'})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'})   

#---------------------------------------delete------------------------------------------------------------------ 

def delete(request,id):
    delUser=User.objects.get(id=id)
    delUser.delete()
    return JsonResponse({'message': 'User deleted successfully'})
#---------------------------------------update------------------------------------------------------------------ 
@csrf_exempt
def update(request, id):
    if request.method == 'POST':
        updateUser = User.objects.filter(id=id)
        if updateUser.exists():
            # if updateUser.image and 'image' in request.FILES:
            #     media_file = os.path.join(os.getcwd(), updateUser.image.path)
            #     if os.path.isfile(media_file):
            #         os.remove(media_file)
            #         print(f"Deleted: {media_file}")
            updateUser.update(
                first_name=request.POST.get('first_name', ''),
                last_name=request.POST.get('last_name', ''),
                email=request.POST.get('email', ''),
                phone=request.POST.get('phone', ''),
                usertype=request.POST.get('usertype', ''),
                password=request.POST.get('password', ''),
                address=request.POST.get('address', ''),
                shopname=request.POST.get('shopname', ''),
                ssn=request.POST.get('ssn', ''),
                image=request.FILES.get('image', ''),
                
            )
            return JsonResponse({'message': 'User updated successfully'})
        else:
            return JsonResponse({'message': 'User not found'}, status=404)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)    
#------------------------------------------------------------------------------------------------
    






#================================================= Product =============================================================  
#---------------------------------------details------------------------------------------------------------------
def productDetails(request):
    # products = Product.objects.all()
    # product_list = []
    # for prod in products:
    #     product_dict = {
    #         'prodSubCategory': prod.prodSubCategory,
    #         'prodName': prod.prodName,
    #         'prodPrice': prod.prodPrice,
    #         'prodDescription': prod.prodDescription,
    #         'prodStock': prod.prodStock,
    #         'prodOnSale': prod.prodOnSale,
    #         'prodDiscountPercentage': prod.prodDiscountPercentage,
    #         'prodImageUrl': prod.prodImageUrl,
    #         'created_at': prod.created_at,
    #     }
    #     # Accessing fields from related User object
    #     if prod.prodVendor:
    #         product_dict['prodVendor'] = {
    #             'username': prod.prodVendor.username,
    #             'email': prod.prodVendor.email,
    #             # Add more fields as needed
    #         }
    #     product_list.append(product_dict)

    # return JsonResponse({'Products': product_list})

    products = Product.objects.all()
    product_list = []
    for prod in products:
        product_dict = {
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

@csrf_exempt
def productadd(request):
    if request.method == 'POST':
        try:
            # Fetch the user instance based on the provided username or ID
            prod_vendor_email = request.POST.get('prodVendor') 
            prod_vendor = User.objects.filter(email=prod_vendor_email)[0] 
            
            prod_categ_name = request.POST.get('prodSubCategory')
            prod_categ = SubCategory.objects.filter(subCateName=prod_categ_name)[0]
            
            addprod = Product.objects.create(
                prodVendor=prod_vendor,  # Assign the user instance
                prodName=request.POST.get('prodName'),
                prodPrice=request.POST.get('prodPrice'),
                prodDescription=request.POST.get('prodDescription'),
                prodSubCategory=prod_categ,
                prodStock=request.POST.get('prodStock'),
                prodOnSale=request.POST.get('prodOnSale'),
                prodDiscountPercentage=request.POST.get('prodDiscountPercentage'),
                prodImageThumbnail=request.POST.get('prodImageThumbnail'),
                prodImageOne=request.POST.get('prodImageOne'),
                prodImageTwo=request.POST.get('prodImageTwo'),
                prodImageThree=request.POST.get('prodImageThree'),
                prodImageFour=request.POST.get('prodImageFour'),
                prodImageUrl=request.POST.get('prodImageUrl'),
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
        prodUser = Product.objects.filter(id=id)
        if prodUser.exists():
            prodUser.update(
                prodVendor=request.POST.get('prodVendor'),
                prodName=request.POST.get('prodName'),
                prodPrice=request.POST.get('prodPrice'),
                prodDescription=request.POST.get('prodDescription'),
                # prodSubCategory=request.POST.get('prodSubCategory'),
                prodStock=request.POST.get('prodStock'),
                prodOnSale=request.POST.get('prodOnSale'),
                prodDiscountPercentage=request.POST.get('prodDiscountPercentage'),
                prodImageThumbnail=request.POST.get('prodImageThumbnail'),
                prodImageOne=request.POST.get('prodImageOne'),
                prodImageTwo=request.POST.get('prodImageTwo'),
                prodImageThree=request.POST.get('prodImageThree'),
                prodImageFour=request.POST.get('prodImageFour'),
                prodImageUrl=request.POST.get('prodImageUrl'),
            )
            return JsonResponse({'message': 'product updated successfully'})
        else:
            return JsonResponse({'message': 'product not found'}, status=404)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)    
#------------------------------------------------------------------------------------------------
    








#=============================================Category======================================================
#---------------------------------------details------------------------------------------------------------------

def categoryDetails(request):
    category = Category.objects.all()
    category_list = []
    for categ in category:
        category_list.append({
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
                cateImage=request.POST.get('cateImage'),
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
            categories.update(
                cateName=request.POST.get('cateName'),
                cateDescription=request.POST.get('cateDescription'),
                cateImage=request.POST.get('cateImage'),
            )
            return JsonResponse({'message': 'category updated successfully'})
        else:
            return JsonResponse({'message': 'category not found'}, status=404)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405) 
#-------------------------------------------------------------------------------------------------------------------------
















#=============================================sub Category======================================================
#---------------------------------------details------------------------------------------------------------------

def subcategoryDetails(request):
    sub_category = SubCategory.objects.all()
    sub_category_list = []
    for categ in sub_category:
        sub_category_list.append({
            'subCateName': categ.subCateName,
            'subCateDescription': categ.subCateDescription,
            'subCateImage': categ.subCateImage.url if categ.subCateImage else None,  # Accessing the URL property
        })
    return JsonResponse({'sub_categories': sub_category_list})    
#---------------------------------------add------------------------------------------------------------------
@csrf_exempt
def addsub_category(request):
    if request.method == 'POST':
        try:
            sub_category = SubCategory.objects.create(
                subCateName=request.POST.get('subCateName'),
                subCateDescription=request.POST.get('subCateDescription'),
                subCateImage=request.POST.get('subCateImage'),
            )
            sub_category.save()
            return JsonResponse({'message': 'sub_category added successfully'})
        except ValidationError as e:
            return JsonResponse({'error': f'Validation Error: {e}'})
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {e}'})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'})
#---------------------------------------delete------------------------------------------------------------------ 
def delsub_category(request,id):
    sub_category=SubCategory.objects.get(id=id)
    sub_category.delete()
    return JsonResponse({'message': 'category deleted successfully'})
#---------------------------------------update------------------------------------------------------------------ 
@csrf_exempt
def updatesub_CateName(request, id):
    if request.method == 'POST':
        sub_category = SubCategory.objects.filter(id=id)
        if sub_category.exists():
            sub_category.update(
                subCateName=request.POST.get('subCateName'),
                subCateDescription=request.POST.get('subCateDescription'),
                subCateImage=request.POST.get('subCateImage'),
            )
            return JsonResponse({'message': 'subCateName updated successfully'})
        else:
            return JsonResponse({'message': 'subCateName not found'}, status=404)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405) 


