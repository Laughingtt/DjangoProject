import os
import mimetypes
from django.shortcuts import render, redirect
from django.http import FileResponse
from django.conf import settings
# import xlrd

from web import models
from web.forms.customer import CustomerForm


def customer_list(request):
    """
    客户列表
    :return:
    """
    data_list = models.Customer.objects.all()

    return render(request, 'customer_list.html', {'data_list': data_list})


def customer_add(request):
    """
    编辑客户
    :return:
    """
    if request.method == 'GET':
        form = CustomerForm()
        return render(request, 'customer_edit.html', {'form': form})
    form = CustomerForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/customer/list/')
    return render(request, 'customer_edit.html', {'form': form})


def customer_edit(request, cid):
    """
    新增客户
    :return:
    """
    obj = models.Customer.objects.get(id=cid)
    if request.method == 'GET':
        form = CustomerForm(instance=obj)
        return render(request, 'customer_add.html', {'form': form})
    form = CustomerForm(data=request.POST, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('/customer/list/')
    return render(request, 'customer_add.html', {'form': form})


def customer_del(request, cid):
    """
    删除客户
    :param request:
    :param cid:
    :return:
    """
    models.Customer.objects.filter(id=cid).delete()
    return redirect('/customer/list/')


