from django.conf.urls import url

from .views import (
    Index_Page,
    Present_Page,
    Blog_Page,
    Login_Page,
    Register_Page,
    LogOut,
    Index_User,
    ViewDetail,
    AddCart,
    ViewCart,
    Buy,
    ViewProductUserBuy,
    DeleteCartItem,
    confirm,
)

urlpatterns = [
    url('^$', Index_Page.as_view(), name='page_Index_Page'),
    url(r'^present/$', Present_Page, name='page_present_page'),
    url(r'^blog/$', Blog_Page, name='page_blog_page'),
    url(r'^login_user/$', Login_Page, name='page_login'),
    url(r'^register_user/$', Register_Page, name='page_register_user'),
    url(r'^logout_user/$', LogOut, name='page_logout_user'),
    url(r'^index/$', Index_User.as_view(), name='page_Index_User'),
    url(r'^view_detail/(?P<id_to>\w+)/$', ViewDetail.as_view(), name='page_ViewDetail'),
    url(r'^add_cart/(?P<id_sp>\w+)/(?P<id_user>\w+)/$', AddCart.as_view(), name='page_AddCart'),
    url(r'^view_cart/(?P<id_user>\w+)/$', ViewCart.as_view(), name='page_BaseViewCart'),
    url(r'^is_buy/(?P<id_user>\w+)/$', Buy, name='page_Buy'),
    url(r'^view_sanpham/(?P<id_user>\w+)/$', ViewProductUserBuy.as_view(), name='page_ViewProductUserBuy'),
    url(r'^delete_product/(?P<id_cart>\w+)/isproduct/(?P<id_product>\w+)/$', DeleteCartItem, name='page_DeleteCart'),
    url(r'^confirm/(?P<id_order>\w+)/$', confirm, name='page_confirm'),
]