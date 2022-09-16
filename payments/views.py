from django.shortcuts import render, HttpResponse, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import hashlib
from .models import Show, Transaction
from datetime import datetime
from django.conf import settings

salt = settings.SALT
keyp = settings.KEYP
txnsalt = settings.TXNSALT
host = settings.HOST
# Create your views here.


def home(request):

    show_name = request.GET.get('show')
    show = get_object_or_404(Show, show_name=show_name)
    return render(request, 'payment.html', {'show': show})


@require_POST
def make_payment(request):
    info = request.POST
    show = get_object_or_404(Show, show_name=info['show_name'])
    txntime = str(datetime.now())

    txnid = hashlib.md5((show.show_name+info['email']+info['firstname']+txntime+txnsalt).encode()).hexdigest()
    print(txnid)
    txn = Transaction()
    txn.txn_id = txnid
    txn.txntime = txntime
    txn.email = info['email']
    txn.phone = info['phone']
    txn.amount = show.price
    txn.first_name = info['firstname']
    txn.showname = show.show_name
    txn.last_name = info['lastname']
    txn.save()
    # print(show.price)
    # print(info['firstname'])
    dict = {
        'key': keyp,
        'txnid': txnid,
        'amount': str(show.price),
        'productinfo': show.show_name,
        'firstname': info['firstname'],
        'email': info['email'],
        'lastname': info['lastname'],
        'surl': host + '/payment_temp/surl/',
        'furl': host + '/payment_temp/furl/',
        'phone': info['phone']
    }

    hash_str = ''

    for key in dict:
        hash_str = hash_str + dict[key]
        hash_str = hash_str + '|'
        if key == 'email':
            hash_str = hash_str + '||||||||||'
            break
    hash_str = hash_str + salt

    hash = hashlib.sha512(hash_str.encode()).hexdigest()

    dict['hash'] = hash

    return render(request, 'pay.html', {'details': dict})
    # return HttpResponse(dict['hash'])


@csrf_exempt
@require_POST
def surl(request):
    res = request.POST
    hash_str = salt +'|'+res['status']+'|||||||||||'+res['email']+'|'+res['firstname']+'|'+res['productinfo']+'|'+res['amount']+'|'+res['txnid']+'|'+keyp
    if (res['hash'] == hashlib.sha512(hash_str.encode()).hexdigest()) and (res['status'] == 'success'):
        txnmod = Transaction.objects.get(txn_id = res['txnid'])
        txnmod.txn_id_pu = res['mihpayid']
        txnmod.status = True
        txnmod.mode_err = res['mode']
        txnmod.save()
        return render(request, 'transaction.html', {'obj': txnmod})
    else:
        return HttpResponse('Malpractice')


@csrf_exempt
@require_POST
def furl(request):
    res = request.POST
    hash_str = salt +'|'+res['status']+'|||||||||||'+res['email']+'|'+res['firstname']+'|'+res['productinfo']+'|'+res['amount']+'|'+res['txnid']+'|'+keyp
    if (res['hash'] == hashlib.sha512(hash_str.encode()).hexdigest()):
        txnmod = Transaction.objects.get(txn_id = res['txnid'])
        txnmod.txn_id_pu = res['mihpayid']
        txnmod.mode_err = 'error:'+res['error']
        txnmod.save()
        return render(request, 'transaction.html', {'obj': txnmod})
    else:
        return HttpResponse('Malpractice')
