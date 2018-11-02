from django.shortcuts import render

# Create your views here.
from app.models import Wheel, Nav, Mustbuy, Shop


def home(request):
    wheels = Wheel.objects.all()
    navs = Nav.objects.all()
    mustbuys = Mustbuy.objects.all()
    shoplist = Shop.objects.all()
    shophead = shoplist[0]
    shoptab = shoplist[1:3]
    shopclass = shoplist[3:7]
    shopcommend = shoplist[7:11]
    # print(wheels)
    data = {
        'wheels': wheels,
        'navs': navs,
        'mustbuys': mustbuys,
        'shophead':shophead,
        'shoptab': shoptab,
        'shopclass': shopclass,
        'shopcommend': shopcommend,
    }

    return render(request, 'home/home.html', context=data)


def market(request):
    return render(request, 'market/market.html')


def cart(request):
    return render(request, 'cart/cart.html')


def mine(request):
    return render(request, 'mine/mine.html')