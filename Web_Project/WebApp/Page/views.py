from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from .models import Product, Order, Customer, CartItem, Cart
from django.db.models import Sum
from .forms import UserForm, SignUpForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


class Index_Page(TemplateView, LoginRequiredMixin):
    login_url = '/'
    template_name = '../Templates/Base_UI_WithoutLogIn.html'

    def get(self, request):
        sanpham = Product.objects.all()
        content = {
            'sanpham': sanpham
        }
        return render(request, self.template_name, content)


def Present_Page(request):
    template_name = '../Templates/NavigationBar/Present_Page.html'
    return render(request, template_name)


def Blog_Page(request):
    template_name = '../Templates/blog_post_without_login/blog_page.html'
    return render(request, template_name)


def Blog_Page_2(request):
    template_name = '../Templates/blog_post_without_login/blog_page_2.html'
    return render(request, template_name)


def Blog_Page_1_Post_1(request):
    template_name = '../Templates/blog_post_without_login/post-1.html'
    return render(request, template_name)


def Blog_Page_1_Post_2(request):
    template_name = '../Templates/blog_post_without_login/post-2.html'
    return render(request, template_name)


def Blog_Page_1_Post_3(request):
    template_name = '../Templates/blog_post_without_login/post-3.html'
    return render(request, template_name)


def Blog_Page_2_Post_4(request):
    template_name = '../Templates/blog_post_without_login/post-4.html'
    return render(request, template_name)


def Blog_Page_2_Post_5(request):
    template_name = '../Templates/blog_post_without_login/post-5.html'
    return render(request, template_name)


def Blog_Page_2_Post_6(request):
    template_name = '../Templates/blog_post_without_login/post-6.html'
    return render(request, template_name)

class Product_List(TemplateView, LoginRequiredMixin):
    login_url = '/'
    template_name = '../Templates/product-list.html'

    def get(self, request):
        sanpham = Product.objects.all()
        content = {
            'sanpham': sanpham
        }
        return render(request, self.template_name, content)


def Login_Page(request):
    template_name = '../Templates/NavigationBar/LogIn_Page.html'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect(reverse('Page:page_Index_User'))
            else:
                return render(request, template_name, {'error_message': 'Your account has been disabled'})
        else:
            return render(request, template_name, {'error_message': 'Đăng nhập không hợp lệ'})
    return render(request, template_name, {})


def Register_Page(request):
    template_name = '../Templates/NavigationBar/Register_Page.html'
    form = SignUpForm(request.POST)
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    return render(request, template_name, {'form': form})
    # return render(request, template_name, {})


def LogOut(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'NavigationBar/LogIn_Page.html', context)


class Index_User(TemplateView, LoginRequiredMixin):
    login_url = '/'
    template_name = '../Templates/Base_UI_WithLogIN.html'

    def get(self, request):
        if request.user.is_authenticated():
            sanpham = Product.objects.all()
            order = Order.objects.all()
            cartItem = CartItem.objects.all()
            user_id = User.objects.get(id=request.user.id)
            cart_id = Cart.objects.filter(id_user=user_id, is_new=True)
            numPro = CartItem.objects.filter(id_cart=cart_id).count()
            content = {
                'sanpham': sanpham,
                'order': order,
                'cartItem': cartItem,
                'numPro': numPro,
            }
            return render(request, self.template_name, content)
        else:
            return HttpResponseRedirect(reverse('Page:page_login'))


class ManagerView(TemplateView, LoginRequiredMixin):
    login_url = '/'
    template_name = '../Templates/Manager_View.html'

    def get(self, request):
        if request.user.is_authenticated():
            order = Order.objects.all()
            content = {
                'order': order,
            }
            return render(request, self.template_name, content)
        else:
            return HttpResponseRedirect(reverse('Page:page_login'))


class ViewDetail(TemplateView, LoginRequiredMixin):
    login_url = '/'
    template_name = '../Templates/Base_ViewDetail.html'

    def get(self, request, id_to):
        product_id = Product.objects.filter(id=id_to)
        content = {
            'product_id': product_id,
        }
        return render(request, self.template_name, content)


def AddCart(request):
    if request.is_ajax():
        id_sp = request.POST.get('id')
        num = request.POST.get('num')
        user = request.POST.get('user')

        proDetail = Product.objects.get(id=id_sp)
        User_id = User.objects.get(id=user)
        value = proDetail.price_sale * float(num)

        if Cart.objects.filter(id_user=User_id, is_new=True).exists():
            Cart_id = Cart.objects.get(id_user=User_id, is_new=True)
            if CartItem.objects.filter(id_product=proDetail, id_cart=Cart_id).exists():
                cartItem = CartItem.objects.get(id_product=proDetail, id_cart=Cart_id)
                numOld = cartItem.num
                cartItem.num = int(num) + numOld
                cartItem.sum_product = proDetail.price_sale * float(cartItem.num)
                cartItem.save()
            else:
                CartItem.objects.create(id_product=proDetail, id_cart=Cart_id, num=num, sum_product=value)
        else:
            Cart_id = Cart.objects.create(id_user=User_id, total_price=0)
            CartItem.objects.create(id_product=proDetail, id_cart=Cart_id, num=num, sum_product=value)

        html = render_to_string('addcart.html')
    return HttpResponse(html)


def Minus(request):
    if request.is_ajax():
        id_cartItem = request.POST.get('id')
        CartItem_id = CartItem.objects.get(id=id_cartItem)
        numOld = CartItem_id.num
        price_Each = CartItem_id.sum_product / CartItem_id.num
        CartItem_id.num = numOld - 1
        numNew = numOld - 1
        CartItem_id.sum_product = float(price_Each) * float(numNew)
        CartItem_id.save()
        html = render_to_string('minus_cart.html')
    return HttpResponse(html)


