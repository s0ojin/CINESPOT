from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods
from .forms import CustomUserCreationForm
from django.http import JsonResponse

# Create your views here.
'''
<accounts앱의 views 함수>
- signup : 회원 생성 페이지 조회 & 단일 회원 데이터 생성 [GET & POST]
- login :  로그인 페이지 조회 & 세션 데이터 및 저장(로그인) [GET & POST]
- logout : 현재 사용자의 세션 데이터 삭제 (로그아웃) [GET & POST]
- profile : 사용자 상세 조회 페이지 (프로필 조회) [GET]
'''


# 회원 가입
@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.user.is_authenticated: 
        # ㄱㄱ 메인페이지
        return redirect('community:index')

    if request.method == 'POST': # 계정 생성 시
        form = CustomUserCreationForm(request.POST)
        if form.is_valid(): # 정보가 유효하면
            user = form.save() # 저장
            auth_login(request, user)
            # ㄱㄱ 메인페이지
            return redirect('community:index')
    else: # GET
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)

# 로그인
@require_http_methods(['GET', 'POST'])
def login(request):
    if request.user.is_authenticated:
        return redirect('community:index')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('community:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)