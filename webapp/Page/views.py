from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
import datetime
from django.db.models import Q, Max, Count, F, Value, Sum
from django.utils import timezone
from datetime import timedelta
from django.contrib import auth
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import timedelta, date
from random import choice
from django.urls import reverse
from .models import Product, Cart, Custumer
from django.db.models.query import EmptyQuerySet
from django.db.models import Sum
from .forms import UserForm, SignUpForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def login(request):
	template_name = '../Templates/NavigationBar/LogIn_Page.html'
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				auth_login(request,user)
				sanpham = Product.objects.all()
				cart = Cart.objects.all()
				sum_cart = list(Cart.objects.filter(TTes__isnull=True).aggregate(Sum('num')).values())[0]
				content = {
					'sanpham': sanpham,
					'cart': cart,
					'sum_cart': sum_cart,
				}
				return HttpResponseRedirect(reverse('Page:page_Index_User'))
			else:
				return render(request, template_name, {'error_message':'Your account has been disabled'})
		else:
			return render(request, template_name, {'error_message': 'Invalid login'})
	return render(request, template_name, {})


def register_user(request):
	template_name = '../Templates/NavigationBar/Register_Page.html'
	form = SignUpForm(request.POST)
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/')
	return render(request, template_name, {'form': form})

def save_user(request):
	template_name = '../Templates/NavigationBar/Register_Page.html'
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		email = request.POST['email']
		name = request.POST['name']
		age = request.POST['age']
		address = request.POST['address']
		phone_number = request.POST['phone_number']
		sex = request.POST['sex']

		if User.DoesNotExist:
			user = User.objects.create_user(username, email, password)
			messages.success(request, "Success")
			customer = Custumer.objects.create(user=user, name=name, age=age, address=address, phone=phone_number, sex=sex)
			customer.save()
		else:
			return render(request, template_name, {'error_message':'Invalid!'})
	return HttpResponseRedirect('/index')

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, '../Templates/Navigation/LogIn_Page.html', context)

def Present_Page(request):
	template_name = '../Templates/NavigationBar/Present_Page.html'
	return render(request, template_name)

def Link(request):
	template_name = '../Templates/NavigationBar/Link_Page.html'
	return render(request, template_name)

def Blog(request):
	template_name = '../Templates/NavigationBar/Blog_Page.html'
	return render(request, template_name)

class Index_Page(TemplateView, LoginRequiredMixin):
	login_url = '/'
	template_name = '../Templates/Base_UI_WithoutLogIn.html'

	def get(self, request):
		sanpham = Product.objects.all()
		cart = Cart.objects.all()
		content = {
			'sanpham': sanpham,
			'cart': cart,
		}
		return render(request, self.template_name, content)

class Index_User(TemplateView, LoginRequiredMixin):
	login_url = '/'
	template_name = '../Templates/Base_UI_WithLogIN.html'

	def get(self, request):

		if request.user.is_authenticated():
			sanpham = Product.objects.all()
			cart = Cart.objects.all()
			carts = Cart.objects.filter(is_pay=True, confirm=False)
			sum_cart = list(Cart.objects.filter(TTes__isnull=True, confirm=False).aggregate(Sum('num')).values())[0]
			content = {
				'sanpham': sanpham,
				'cart': cart,
				'sum_cart': sum_cart,
				'carts': carts,
			}
			return render(request, self.template_name, content)
		else:
			return HttpResponseRedirect(reverse('Page:page_login'))

class AddCartEmpty(TemplateView, LoginRequiredMixin):
	login_url = '/'

	def get(self, request, id_sp, id_user):
		if request.user.is_authenticated():
			all_cart = Cart.objects.all()
			id_sanpham = get_object_or_404(Product, id=id_sp)
			user_id = get_object_or_404(User, id=id_user)
			value = id_sanpham.price
			add_cart = Cart.objects.create(user=user_id, product=id_sanpham, num=1, sum_product=value)
			return HttpResponseRedirect(reverse('Page:page_Index_User'))
		else:
			return HttpResponseRedirect(reverse('Page:page_login'))

class AddCart(TemplateView, LoginRequiredMixin):
	login_url = '/'

	def get(self, request, id_sp, id_user):
		if request.user.is_authenticated():
			print(type(id_user))
			all_cart = Cart.objects.all()
			id_sanpham = get_object_or_404(Product, id=id_sp)
			user_id = get_object_or_404(User, id=id_user)
			value = id_sanpham.price
			all_cart = Cart.objects.filter(
				product__id__endswith=id_sp,
			)
			all_cart_equal = Cart.objects.filter(
				product__id__endswith=id_sp,
				confirm=True,
			)
			if all_cart:
				for item in all_cart:
					if item.product.id == id_sanpham.id and item.TTes != None and item.is_pay == False:
						cart = Cart.objects.get(id=item.id)
						cart.TTes = None
						cart.save()
						break;
					elif item.product.id == id_sanpham.id and item.TTes == None and item.is_pay == False:
						cart = Cart.objects.get(id=item.id)
						num = cart.num + 1
						cart.sum_product = id_sanpham.price * num
						cart.num = num
						cart.save()
						break;
					elif item.product.id == id_sanpham.id and item.TTes == None and item.is_pay == True and item.is_old == False:
						add_cart = Cart.objects.create(user=user_id, product=id_sanpham, num=1, sum_product=value)
						update_cart = get_object_or_404(Cart, id=item.id)
						if update_cart:
							update_cart.is_old = True
							update_cart.save()
			else:
				add_cart = Cart.objects.create(user=user_id, product=id_sanpham, num=1, sum_product=value)

			return HttpResponseRedirect(reverse('Page:page_Index_User'))
		else:
			return HttpResponseRedirect(reverse('Page:page_login'))

