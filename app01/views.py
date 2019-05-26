
import hashlib
from datetime import datetime
import hashlib
from django.contrib.auth import authenticate
from django.contrib.messages.storage import session
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
import random,string
from django.core.paginator import Paginator
from django.urls import reverse
from django_redis import get_redis_connection

from app01.captcha.image import ImageCaptcha
import re

# Create your views here.
from app01.models import TCategory, TBook, TUser, TAddress
from dangdangapp import settings


def index(request):
    name=request.COOKIES.get('txtUsername')
    if name:
        request.session['nuname'] = name

    nuname = request.session.get('nuname')
    nuname2 = request.GET.get('nuname')
    if nuname2 == '1':
        nuname = ''
        request.session.clear()

    eone = TCategory.objects.filter(category_pid__isnull=True)
    etwo = TCategory.objects.filter(category_pid__isnull=False)
    # for i in etwo:
    #     print(i)
        # pass
    # print(eone)
    # print(etwo,'13')
    new = TBook.objects.all().order_by("-shelves_date")[0:8]
    # print(new,'28')

    return render(request,"index.html",{"eone":eone,"etwo":etwo,"new":new,'nuname':nuname})


# def booklist(request):
#
#     return render(request,'booklist.html')


def book_det(request):
    nuname = request.session.get('nuname')
    # print(nuname,'111')
    nuname2 = request.GET.get('nuname')
    # print(nuname2,'222')
    if nuname2 == '1':
        nuname = ''
        del request.session['nuname']
    id = request.GET.get("id")
    # print(id,type(id))
    det = TBook.objects.filter(book_id = id)
    # print(det,type(det))

    return render(request,'Book details.html',{"det":det,'nuname':nuname})

def regist(request):
    id = TUser.objects.all().order_by("user_id")
    for i in id:
        print(i)

    return render(request,'register.html')

def getcaptcha(request):
    image = ImageCaptcha()
    rand_code = random.sample(string.ascii_letters+string.digits,5)
    rand_code = ''.join(rand_code)
    request.session['code'] = rand_code
    data = image.generate(rand_code)
    return HttpResponse(data,'image/png')


def hash_code(username, now):
    h = hashlib.md5()
    username += now
    h.update(username.encode())
    return  h.hexdigest()


def make_confirm_string(use):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    code_y = hash_code(use.user_email,now)
    # request.session['code_y'] = code_y
    # request.session['use'] = use
    return code_y


def send_email(username,code_y):

    subject = '验证注册'
    text_content = '欢迎访问注册当当，祝贺你收到了我的邮件，有幸收到我的邮件说明你及其幸运'
    html_content = '<p>感谢注册当当，<a href="http://{}:8000/app01/confirm/?email={}&code={}" target=blank>点我</a>，就能验证你的个人信息了，验证结束你就可以登录了！</p>'.format('127.0.0.1',username,code_y)
    msg = EmailMultiAlternatives(subject, text_content,settings.EMAIL_HOST_USER,[username])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def regist_handle(request):#注冊處理

    # try:
    #     with transaction.atomic():
    username = request.POST.get('user_name')
    password = request.POST.get('pwd')
    password2 = request.POST.get('cpwd')
    captcha = request.POST.get('txt_vcode')
    code = request.session.get('code')
    # id = TUser.objects.all().order_by("user_id")[0]
    # print(id,'59')
    # agreement = request.POST.get('chb_agreement')
    if captcha.upper() == code.upper() and password == password2:
        l = '23567898900fbnjdfnbkdnvlzksfdjgnolkdr!@#$%^&*()'
        salt = ''.join(random.sample(l, 6))
        s1 = hashlib.md5()
        s1.update(password.encode('utf8'))
        password = s1.hexdigest()
        # code_y = request.session.get('code_y')
        use = TUser.objects.create(user_email=username, user_password=password,user_status = 0)
        code_y = make_confirm_string(use)
        request.session['code_y'] = code_y

        send_email(username,code_y)


        request.session['nuname'] = username
        # use.save()
        return redirect('app01:registeok')
    else:
        return HttpResponse('注册失败')
    # if use:
    #     return redirect('app01:login')
    # except:
        # return HttpResponse('ASDA')
        # return redirect('app01:regist')


