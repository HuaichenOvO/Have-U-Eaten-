from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .alipay import AliPay
import uuid
from urllib.parse import parse_qs
# Create your views here.
def index(request):
     return render(request,'index.html')
 
 
def dingdan(request):
    # 实例化AliPay
    alipay = AliPay(
        appid="2021000119666477",
        app_notify_url='http://127.0.0.1:8000/alipay/check/',#支付宝会向这个地址发送post请求
        return_url='http://127.0.0.1:8000/alipay/show/',#支付宝会向这个地址发送get请求
        app_private_key_path=r'C:/Users/24654/Desktop/project/frontend/django/pay/keys/private2048.txt',  # 应用私钥
        alipay_public_key_path=r'C:/Users/24654/Desktop/project/frontend/django/pay/keys/alipay_public.txt',  # 支付宝公钥
        debug=True,  # 默认是False
    )
    # 定义请求地址传入的参数
    res=alipay.direct_pay(
        subject='Bittencoin',  # 商品描述
        out_trade_no=str(uuid.uuid4()),  # 订单号
        total_amount='0.1',  # 交易金额(单位是元，保留两位小数)
    )
    #生成跳转到支付宝支付页面的url
    url='https://openapi.alipaydev.com/gateway.do?{0}'.format(res)
    return redirect(url)
 
 
 
 
 
 
def show(request):
    if request.method == 'GET':
        alipay = AliPay(
            appid="2021000119666477",  
            app_notify_url='http://127.0.0.1:8000/alipay/check/',
            return_url='http://127.0.0.1:8000/alipay/show/',
            app_private_key_path=r'C:/Users/24654/Desktop/project/frontend/django/pay/keys/private2048.txt',  # 应用私钥
            alipay_public_key_path=r'C:/Users/24654/Desktop/project/frontend/django/pay/keys/alipay_public.txt',  # 支付宝公钥
            debug=True,  # 默认是False
        )
        param=request.GET.dict()  # 获取请求携带的参数并转换成字典类型
        sign=param.pop('sign', None)  # 获取sign的值
        # 对sign参数进行验证
        statu = alipay.verify(param,sign)
        if statu:
            return render(request, 'show.html', {'msg': '支付成功'})
        else:
            return render(request, 'show.html', {'msg': '支付失败'})
    else:
        return render(request, 'show.html', {'msg': '只支持GET请求，不支持其它请求'})
 
 
def check(request):
    if request.method=='POST':
        alipay=AliPay(appid="2021000119666477",
            app_notify_url='http://127.0.0.1:8000/alipay/check/',  # 支付宝会向这个地址发送post请求
            return_url='http://127.0.0.1:8000/show_msg/',  # 支付宝会向这个地址发送get请求
            app_private_key_path=r'C:/Users/24654/Desktop/project/frontend/django/pay/keys/private2048.txt',  # 应用私钥
            alipay_public_key_path=r'C:/Users/24654/Desktop/project/frontend/django/pay/keys/alipay_public.txt',  # 支付宝公钥
            debug=True,
        )
        body=request.body.decode('utf-8')  # 转成字符串
        post_data = parse_qs(body)  # 根据&符号分割
        post_dict = {}
        for k, v in post_data.items():
            post_dict[k] = v[0]
        sign = post_dict.pop('sign', None)
        status = alipay.verify(post_dict, sign)
        if status:  # 支付成功
            return HttpResponse('支付成功')
        else:
            return HttpResponse('支付失败')
    else:
        return HttpResponse('只支持POST请求')