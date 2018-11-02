from django.db import models

# Create your models here.
class Base(models.Model):
    # 图片
    img = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    trackid = models.CharField(max_length=10)

    class Meta:
        abstract = True

#　轮播图
class Wheel(Base):
    class Meta:
        db_table = 'axf_wheel'

class Nav(Base):
    class Meta:
        db_table = 'axf_nav'

class Mustbuy(Base):
    class Meta:
        db_table = 'axf_mustbuy'

class Shop(Base):
    class Meta:
        db_table = 'axf_shop'