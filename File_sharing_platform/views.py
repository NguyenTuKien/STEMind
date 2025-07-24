from unicodedata import category
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import File, Category
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout

def home(request):
    categories = Category.objects.all()
    featured_files = File.objects.filter(file_status=1).order_by('-file_views')[:3]
    recently_files = File.objects.filter(file_status=1).order_by('-created_at')[:10]
    top_users = User.objects.annotate(num_posts=Count('Files')).order_by('-num_posts')[:10]
    context = {
        'categories':categories,
        'featured_files':featured_files,
        'recently_files':recently_files,
        'top_users':top_users
    }
    return render(request, 'home.html', context)

def enter(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Tài khoản hoặc mật khẩu không chính xác!')
        else:
            messages.error(request, 'Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu!')
    return render(request, 'enter.html')    

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes for Bootstrap styling
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'username'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'name@example.com'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'password'
        })

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tài khoản đã được tạo thành công!')
            return redirect('enter')
    else:
        form = RegisterForm()
    context = {
        'form':form
    }
    return render(request, 'register.html', context)

def user_logout(request):
    logout(request)
    return redirect('home')

def posts_by_category(request, category_name):
    categories = Category.objects.all()
    category = get_object_or_404(Category, category_name=category_name)
    featured_files = File.objects.filter(file_status=1, category=category).order_by('-file_views')[:3]
    recently_files = File.objects.filter(file_status=1, category=category).order_by('-created_at')[:15]
    top_users = User.objects.annotate(num_posts=Count('Files', filter=Q(Files__category=category))).order_by('-num_posts')[:10]
    context = {
        'categories':categories,
        'featured_files':featured_files,
        'recently_files':recently_files,
        'top_users':top_users
    }
    return render(request, 'home.html', context)

def file_detail(request, title):
    categories = Category.objects.all()
    file_obj = get_object_or_404(File, title=title)
    
    # Tăng lượt view
    file_obj.file_views += 1
    file_obj.save(update_fields=['file_views'])
    
    related_files = File.objects.filter(file_status=1, category=file_obj.category).exclude(id=file_obj.id).order_by('-file_views')[:5]
    top_users = User.objects.annotate(num_posts=Count('Files', filter=Q(Files__category=file_obj.category))).order_by('-num_posts')[:5]
    context = {
        'file': file_obj,
        'categories':categories,
        'related_files':related_files,
        'top_users':top_users
    }
    return render(request, 'file_detail.html', context)

# Alias để tương thích với template cũ