def checkname(request):
    name = request.GET.get('user_name')
    print(name,'11')
    result2 = TUser.objects.filter(user_email = name)
    print(result2,'11')
    if result2:
        return HttpResponse('该账号已被注册')
    elif not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',name) and not re.match(r'^1(3|4|5|7|8)\d{9}$',name):
        return HttpResponse('输入格式不正确')
    else:
        return HttpResponse(' ')

def checkpwd(request):
    userpwd1 = request.GET.get('pwd')
    userpwd2 = request.GET.get('cpwd')
    # print("1:"+userpwd1,"2"+userpwd2)
    print(userpwd1,userpwd2,'22')
    if userpwd1 == userpwd2:
        return HttpResponse(' ')
    else:
        return HttpResponse('两次密码不一致请再次输入')

def checknum(request):
    number = request.GET.get('txt_vcode')

    code = request.session.get('code')
    print(number, code)
    if number.upper() == code.upper():
        return HttpResponse(' ')
    else:
        return HttpResponse('验证码有误')

def checkallow(request):
    allow = request.GET.get('chb_agreement')
    print(allow)
    if allow == 'on':
        return HttpResponse('协议没有被同意')

# def logout(request):
#     logout(request)
#     return redirect(reverse('app01:index'))

def login(request):
    name = request.COOKIES.get('txtUsername')
    password = request.COOKIES.get('txtPassword')
    result = TUser.objects.filter(user_email=name,user_password=password)
    if result:
        request.session['nuname'] = name
        return render(request,'index.html')
    return render(request,'login.html')

def login_logic(request):
    username = request.POST.get("txtUsername")
    pwd = request.POST.get("txtPassword")
    print(username,pwd,'121')
    captcha = request.POST.get('txt_vcode')
    code = request.session.get('code')
    # if not all([username,pwd]):#验证完数据完整性
    #     return render(request,"login.html")
    l = '23567898900fbnjdfnbkdnvlzksfdjgnolkdr!@#$%^&*()'
    salt = ''.join(random.sample(l, 6))
    s1 = hashlib.md5()  # 创建sha1对象
    s1.update(pwd.encode('utf8'))  # 要先编码
    pwd = s1.hexdigest()
    user = TUser.objects.get(user_email=username)
    s = user.user_status
    user = TUser.objects.filter(user_email=username,user_password=pwd) #验证数据的正确性
    if user and s == '1':
        request.session['nuname'] = username  # 验证成功就添加session状态
        res = redirect('app01:index')
        res.set_cookie('txtUsername', username, max_age=7 * 24 * 3600)
        res.set_cookie('txtPassword', pwd, max_age=7 * 24 * 3600)  # 添加cookie
        return res

    else:
        # return render(request,"login.html")
        return HttpResponse('用户名或密码错误')


def confirm(request):
    email = request.GET.get('email')
    code = request.GET.get('code')
    # print(code,email,'aaa')
    try:
        user = TUser.objects.get(user_email=email)
    except:  # 用户不存在
        return HttpResponse('链接已失效')
    # 判断请求的注册码是否与数据库中该用户保存的一致
    old_code = request.session.get('code_y')
    # print(old_code,'bbb')
    if code != old_code:
        return HttpResponse('链接已失效')
    # 将该用户的状态改为可用
    user.user_status = '1'
    user.save()
    print(user.user_status,'ccc')

    # 直接登录，保存登录状态&用户名&用户id
    request.session['nuname'] = email

    request.session['login_userid'] = user.user_id
    return render(request, 'register ok.html', {'username': email,

                                                        'login_userid': request.session.get('login_userid'), })



def registeok(request):
        return render(request, 'register ok.html')

