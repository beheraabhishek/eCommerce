from django.core.serializers import serialize
from django.http import HttpResponse
from django.shortcuts import render
from .models import MerchantModel, ProductModel
from django.views.generic import DeleteView, ListView, View
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .forms import MerchantForm, ProductForm


def logincheck(request):
    uname = request.POST['name']
    password = request.POST['password']
    if uname == 'admin':
        if password == 'admin':
            return render(request, 'adminapplication/welcome.html')
        else:
            return render(request, 'adminapplication/index.html', {'message': 'Invalid Password'})
    else:
        return render(request, 'adminapplication/index.html', {'message': 'Invalid Username'})


def addmerchant(request):
    try:
        res = MerchantModel.objects.all()[::-1][0]
        idno = int(res.id_no) + 407
    except IndexError:
        idno = 7003000
    password = 1234567890
    return render(request, 'adminapplication/addmerchant.html', {'idno': idno, 'password': password})


def savemerchant(request):
    try:
        username = request.POST['email']
        contact = request.POST['contact']
        name = request.POST['name']
        id_no = request.POST['idno']
        password = username[0]+contact[-1]+str(len(name)+int(id_no))+username[1]+username[2]
        MerchantModel(id_no=id_no, name=name, username=username, contact=contact, password=password).save()
        return render(request, 'adminapplication/welcome.html', {'message': 'Merchant Details Register'})
    except:
        try:
            res = MerchantModel.objects.all()[::-1][0]
            idno = int(res.id_no) + 407
        except IndexError:
            idno = 7003000
        password = 1234567890
        return render(request, 'adminapplication/addmerchant.html', {'idno': idno, 'password': password, 'erroremail': "EmailID Already Exits", 'errorcont': "Contact No Already Exits"})


class Checkuser(View):
    def get(self, request, username, password):
        try:
            res = MerchantModel.objects.get(username=username, password=password)
        except:
            data1 = json.dumps('Invalid Username & Password')
            return HttpResponse(data1, content_type='application/json', status=400)
        else:
            data = serialize('json', [res])
            return HttpResponse(data, content_type='application/json', status=200)


@method_decorator(csrf_exempt, name='dispatch')
class Changepassword(View):
    def put(self, request, email):
        d1 = request.body
        new_password = json.loads(d1)
        try:
            res = MerchantModel.objects.get(username=email)
            old_data = {'id_no': res.id_no,
                   'name': res.name,
                   'username': res.username,
                   'contact': res.contact,
                   'password': res.password}
        except:
            mes = json.dumps('Invalid Email Id')
            return HttpResponse(mes, content_type='application/json', status=400)
        else:
            old_data.update(new_password)
            merchant_update = MerchantForm(old_data, instance=res)
            if merchant_update.is_valid():
                merchant_update.save()
            mes = json.dumps("Password Updated Successfully")
            return HttpResponse(mes, content_type='application/json', status=200)


@method_decorator(csrf_exempt, name='dispatch')
class Changeoldpassword(View):
    def put(self, request, email, password):
        d2 = request.body
        new_password = json.loads(d2)
        try:
            res = MerchantModel.objects.get(username=email, password=password)
            old_data = {'id_no': res.id_no,
                        'name': res.name,
                        'username': res.username,
                        'contact': res.contact,
                        'password': res.password}
        except:
            mes = json.dumps('Invalid Email ID & Password')
            return HttpResponse(mes, content_type='application/json', status=400)
        else:
            old_data.update(new_password)
            merchant_update = MerchantForm(old_data, instance=res)
            if merchant_update.is_valid():
                merchant_update.save()
            mes = json.dumps("Password Updated Successfully")
            return HttpResponse(mes, content_type='application/json', status=200)


@method_decorator(csrf_exempt, name='dispatch')
class Saveproduct(View):
    def post(self, request):
        d = request.body
        pdata = json.loads(d)
        data = ProductForm(pdata)
        if data.is_valid():
            data.save()
            js = json.dumps('Product Data Added')
            return HttpResponse(js, content_type='application/json',status=200)
        else:
            js = json.dumps('Product No is Already Exists')
            return HttpResponse(js, content_type='application/json', status=400)


class ViewProduct(View):
    def get(self, request, idno):
        try:
           res = ProductModel.objects.filter(merchant_id=idno)
        except:
            data1 = json.dumps('Product Data Not Available')
            return HttpResponse(data1, content_type='application/json', status=400)
        else:
            data = serialize('json', res)
            return HttpResponse(data, content_type='application/json', status=200)


@method_decorator(csrf_exempt, name='dispatch')
class DeleteProduct(View):
    def delete(self, request, idno):
        res = ProductModel.objects.filter(product_no=idno).delete()
        if res[0]:
            message = json.dumps('Product Deleted')
            return HttpResponse(message, content_type='application/json')
        else:
            message = json.dumps('Given Id Is Invalid')
            return HttpResponse(message, content_type='application/json')


class UpdateRequest(View):
    def get(self, request, id):
        try:
           res = ProductModel.objects.get(product_no=id)
        except:
            data1 = json.dumps('Product Data Not Available')
            return HttpResponse(data1, content_type='application/json', status=400)
        else:
            data = serialize('json', [res])
            return HttpResponse(data, content_type='application/json', status=200)


@method_decorator(csrf_exempt, name='dispatch')
class SaveUpdate(View):
    def put(self, request, id_no):
        old_data = ProductModel.objects.get(product_no=id_no)
        old_data_dict = {'product_no': old_data.product_no,
                         'name': old_data.name, 'price': old_data.price,
                         'quantity': old_data.quantity, 'merchant': old_data.merchant_id}
        data = request.body
        new_data = json.loads(data)
        old_data_dict.update(new_data)
        ef = ProductForm(old_data_dict, instance=old_data)
        if ef.is_valid():
            ef.save()
            json_mess = json.dumps("Product Data is Updated")
            return HttpResponse(json_mess, content_type="application/json")
        if ef.errors:
            json_mess = json.dumps(ef.errors)
            return HttpResponse(json_mess, content_type="application/json")