def Plus(request):
    if request.is_ajax():
        id_cartItem = request.POST.get('id')

        CartItem_id = CartItem.objects.get(id=id_cartItem)
        numOld = CartItem_id.num
        price_Each = CartItem_id.sum_product / CartItem_id.num
        CartItem_id.num = numOld + 1
        numNew = numOld + 1
        CartItem_id.sum_product = float(price_Each) * float(numNew)
        CartItem_id.save()
        html = render_to_string('plus_cart.html')
    return HttpResponse(html)


def Buy(request, id_user):
    address = request.POST.get('addressInputText', False)
    selected_value = request.POST.getlist('selected_product')

    User_id = get_object_or_404(User, id=id_user)
    cart_id = Cart.objects.get(id_user=User_id, is_new=True)

    if len(selected_value) == 0:
        pass
    else:
        if cart_id.is_new:
            cart_id.is_new = False
            cart_id.save()
        Order.objects.create(id_user=User_id, id_cart=cart_id, status='pending', address=address)
        Cart_id = Cart.objects.create(id_user=User_id, total_price=0)

        for item in selected_value:
            Product_id = get_object_or_404(Product, id=item)
            cartItem_id = CartItem.objects.get(id_cart=cart_id, id_product=Product_id)
            cartItem_id.is_checked = True
            cartItem_id.save()

        CartItem_id = CartItem.objects.filter(id_cart=cart_id, is_checked=False)
        for item in CartItem_id:
            item.id_cart = Cart_id
            item.save()

    return HttpResponseRedirect(reverse('Page:page_Index_User'))


class ViewCart(TemplateView, LoginRequiredMixin):
    login_url = '/'

    template_name = '../Templates/Base_ViewCart.html'

    def get(self, request, id_user):
        if request.user.is_authenticated():
            user_id = get_object_or_404(User, id=id_user)
            cart = Cart.objects.filter(id_user=user_id, is_new=True)
            cartItem = CartItem.objects.filter(id_cart=cart)
            num = 0
            for item in cartItem:
                num = num + item.sum_product
            content = {
                'cartItem': cartItem,
                'total': num,
            }
            return render(request, self.template_name, content)
        else:
            return HttpResponseRedirect(reverse('Page:page_login'))


class ViewProductUserBuy(TemplateView, LoginRequiredMixin):
    login_url = '/'
    template_name = '../Templates/Base_Product_User.html'

    # def get(self, request, id_user):
    #     if request.user.is_authenticated():
    #         user_id = get_object_or_404(User, id=id_user)
    #         order = Order.objects.filter(id_user=user_id)
    #         cartItem = CartItem.objects.all()
    #         content = {
    #             'order': order,
    #             'cartItem': cartItem,
    #         }
    #         return render(request, self.template_name, content)
    #     else:
    #         return HttpResponseRedirect(reverse('Page:page_login'))

    def get(self, request, id_user):
        if request.user.is_authenticated():
            user_id = get_object_or_404(User, id=id_user)
            order = Order.objects.filter(id_user=user_id)
            cartItem = CartItem.objects.all()
            content = {
                'order': order,
                'cartItem': cartItem,
            }
            return render(request, self.template_name, content)
        else:
            return HttpResponseRedirect(reverse('Page:page_login'))


class ViewHistory(TemplateView, LoginRequiredMixin):
    login_url = '/'
    template_name = '../Templates/Base_History.html'

    def get(self, request, id_user):
        if request.user.is_authenticated():
            user_id = get_object_or_404(User, id=id_user)
            order = Order.objects.filter(id_user=user_id, status="completed")
            cartItem = CartItem.objects.all()
            content = {
                'order': order,
                'cartItem': cartItem,
            }
            return render(request, self.template_name, content)
        else:
            return HttpResponseRedirect(reverse('Page:page_login'))


def DeleteCartItem(request, id_user, id_cartItem):
    CartItem.objects.filter(id=id_cartItem).delete()
    return HttpResponseRedirect(reverse('Page:page_BaseViewCart', kwargs={'id_user': id_user}))


def DeleteOrder(request, id_order):
    order_id = Order.objects.get(id=id_order)
    Cart_id = Cart.objects.get(id=order_id.id_cart.id)
    order_id.delete()
    Cart_id.delete()
    return HttpResponseRedirect(reverse('Page:page_Index_User'))


def CancelOrder(request, id_user, id_order):
    order_id = Order.objects.get(id=id_order)
    Cart_id = Cart.objects.get(id=order_id.id_cart.id)
    order_id.delete()
    Cart_id.delete()
    return HttpResponseRedirect(reverse('Page:page_ViewProductUserBuy', kwargs={'id_user': id_user}))


def confirm(request, id_order):
    order_id = Order.objects.get(id=id_order)
    order_id.status = 'confirm'
    order_id.save()
    return HttpResponseRedirect(reverse('Page:page_Manager'))


def shipping(request, id_order):
    order_id = Order.objects.get(id=id_order)
    order_id.status = 'shipping'
    order_id.save()
    return HttpResponseRedirect(reverse('Page:page_Manager'))


def paid(request, id_order):
    order_id = Order.objects.get(id=id_order)
    order_id.status = 'paid'
    order_id.save()
    return HttpResponseRedirect(reverse('Page:page_Manager'))


def completed(request, id_order):
    order_id = Order.objects.get(id=id_order)
    order_id.status = 'completed'
    order_id.save()
    return HttpResponseRedirect(reverse('Page:page_Manager'))


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect(reverse('Page:page_login'))
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })
