from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .alipay import AliPay
import uuid
from urllib.parse import parse_qs
# Create your views here.
def index(request):
     return render(request,'index.html')
 
 
def bill(request):
    alipay = AliPay(
        appid="2021000119666477",
        app_notify_url='http://127.0.0.1:8000/alipay/check/',
        return_url='http://127.0.0.1:8000/alipay/show/',
        app_private_key_path=r'alipay/keys/private2048.txt', 
        alipay_public_key_path=r'alipay/keys/alipaypublic.txt', 
        debug=True,  
    )
    res=alipay.direct_pay(
        subject='Bittencoin',  
        out_trade_no=str(uuid.uuid4()), 
        total_amount='0.1',
    )
    url='https://openapi.alipaydev.com/gateway.do?{0}'.format(res)
    return redirect(url)
 
 
 
 
 
 
def show(request):
    if request.method == 'GET':
        alipay = AliPay(
            appid="2021000119666477",  
            app_notify_url='http://127.0.0.1:8000/alipay/check/',
            return_url='http://127.0.0.1:8000/alipay/show/',
            app_private_key_path=r'alipay/keys/private2048.txt', 
            alipay_public_key_path=r'alipay/keys/alipaypublic.txt', 
            debug=True, 
        )
        param=request.GET.dict() 
        sign=param.pop('sign', None)  
        statu = alipay.verify(param,sign)
        if statu:
            return redirect("Profile")
        else:
            return render(request, 'show.html', {'msg': 'Payment Failed'})
    else:
        return render(request, 'show.html', {'msg': 'Accept GET method only.'})
 
 
def check(request):
    if request.method=='POST':
        alipay=AliPay(appid="2021000119666477",
            app_notify_url='http://127.0.0.1:8000/alipay/check/', 
            return_url='http://127.0.0.1:8000/show_msg/', 
            app_private_key_path=r'alipay/keys/private2048.txt', 
            alipay_public_key_path=r'alipay/keys/alipaypublic.txt',  
            debug=True,
        )
        body=request.body.decode('utf-8')
        post_data = parse_qs(body)
        post_dict = {}
        for k, v in post_data.items():
            post_dict[k] = v[0]
        sign = post_dict.pop('sign', None)
        status = alipay.verify(post_dict, sign)
        if status:  # 支付成功
            return HttpResponse('Payment Success')
        else:
            return HttpResponse('Payment Failed')
    else:
        return HttpResponse('Accept POST method only')