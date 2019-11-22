from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from .models import Food, Vendor
from .forms import VendorForm
from .forms import RawVendorForm
from django.shortcuts import get_object_or_404 # 新增

# Create your views here.


def helloWorld(request):
    return HttpResponse("HI")


def vendorIndex(request):
    vendorList = Vendor.objects.all()
    context = {'vendorList': vendorList}
    return render(request, 'vendors/vendorAll.html', context)


def vendor_create_view(request):
    # form = VendorForm(request.POST or None)
    form = RawVendorForm(request.POST or None)
    if form.is_valid():
        # form.save()
        # print(form.cleaned_data)
        Vendor.objects.create(**form.cleaned_data)
        # form = VendorForm()
        form = RawVendorForm()

    context = {
        'form': form
    }
    return render(request, "vendors/vendorCreate.html", context)


def singleVendor(request, id):
    # vendorList = Vendor.objects.get(id=id)
    # vendorList = get_object_or_404(Vendor, id =id)
    vendorList = get_object_or_404(Vendor, id=id)
    # try:
    #     vendorList = Vendor.objects.get(id=id)
    # except Vendor.DoesNotExist:
    #     raise Http404
    context = {
        'vendorList': vendorList
    }
    return render(request, 'vendors/vendorSingle.html', context)