class BaseViewCart(TemplateView, LoginRequiredMixin):
	login_url='/'
	template_name = '../Templates/Base_ViewCart.html'

	def get(self, request):
		if request.user.is_authenticated():
			cart = Cart.objects.filter(TTes=None, confirm=False)
			sum_cart = list(Cart.objects.filter(TTes__isnull=True, confirm=False).aggregate(Sum('num')).values())[0]
			content = {
				'cart': cart,
				'sum_cart': sum_cart,
			}
			return render(request, self.template_name, content)
		else:
			return HttpResponseRedirect(reverse('Page:page_login'))

class AddProduct(TemplateView, LoginRequiredMixin):
	login_url='/'

	def get(self, request, id_cart, id_product):
		id_cart = get_object_or_404(Cart, id=id_cart)
		id_product = get_object_or_404(Product, id=id_product)
		id_num = id_cart.num
		value_product = id_product.price
		nums = id_num + 1
		sum_product = value_product * nums
		try:
			if id_cart:
				id_cart.num = nums
				id_cart.sum_product = sum_product
			id_cart.save()
		except (KeyError, Cart.DoesNotExits):
			return HttpResponseRedirect(self.login_url)
		else:
			return HttpResponseRedirect(reverse('Page:page_BaseViewCart'))

class MinusProduct(TemplateView, LoginRequiredMixin):
	login_url='/'

	def get(self, request, id_cart, id_product):
		id_cart = get_object_or_404(Cart, id=id_cart)
		id_product = get_object_or_404(Product, id=id_product)
		id_num = id_cart.num
		value_product = id_product.price
		nums = id_num - 1
		sum_product = value_product * nums
		try:
			if id_cart:
				id_cart.num = nums
				id_cart.sum_product = sum_product
			id_cart.save()
		except (KeyError, Cart.DoesNotExits):
			return HttpResponseRedirect(self.login_url)
		else:
			return HttpResponseRedirect(reverse('Page:page_BaseViewCart'))


def DeleteCart(request, id_cart, id_product):
	cart_id = get_object_or_404(Cart,id=id_cart)
	product_id = get_object_or_404(Product, id=id_product)
	value_product = product_id.price
	datetimenow = datetime.datetime.today()
	if cart_id:
		cart_id.TTes = datetimenow
		cart_id.num = 1
		cart_id.sum_product = value_product
	cart_id.save()
	all_cart = Cart.objects.filter(TTes=None)
	if all_cart:
		return HttpResponseRedirect(reverse('Page:page_BaseViewCart'))
	else:
		return HttpResponseRedirect(reverse('Page:page_Index_User'))

def Buy(request, id_cart):
	id_cart = get_object_or_404(Cart, id=id_cart)
	if id_cart.is_pay == False:
		id_cart.is_pay = True
		id_cart.confirm = False
		id_cart.save()
	elif id_cart.is_pay == True:
		id_cart.is_pay = False
		id_cart.confirm = False
		id_cart.save()
	return HttpResponseRedirect(reverse('Page:page_BaseViewCart'))

def confirm(request, id_cart):
	id_cart = get_object_or_404(Cart, id=id_cart)
	if id_cart.confirm == False:
		id_cart.confirm = True;
		id_cart.save()
	return HttpResponseRedirect(reverse('Page:page_Index_User'))

class ViewSPUserBuy(TemplateView, LoginRequiredMixin):
	login_url = '/'
	template_name = '../Templates/Base_Product_User.html'

	def get(self, request, user_to):
		if request.user.is_authenticated():
			carts = Cart.objects.filter(confirm=True, user=user_to)
			sum_cart = list(Cart.objects.filter(TTes__isnull=True, confirm=False).aggregate(Sum('num')).values())[0]
			content = {
				'carts': carts,
				'sum_cart': sum_cart,
			}
			return render(request, self.template_name, content)
		else:
			return HttpResponseRedirect(reverse('Page:page_login'))

class ViewConfirmManager(TemplateView, LoginRequiredMixin):
	login_url = '/'
	template_name = '../Templates/Base_Confirm_Manager.html'

	def get(self, request):
		if request.user.is_authenticated():
			carts_confirm = Cart.objects.filter(confirm=True)
			content = {
				'carts_confirm': carts_confirm,
			}
			return render(request, self.template_name, content)
		else:
			return HttpResponseRedirect(reverse('Page:page_login'))

class ViewDetail(TemplateView, LoginRequiredMixin):
	login_url = '/'
	template_name = '../Templates/Base_ViewDetail.html'

	def get(self, request, id_to):
		id_sanpham = Product.objects.filter(id=id_to)
		content = {
			'id_sanpham': id_sanpham,
		}
		return render(request, self.template_name, content)