#分页显示
def list(request):
    eone = TCategory.objects.filter(category_pid__isnull=True)
    etwo = TCategory.objects.filter(category_pid__isnull=False)
    nuname = request.session.get('nuname')
    print(nuname, '111')
    nuname2 = request.GET.get('nuname')
    print(nuname2, '222')
    if nuname2 == '1':
        nuname = ''
        request.session.clear()

    number = request.GET.get("num")
    # print(number,'146')
    e = TBook.objects.all()
    pagtor = Paginator(e,per_page=3)
    try:
        number = int(number)
    except Exception as e:
        number = 1

    # if number >= pagtor.num_pages:
    #     number = 1

    s_page = pagtor.page(number)
    print(number,'157')
    num_pages = pagtor.num_pages
    if num_pages <5:
        pages = range(1,num_pages+1)
    elif number <= 3:
        pages = range(1,6)
    elif num_pages-number <= 2:
        pages = range(num_pages-4,num_pages+1)
    else:
        pages = range(number-2,number+3)

    return render(request,'booklist.html',{"s_page":s_page,"pages":pages,"nuname":nuname,'eone':eone,'etwo':etwo})


def caradd(request):    #购物车模块
    b = 0

    count = request.GET.get("count")
    id = request.GET.get("id")
    # print(count,'333',type(count))
    # print(id,'222',type(id))
    information = request.session.get('informate')
    # print(information, '00000000')
    request.session['carid'] = id
    if information:
        for i in information:
            if int(i['id']) == int(id):
                c = int(i['count'])+int(count)
                sums = c * int(i['book_price'])
                i['count']=c
                i['sums']=sums
                # information[b]=i
                request.session['informate']=information
                # print(information,'000000')
                return redirect("app01:book_det")
        table = TBook.objects.get(book_id=int(id))
        book_name = table.book_name
        book_price = table.book_price
        count = count
        sums = int(count)*int(book_price)
        l_sku = {"id": id, "book_name": book_name, "book_price": book_price, "count": count,'sums':sums}
        information.append(l_sku)
        # b += 1
        request.session['informate'] = information
        return redirect("app01:book_det")
    else:
        information = []
        table =TBook.objects.get(book_id=int(id))
        book_name= table.book_name
        book_price = table.book_price
        count = count
        sums = int(count)*int(book_price)
        l_sku = {"id": id, "book_name": book_name, "book_price": book_price, "count": count, "sums":sums}
        information.append(l_sku)
        # print(information,'22222222')
        request.session['informate']=information
        return redirect("app01:book_det")
    request.session['informate'] = information
    return redirect("app01:book_det")

def shoppingcar(request):
    name = request.COOKIES.get('txtUsername')
    if name:
        request.session['nuname'] = name

    nuname = request.session.get('nuname')
    nuname2 = request.GET.get('nuname')
    if nuname2 == '1':
        nuname = ''
        request.session.clear()
    information=request.session.get('informate')
    # print(information,'666')
    if information is None:
        return render(request,"car_k.html")
    s_sums = 0
    for i in information:
    # print(information,'222')
        s_sums += int(i['sums'])
    s_sums = s_sums
    return render(request,'car.html',{"information":information,'s_sums':s_sums,'nuname':nuname})

def shopadd(request):
    id = request.GET.get("id")
    # print(id,'274')
    information=request.session.get("informate")
    print(information)
    s_sum = 0
    for i in information:
        if i['id'] == id:
            count = int(i['count'])+1
            sums = int(i['book_price']) * count
            # print(count,sums,'11111')
            i['sums']=sums
            i['count']=count
        s_sum += int(i['sums'])
    s_sums=s_sum

    request.session['informate'] = information


    return JsonResponse({'count':count,'sums':sums,'s_sums':s_sums})


def shopdel(request):
    id = request.GET.get("id")
    information = request.session.get('informate')
    s_sum = 0
    for i in information:
        if i['id'] == id:
            count = int(i['count']) - 1
            sums = int(i['book_price']) * count
            # print(count, sums, '11111')
            i['sums'] = sums
            i['count'] = count
        s_sum += int(i['sums'])
    s_sums = s_sum
    request.session['informate'] = information

    return JsonResponse({'count':count, 'sums':sums,'s_sums':s_sums})

