from django.db import models
from django.contrib import admin
# 額外 import 這個套件
from django.utils.translation import gettext_lazy as _
from django.urls import reverse  # 新增


class Vendor(models.Model):
    primary_key = True
    vendor_name = models.CharField(max_length=20)
    store_name = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=100)

    # 覆寫 __str__

    def __str__(self):
        return self.vendor_name

    # 新增
    def get_absolute_url(self):
        # return f"/vendor/{self.id}/"
        return reverse("vendors:vendorId", kwargs={'id': self.id})


class Food(models.Model):
    food_name = models.CharField(max_length=30)
    # 使用 Decimal 实例表示固定精度的十进制数的字段。它有两个必须的参数：
    # max_digits整數最多幾位
    # decimal_places小數點最多幾位
    price_name = models.DecimalField(max_digits=3, decimal_places=0)
    # ForeignKey，在 Django中是 多對一(many-to-one)的關聯，而前方的參數代表的意思就是對應到哪一個類別，
    # 這裡對應到的是 Vendor，
    # 而後方的 on_delete 代表的是當對應的類別被刪除之後，
    # 這些對應到別人的資料要怎麼被處理，
    # 而 CASCADE 就是一倂刪除
    food_vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)

    def __str__(self):
        return self.food_name

# 自行宣告 類別


class Morethanfifty(admin.SimpleListFilter):

    title = _('price')
    parameter_name = 'compareprice'  # url最先要接的參數

    def lookups(self, request, model_admin):
        return (
            ('>50', _('>50')),  # 前方對應下方'>50'(也就是url的request)，第二個對應到admin顯示的文字
            ('<=50', _('<=50')),
        )
    # 定義查詢時的過濾條件

    def queryset(self, request, queryset):
        if self.value() == '>50':
            return queryset.filter(price_name__gt=50)
        if self.value() == '<=50':
            return queryset.filter(price_name__lte=50)


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    # list_display = (field.name for field in Vendor._meta.fields)
    list_display = [field.name for field in Vendor._meta.fields]
    # list_display = ('id', 'vendor_name', 'store_name', 'phone_number', 'address')


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    #  list_display = ['id', 'food_name', 'price_name', 'food_vandor']
    list_display = [field.name for field in Food._meta.fields]
    # list_filter = ('price_name',)
    list_filter = (Morethanfifty,)
    fields = ['price_name']  # 顯示欄位
    exclude = ['food_name', 'food_vendor']
    search_fields = ('food_name', 'price_name')  # 搜尋欄位
    # ordering = ('price_name',) # 價格 由小到大 排序
    ordering = ('-price_name',)  # 價格 由大到小 排序
