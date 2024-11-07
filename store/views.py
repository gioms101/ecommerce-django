from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView, View
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.core.mail import send_mail
from .models import Category, Product, ProductTag
from order.models import CartItem
from user.models import CustomUser
from user.forms import RegisterUserForm


# Create your views here.

class MainPage(ListView):
    model = Product
    template_name = 'index.html'
    context_object_name = 'products'
    queryset = Product.objects.join_related_tables()  # join_related_tables()  is custom method in managers.py
    paginate_by = 3


class CategoryPage(ListView):
    model = Product
    template_name = 'shop.html'
    context_object_name = 'products'
    queryset = Product.objects.join_related_tables()
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        searched = self.request.GET.get('searched')
        sorting_field = self.request.GET.get('sorting_products')
        slug = self.kwargs.get('slug')
        price = self.request.GET.get('rangeInput')
        product_tag = self.request.GET.get('product_tag')

        if slug:
            queryset = queryset.filter(category__name=slug)

        if price and price != '0':
            queryset = queryset.filter(price__lte=price)

        if product_tag:
            queryset = queryset.filter(tags__name=product_tag)

        elif searched:
            queryset = queryset.filter(name__contains=searched)
        elif sorting_field:
            queryset = queryset.order_by(sorting_field)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slug'] = self.kwargs.get('slug') or ''
        context['tags'] = ProductTag.objects.all()
        context['categories'] = Category.objects.filter(parent__name=context['slug'])
        return context

    def post(self, request, *args, **kwargs):  # invokes pre_save() signal to check product quantity in signals.py
        # handle product add to cart in POST request
        product_id = request.POST.get('product')
        cart_id = request.POST.get('cart')
        if product_id and cart_id:
            cart_item_obj = CartItem.objects.filter(cart_id=cart_id, product_id=product_id)
            if cart_item_obj.exists():
                cart_item_obj = cart_item_obj.first()
                cart_item_obj.quantity += 1
                cart_item_obj.save(update_fields=['quantity'])
            else:
                CartItem.objects.create(cart_id=cart_id, product_id=product_id)

        return self.get(request, *args, **kwargs)


class RegisterPage(CreateView):
    model = CustomUser
    form_class = RegisterUserForm
    template_name = 'register.html'
    success_url = reverse_lazy('store:category')

    def form_valid(self, form):
        response = super().form_valid(form)

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)

        if user:
            login(self.request, user)

        return response


class ContactView(TemplateView):
    template_name = 'contact.html'

    def post(self, request):
        if self.request.user.is_authenticated:
            subject = self.request.POST.get('subject')
            message = self.request.POST.get('message')
            if subject and message:
                send_mail(
                    subject,
                    message,
                    self.request.user.email,
                    [CustomUser.objects.get(username='admin').email],
                    fail_silently=False,
                )
                return render(request, 'contact.html', {'sent_message': True})
        else:
            return redirect('/login/?next=/contact/')


def handle_404(request, exception):
    return render(request, 'error_handling/404.html')


def handle_500(request):
    return render(request, 'error_handling/500.html')


class LogoutUser(View):
    def get(self, request):
        logout(self.request)
        return redirect(reverse_lazy('store:login'))


# def shop_detail(request, slug=None):
#     current_page = 'shop_detail'
#     if slug:
#         product = Product.objects.get(name=slug)
#     else:
#         product = Product.objects.first()
#
#     # 'categories' for category_fragment.html
#     categories = Category.objects.prefetch_related('product_set')
#
#     # 'products' for featured_products_fragment.html and scroll_products_fragment.html
#     products = Product.objects.prefetch_related('category')
#
#     return render(request, 'shop-detail.html', {'product': product, 'categories': categories,
#                                                 'products': products, 'current_page': current_page
#                                                 })
# def checkout_page(request):
#     return render(request, 'chackout.html')
