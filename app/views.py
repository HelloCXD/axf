from django.shortcuts import render

# Create your views here.
from app.models import Wheel, Nav, Mustbuy, Shop, MainShow, Foodtypes, Goods


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


    data = {
        'foodtypes': foodtypes,
        'goodslist': goodslist,
        'categoryid': categoryid,
        'childTypleList': childTypleList,
        'childid': childid,
    }
    return render(request, 'market/market.html', context=data)


def cart(request):
    return render(request, 'cart/cart.html')


def mine(request):
    return render(request, 'mine/mine.html')