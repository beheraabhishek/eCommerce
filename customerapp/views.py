from django.shortcuts import render, redirect
from adminapp.models import CustomerModel, ProductModel


def mainpage(request):
    try:
        name = request.session['user']
        pdata = ProductModel.objects.all()
        return render(request, 'customerapplication/welcome.html', {'data': name, 'pdata': pdata})
    except:
        pdata = ProductModel.objects.all()
        return render(request, 'customerapplication/homepage.html', {'pdata': pdata})


def register(request):
    try:
        res = CustomerModel.objects.all()[::-1][0]
        idno = int(res.id_no) + 407
    except IndexError:
        idno = 600325
    return render(request, 'customerapplication/register.html', {'idno': idno})


def savesignup(request):
    try:
        id_no = request.POST['uno']
        name = request.POST['name']
        contact = request.POST['cno']
        address = request.POST['address']
        email = request.POST['email']
        passw = request.POST['password']
        password = request.POST['conf_password']
        if passw == password:
            CustomerModel(id_no=id_no, name=name, contact=contact, address=address, email=email, password=password).save()
            return render(request, 'customerapplication/login.html', {'message': 'User Details Register'})
        else:
            try:
                res = CustomerModel.objects.all()[::-1][0]
                idno = int(res.id_no) + 407
            except IndexError:
                idno = 600325
            return render(request, 'customerapplication/register.html', {'idno': idno,"message1": 'Password Not Matched'})
    except:
        try:
            res = CustomerModel.objects.all()[::-1][0]
            idno = int(res.id_no) + 407
        except IndexError:
            idno = 600325
        return render(request, 'customerapplication/register.html', {'idno': idno, 'erroremail': "EmailID Already Exits", 'errorcont': "Contact No Already Exits"})


def logincheck(request):
    name = request.POST['name']
    passwod = request.POST['password']
    if '@' in name:
        try:
            CustomerModel.objects.get(email=name, password=passwod)
            request.session['user'] = name
            pdata = ProductModel.objects.all()
            return render(request, 'customerapplication/welcome.html', {'data': name, 'pdata': pdata})
        except:
            return render(request, 'customerapplication/login.html', {'message1': 'Username & Password Invalid'})
    else:
        try:
            CustomerModel.objects.get(contact=name, password=passwod)
            request.session['user'] = name
            pdata = ProductModel.objects.all()
            return render(request, 'customerapplication/welcome.html', {'data': name, 'pdata': pdata})
        except:
            return render(request, 'customerapplication/login.html', {'message2': 'Contact No & Password Invalid'})


def logoutCustomer(request):
    del request.session['user']
    request.session.clear()
    return redirect('main')
