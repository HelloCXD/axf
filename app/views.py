import hashlib
import os
import uuid


from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from AXF import settings
from app.models import Wheel, Nav, Mustbuy, Shop, MainShow, Foodtypes, Goods, User, Cart


def home(request):
    wheels = Wheel.objects.all()
    navs = Nav.objects.all()
    mustbuys = Mustbuy.objects.all()
    shoplist = Shop.objects.all()
    shophead = shoplist[0]
    shoptab = shoplist[1:3]
    shopclass = shoplist[3:7]
    shopcommend = shoplist[7:11]

    # 商品主体内容
    mainshows = MainShow.objects.all()

    # print(wheels)
    data = {
        'wheels': wheels,
        'navs': navs,
        'mustbuys': mustbuys,
        'shophead':shophead,
        'shoptab': shoptab,
        'shopclass': shopclass,
        'shopcommend': shopcommend,
        'mainshows': mainshows,
    }

    return render(request, 'home/home.html', context=data)



# categoryid 分类ID
# childid 子类ID
# sortid 排序ID


def market(request,categoryid, childid, sortid):
    # 分类信息
    foodtypes = Foodtypes.objects.all()

    # 分类 点击小标
    typeIndex = int(request.COOKIES.get('typeIndex', 0))
    # 根据分类下标获取对应的分类ＩＤ
    categoryid = foodtypes[typeIndex].typeid

    # 子类信息
    childtypenames = foodtypes.get(typeid=categoryid).childtypenames

    # 拆分子类
    # print(childid)
    childTypleList = []
    for item in childtypenames.split('#'):
        list = item.split(':')
        dir = {
            'childname': list[0],
            'childid': list[1]
        }
        childTypleList.append(dir)
    # print(childTypleList)
    # 商品信息－根据分类ｉｄ获取对应的数据
    # goodslist = Goods.objects.all()
    if childid == '0': # 全部分类
        # print(1)

        goodslist = Goods.objects.filter(categoryid=categoryid)
        # print(goodslist)
    else:   # 分类下的子类
        # print(categoryid,childid)
        goodslist = Goods.objects.filter(categoryid=categoryid).filter(childcid=childid)
        # print(goodslist)

    # 排序
    if sortid == '1':
        goodslist = goodslist.order_by('-productnum')
    elif sortid == '2':
        goodslist = goodslist.order_by('price')
    elif sortid == '3':
        goodslist = goodslist.order_by('-price')

    # 购物车数据
    token = request.session.get('token')
    carts = []
    if token:   # 根据用户，获取对应用户下所有购物车数据
        user = User.objects.get(token=token)
        carts = Cart.objects.filter(user=user)


    data = {
        'foodtypes': foodtypes,
        'goodslist': goodslist,
        'categoryid': categoryid,
        'childTypleList': childTypleList,
        'childid': childid,
        'carts': carts
    }
    return render(request, 'market/market.html', context=data)


def cart(request):
    token = request.session.get('token')
    if token:
        user = User.objects.get(token=token)
        carts = Cart.objects.filter(user=user)

        return render(request, 'cart/cart.html', context={'carts': carts})
    else:
        return redirect('app:login')

def mine(request):
    # 获取用户信息
    token = request.session.get('token')

    responseData = {}

    if token:  # 登录
        user = User.objects.get(token=token)
        responseData['name'] = user.name
        responseData['rank'] = user.rank
        responseData['img'] = '/static/uploads/' + user.img
        responseData['isLogin'] = 1
    else:  # 未登录
        responseData['name'] = '未登录'
        responseData['img'] = '/static/uploads/axf.png'

    return render(request, 'mine/mine.html', context=responseData)


def registe(request):
    if request.method == 'GET':
        print(1)
        return render(request, 'mine/registe.html')
    elif request.method == 'POST':
        print(2)
        user = User()
        user.name = request.POST.get('name')
        user.password = genarate_password(request.POST.get('password'))
        user.account = request.POST.get('account')
        user.phone = request.POST.get('phone')
        user.addr = request.POST.get('addr')


        # 头像上传
        imgName = user.account + '.png'
        imgPath = os.path.join(settings.MEDIA_ROOT, imgName)
        file = request.FILES.get('icon')
        with open(imgPath, 'wb') as fp:
            for data in file.chunks():
                fp.write(data)
        user.img = imgName
        print(user.account, user.password, user.name, user.phone, user.addr)
        user.token = str(uuid.uuid5(uuid.uuid4(), 'registe'))
        print(user.token)
        user.save()
        print(4)

        # 状态保持
        request.session['token'] = user.token

        return redirect('app:mine')




def checkaccount(request):
    account = request.GET.get('account')

    responseDate = {
        'msg': '账号可用',
        'status': 1  # 1为可用，　－１为不可用

    }

    try:
        user = User.objects.get(account=account)
        responseDate['msg'] = '账号已被注册'
        responseDate['status'] = -1

        return JsonResponse(responseDate)
    except:
        return JsonResponse(responseDate)


def login(request):
    if request.method == 'GET':
        return render(request, 'mine/login.html')
    elif request.method == 'POST':
        account = request.POST.get('account')
        password = request.POST.get('password')

        try:
            user = User.objects.get(account=account)
            print('try'+user.account)
            if user.password == genarate_password(password):    # 登录成功

                # 更新token
                print(1)
                user.token = str(uuid.uuid5(uuid.uuid4(), 'login'))
                user.save()

                # 状态保持
                request.session['token'] = user.token
                return redirect('app:mine')
            else:   # 登录失败
                return render(request, 'mine/login.html', context={'passwdErr': '密码错误!'})
        except:
            print('e'+ account)
            return render(request, 'mine/login.html', context={'acountErr':'账号不存在!'})


def logout(request):
    request.session.flush()

    return redirect('app:mine')

def genarate_password(param):
    sha = hashlib.sha256()
    sha.update(param.encode('utf-8'))
    return sha.hexdigest()


def addcart(request):
    goodsid = request.GET.get('goodsid')
    token = request.session.get('token')

    responseData = {
        'msg': '添加购物车成功',
        'status': 1
    }

    if token: # 已登录
        user = User.objects.get(token=token)
        goods = Goods.objects.get(pk=goodsid)

        # 判断商品是否在购物车中
        carts = Cart.objects.filter(user=user).filter(goods=goods)
        if carts.exists():
            cart = carts.first()
            cart.number = cart.number + 1
            cart.save()
            responseData['number'] = cart.number
        else:
            cart = Cart()
            cart.user = user
            cart.goods = goods
            cart.number = 1
            cart.save()

            responseData['number'] = cart.number

        return JsonResponse(responseData)
    else: #　未登录
        responseData['msg'] = '请登录后操作'
        responseData['status'] = -1
        return JsonResponse(responseData)



def subcart(request):
    goodsid = request.GET.get('goodsid')
    print(goodsid)
    token = request.session.get('token')
    print(token)

    user = User.objects.get(token=token)
    goods = Goods.objects.get(pk=goodsid)

    cart = Cart.objects.filter(user=user).filter(goods=goods).first()
    print(cart)
    cart.number = cart.number - 1
    print(cart.number)
    cart.save()

    responseData = {
        'msg': '购物车减操作成功',
        'status': 1,
        'number': cart.number
    }
    return JsonResponse(responseData)