def shoudong(request):
    id = request.GET.get('id')
    count = request.GET.get('count')
    print(id,count,'333')
    information = request.session.get('informate')
    s_sum = 0
    for i in information:
        if i['id'] == id:
            count = count
            print(count,'666')
            sums = int(count)*int(i['book_price'])
            i['sums'] = sums
            i['count'] = count
        s_sum += int(i['sums'])
    s_sums = s_sum
    request.session['informate'] = information
    return JsonResponse({'count': count, 'sums': sums, 's_sums': s_sums})

def delete_s(request):
    id = request.GET.get("id")
    information = request.session.get('informate')
    if information[0] is None:
        return render(request,"car_k.html")
    for i in information:
        if i['id'] == id:
            information.remove(i)
            print(information,1111)
            request.session['informate']=information
            # return redirect('app01:shoppingcar')
    return redirect('app01:shoppingcar')


def indent(request):
    name = request.COOKIES.get('txtUsername')
    if name:
        request.session['nuname'] = name

    nuname = request.session.get('nuname')
    nuname2 = request.GET.get('nuname')
    if nuname2 == '1':
        nuname = ''
        request.session.clear()

    nuname = request.session.get('nuname')

    #检测用户是否登录
    if nuname: #已登录
        information = request.session.get('informate')
        # print(information,'666')

        s_sums = 0
        for i in information:
            # print(information,'222')
            s_sums += int(i['sums'])
        s_sums = s_sums
        m = TUser.objects.filter(user_email=nuname)
        se_add = m[0].taddress_set.all()
        # print(se_add,'111111111')

        m = TUser.objects.filter(user_email=nuname)
        se_add = m[0].taddress_set.all()
        # print(se_add, '0000')
        va = request.GET.get('value_s')
        print(va,type(va),'aaa')
        for s in se_add:
            name = s.name
            deta = s.detail_address
            telphone = s.telphone
            mobile = s.addr_mobile
            addid = str(s.id)
            print(addid,type(addid),'bbb')

            id = s.user_id
            if addid == va:
                print(123)
                return JsonResponse({'name': name, 'deta': deta, 'telphone': telphone, 'mobile': mobile})

        return render(request, 'indent.html', {"information": information, 's_sums': s_sums,'nuname':nuname,'se_add':se_add})

    else:  #未登录
        return render(request,'login.html')

# def indentx(request):
#     nuname = request.session('nuname')
#     print(nuname)
#     m = TUser.objects.filter(user_email=nuname)
#     se_add = m[0].taddress_set.all()
#     print(se_add, '0000')
#     va = request.GET.get('value_s')
#     print(va, '33')
#     for s in se_add:
#         name = s.name
#         deta = s.detail_address
#         telphone = s.telphone
#         mobile = s.addr_mobile
#         addid = s.id
#         id = s.user_id
#         if addid == va:
#             return JsonResponse({'name':name,'deta':deta,'telphone':telphone,'mobile':mobile})


def indent_ok(request):
    name = request.COOKIES.get('txtUsername')
    if name:
        request.session['nuname'] = name

    nuname = request.session.get('nuname')
    nuname2 = request.GET.get('nuname')
    if nuname2 == '1':
        nuname = ''
        request.session.clear()

    name = request.POST.get('ship_man')
    address = request.POST.get("ship_add")
    num = request.POST.get("ship_num")
    mp = request.POST.get("ship_mp")
    tp = request.POST.get("ship_tp")
    n = TUser.objects.get(user_email=nuname)
    n.taddress_set.create(name=name, detail_address=address,telphone=tp,addr_mobile=mp)
    print(n,111)


    # add_table = TAddress.objects.create(name=name, detail_address=address,telphone=tp,addr_mobile=mp,user_id=5)
    # add_table.save()
    information = request.session.get('informate')
    # print(information,'666')
    s_sums = 0
    for i in information:
        # print(information,'222')
        s_sums += int(i['sums'])
    s_sums = s_sums
    return render(request,'indent ok.html',{'nuname':nuname,'s_sums':s_sums})











