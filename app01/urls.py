from django.urls import path
from app01 import views

app_name = 'app01'

urlpatterns = [
    path('index/',views.index,name = 'index'),
    path('book_det/',views.book_det,name = 'book_det'),
    # path('booklist/',views.booklist,name = 'booklist'),
    path('regist/',views.regist, name = 'regist'),
    path('regist_handle/',views.regist_handle, name = 'regist_handle'),
    path('getcaptcha/',views.getcaptcha,name = 'getcaptcha'),
    path('checkname/',views.checkname,name = 'checkname'),
    path('checkpwd/',views.checkpwd,name = 'checkpwd'),
    path('checknum/',views.checknum,name = 'checknum'),
    path('checkallow/',views.checkallow,name = 'checkallow'),
    path('login/',views.login,name = 'login'),
    path('login_logic/',views.login_logic,name="login_logic"),
    path('list/',views.list,name = "list"),
    path('caradd/',views.caradd,name = 'caradd'),
    path('shoppingcar/',views.shoppingcar,name = 'shoppingcar'),
    path('registeok/',views.registeok,name = 'registeok'),
    path('shopadd/',views.shopadd,name = 'shopadd'),
    path('shopdel/',views.shopdel,name = 'shopdel'),
    path('delete_s/',views.delete_s,name = 'delete_s'),
    path('indent/',views.indent,name = 'indent'),
    path('indent_ok/',views.indent_ok,name = 'indent_ok'),
    path('shoudong/',views.shoudong,name = 'shoudong'),
    # path('indentx/',views.indentx,name = 'indentx')
    path('confirm/',views.confirm,name = 'confirm')
]
