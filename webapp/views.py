import datetime
import io
import json
import logger

from _decimal import Decimal
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import requests
from sqlalchemy import not_
from sqlalchemy.orm import class_mapper

from .forms import BankDetailsForm
from .helpers import *
from .myauthBackend import UserAuthBackend
from .services import *
from .models import ProcessedDeposits, BankDetails, Users, UserLoginHistory
import requests
import pandas as pd

URL = "http://41.175.13.198:7664/api/json/commercials/zicb/banking"
IFT_KEY = "wmdTRHHpCAqgpCMMBfQUGZzpvOaOWmIFuNElwQBeuyyeRfHlRadnHSbMWimMZfPFhKIQEEgFPjkeJgHRwbTErvAZRlLJrVNhqSQRknxXpZhlsdzAuTTZtPZHFJOsvWtIRreHzFjPSEkwmGNdsOCMYipktXBeMkYEoWwFobzrUJRVJXeBWBveZYqirlbVlcwRXDdRJSIoFUMtxjFcbjFvxEKlmVzdjIpGWrqegWDOZQMOqLwSXsdBYjhkvcbQERolchgYpZbrmYRSMUFIHfiSBESXyVIeUAcXAhIcQAAQjWOVoZhuURxJNKRFUNiSMLOnIDwxaesFAwJPuZHbbKeMDxXzRQWaGCoaqKVjZshMpHVcEcncAZeKiioptRnpLAvmGHlrAXxSkaHgpWaqitRvYGOWDDMIxzsccEHpOfwsAfyZpCJyPRcpwiuCUTRRyOspSpWvFVIrHZxnzSizXkkVZtlhPeSYBrxplbhoAFYAPmxaZkAsNjQphlcfwmaZKzWreSkBpbGKrCcllzDcyibtGnbSlqqFZGIWFpokiyKVmcUaHDitetRwNMdksycsCsGTTiNysYVbeqLPFuGPTdrzfsMZZRQkAHqmyuYOMxQeEvpXibFylxPaoeaTXVWAVozTfdSIuufLgoADbvtDTpvpDhMiMcmPIIICEyeHpjyLGGFwqhBeSkVvYuQLSnHnoMlMZwCKRXzCXVjkcxEYCYflOdImrjPlMYzRNQjaCaMhhpBJTWoRDpQGaIhIQcsVAyHMtYIlRwEhGpnXZTFxshsxyDTBHPxaSKoPuHejMLQYIXyiMLtPfFJfZXYNAXfDXstXEBIHgqvYZAlogYbMPVIkDCceNNuaxkrRTAtcZGESKsRuPGOrukdHkdGaAGsbTSAgLXZmCkowppFOWZjgIJPiySyeeQOIQOfmcEyPWpByRBUxGmCnuOFbmbXEUBuuROdJsCKhfuaGIavHBUBdUuuhwuwEUOXYYwGmTEXXmVXRZrJLsDruGoYpYmTAcciUWMssQQRDEPhhuCEAkUZlfYoNkqUadbgEEzvJTQTkVPbeFnsoCPWKBEYeAqiwYpunQaLiUBpTMEuLGicQRgNnLvxbvJbKLYTxr"
DDAC_KEY = "DdzDsZAhnpCBYdYIjTMGnwLkCdjUSqXKtPNBtnEggTpXMjVFPZRKplbvkxDcXkAdgZaaHMmZWfMvtixnOpjpgLTltGlBsnaUwfsoqXMaFNOudDUAJOCukUnnuEbAgLyqqkevkoOWcrSiUeXkTzHcmiNhoiIcTeTxwgUMvOUxPqXdFVXGjPRKRRRlOtaLibcMYOIPcIVgQwgNuLcbRAEzvIoFyHphPWZxIUmZLWQDLQdjjZNzfuwLyecspNCZKTjIPhbFbHKERezyxEBbUGMuLltbeyDVpxoAGtaWEHyrhpJxVkATMOEwuNHTNfKeioLNeHhwauJWjLnqeNlbrvZYLcYqAxIieOiuqFxKLOIhnFsoXtEZlJoYmUlrCSZPZpAzfGtOCjmHCksctYwepNVXCZEScYnbskmdqHWyZkSNgMzYceRkkbxnbzgmpSiUJpyEWjBNbNZiPbbENkwhKtHAVJKzPJpzrGvLWwPKGUdXkPpMMbZVlNZGeAOcQBLEnHiLSpfcVrpKoIUYBFKvhUNKVXeMmEmQUCpciEtAZwUdfPyKOheYdtQFXbklwppeFEeOVnqQBgHhTCZlNbETHSdSYLihxOjqDeBRsfVzrdTwiSTVvkSJxbBEuuRcbZCYJOOUtyTjcpNEVdKvHJirRLfoSOltxNQFTGMtCJTqnaeEZFSSIbHyjaDVeJyfHilqlpysiDEKRFawquymCzHTSckbQYrHNjdfoMXFUVYYTFExtEHkGjLZAXplCVDMRIJkxBOFqksPddOGfaUMQdEYUGjCNxVdjpYKPcSXDVJGhXRkyikoAiBiKOGipzSJowglSvjUQtqoqBUswPTUxsPTfOIUTpXIrdghCmSjFpKLKWndmuiXpawEjVYbwBDaVdqGoYqNrxfpjkYspZoJrNMpNGPBhlvQMJJtgajNhHyOHtUqhTEPwDaVVuYdWsBmLlWCeEBqpyHPnwkGHJzrDieaSqoYHnpXtosFCIATDeTSZepebGcNbMCAjmfThNvUVoOGXaYOIXCKsUCdqDnpMolNEZUWLJhHFTpahUmUXvvuxtxyepgyhJRjEhDsISFENzkUkFxyKptCdjPePLaLjnXPFweLBUMUIuyBl"
API_KEY = "jVKRmqnoqsmoMXfhgaEjeXKctmtWdMpaPKINOfaiglVaWkVraFYngtYcfspiitZIcKjfZUwPTPHRNUrIgdiAyqpgplQFDJYwDCvzdUnnxalobZxzOCMWVKhVQZYiEfukQUCTeXOhKAIXTWSLszsFmuwZAGwTmpBUTjraYerObIOEAJbmEffhhxRgsglFAPPkKVCIzNkyzCaMxyIuNVdjHURqzqimwoPfkugKrgBNCTOZWYrUVyXKbGaeUayugjUFfbdboEOwipAQxQgTDrfpBGcSVELjqtrqTtlElIShCwUErSqvZVGneqWXEvuRwOqbVtJSbqZyReGCpRyXaivqoDSycUpDYnSymrcwQBDSTZRVIKALobWZxHQpVeTCfEhqDqfMydQqVjRpSaljyIRoIXDkhqhuEsZWVKZmgcbPxvTPSAuCoIvYfjdoFRZVemldnYZctyjTUTtmfiQQPRibOHwVEbstjZacCLHwgXPxtzRtdSypEjJcdkCUnfulNPtlSheLzNgtpAdQjWcuruYNtIgreCZELvbYxxYDlwWIngVmuzLTERviDjwYjeaeVnJxWecdIeLylpLKNHPobrXnJBltzgknhsqdKlKtoRqQobuvoCGVySOoTDPFhzjjeZGscCOvgKecixZdgXrRnghhsCuefYzgiCrHzmAaObiHIKPWxuFJkBaXxhNYOjSVyUmOFIxIkdeJSNDAIGldCMuUsExwPhoIrjcoACqLuUxvTlnGKpXrpCZhkbsUtUiCnLOtzZhjjFbrXxZSNPwOcCuLTCqzgxnBZrCcBEOevMIaRutODtwpJiRZGqpdQziPNyVwVdLxBwsZpZcVUAgTKjjaHHBFfFXtVrakSIosGVlQILvLiVgLgtFVXaEPwIdpCBuAJRpsRkoFUHKXVoiKFiLGsQaXxxiMCNdFcDVwrlYIiPxwKjbMptVUrPijJHbMYXHHppplksabPCparawfDYUwVIHVlgJZDceJOWfJdSWzUOfvrHUiFrAzrbSQmWrVEPhOpMmErnYBBfvxBPEWMeDkhzqTpbOCYHDfxGPJDiAVAMOcXKvOWIFzGQmZCaeMbRHXLNiANlbXYZprypSTIuJziqwUPctZL"
INFO_KEY = "phVlVbCWHMgWxvBTxGnFwVLjnpelCuhYblZpelJuSRTXrPLQEKfEZDwxfTSBdmpcnVbzukyfEOnaVFNoOPJiSKKdpQqATODUxiiLJgaCmYXNdZsCXVshzZOURPxGvhSBrkxszwsnCbnYqDOiGYOLyRGrDEwPVxASspqFeGYcFDmDGovlqUDGgcQPKHRJMyWaQWbYzzCgOJETIdjEkmvxGnJPwgwnMsxMxQtKyoxLQskYSuSrwNkLCrvZYcqxovRhKFiwxXMRRpwVFNteydZBCwQSGJlWrseMEDKZlfNzlYFEESiAwyMRBghQlaipGkmRvxPcuWWxPSrIolqzzjTLhLIhRUxBbadHJXqoYEFSEsHrWjeGIqHvpgORtlDXYitqWaHJNrffnTryfYqYSvwXgtxTJPZnVbZzMxdtAKsKstOhzokNcsPxqhmSczYHdKTOksjRkBSkZlqHIPOCaWBGjsDAGsoPXqdrurcaOELRHgOcukddAOsRyUepOvwKPZieSwnemmlIKCPeRUtlsTFYJqSTztiQpFmiFHzOLQxwzezRTfvSADoiOzYCSRtANuoyyuKxQHmocYmcEmtbYpisnzJInfJCjFSdCwTIOzWtGQNTFZlPaWQTwVKyQqzoDXTiXEvOZknzdxAmzNARPHPfgVUzQEiCSFTXWiFGmWfowlsPrNUjNrGrRfXTxmsuSuKEUOfvSGmwJqBGDyderfRcGQNzaNSgVrXJOCAnvAWzerznYdxRfTFiGcwdJZqESiujfIAaazlaGxcoExDzsjMkYKJxsXroxVBCNiWFvqqVKFhtqaZJIVDnLxqtufAEWXnzCEPgYAxSJaoITXisyjcmvIqmSfGmVAlqDsBtieTQvbShqgzJylvRxoXpBRPnpRkXlsvmOWZuMauplDcZqAIsyHSymGELLXDYdmYnMPzEYLkkJaHmoyvGFSsPIQkZEnbVEmdaLmeIATnKEeeuvpUJRAhpppBMneuwJKRjtUluLKxdmsiJyobAqoMLIYUejitSIIjrgPAuBYEhhYvtMrQvcPeNXKnCHYIWmSUYWaeQkYRYfbEjSgGMpPDGmgNYOJWkGnGfodApdfAvVVcMqsjEeIWLEylxO"
transaction_headers = {"Content-Type": "application/json; charset=utf-8", "authkey": API_KEY}


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def UserLogin(request):
    user_backend = UserAuthBackend()
    if request.method == 'POST':
        username = request.POST["username"]
        cif = request.POST["cif"]
        password = request.POST["password"]
        user = user_backend.authenticate(request, username=username, password=None)
        if user is not None:
            login(request, user)
            json = {
                "service": "CORE_BANKING_LOGIN",
                "request": {
                    "username": f"{username}",
                    "cif": f"{cif}",
                    "password": f"{password}",
                    "channelType": "CORPORATE"
                }
            }

            resp = requests.post(url=URL, headers=transaction_headers, json=json)
            resp = resp.json()
            print(resp)
            if resp['response']['otpEnable']:
                json = {
                    "service": "CORE_BANKING_GENERATE_OTP",
                    "request": {}
                }
                response = requests.post(url=URL, headers=transaction_headers, json=json)
                response = response.json()
                print(response)
                if response['response']['otpEnable']:
                    log_hist = UserLoginHistory(username=username, ipaddress=get_ip_address(request),
                                                timestamp=datetime.datetime.now())
                    log_hist.save()
                    return redirect('webapp:enter-otp', )
            else:
                messages.error(request, message=resp['response']['message'])
                return redirect("webapp:login")
        else:
            messages.error(request, message="Username/Passowrd not registered")
            return redirect("webapp:login")
    else:
        return render(request, 'index.html')


def enterOTP(request):
    if request.method == 'POST':
        otp = request.POST["otp"]
        json = {
            "service": "CORE_BANKING_VERIFY_OTP",
            "request": {
                "otp": f"{otp}"
            }
        }
        cache.set(request.user.username, otp, timeout=600)  # set the OTP with a timeout of 300 seconds
        resp = requests.post(url=URL, headers=transaction_headers, json=json)
        resp = resp.json()
        print(resp)
        if resp['response']['message'] == "Success":
            if request.user.role == '001':
                return redirect('webapp:bank-details')
            elif request.user.role == '002':
                return redirect('webapp:homepage')
            else:
                messages.error(request, message="User Role Unknown")
                return redirect('webapp:login')
        else:
            messages.error(request, message='Login Failed.Invalid OTP')
            return redirect("webapp:login")

    return render(request, 'validate-otp.html')


def UserLogout(request):
    logout(request)
    return redirect('webapp:homepage')


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        # 👇️ if passed in object is instance of Decimal
        # convert it to a string
        if isinstance(obj, Decimal):
            return str(obj)
        # 👇️ otherwise use the default behavior
        return json.JSONEncoder.default(self, obj)


def get_search_results(request):
    """
    Get search results based on query parameters"""

    if request.method != 'GET':
        return JsonResponse({'message': 'Only GET requests are allowed'}, status=400)

    try:
        vendor_info = BankDetails.objects.values('vendor_id', 'sort_code',
                                                 'account_no',
                                                 'account_name').all()

        vendors = [vendor['vendor_id'] for vendor in vendor_info]

        # Dictionary containing field mapping parameters
        field_mapping_transactions = {
            'vendor_id': appym.IDVEND.like(f'%{request.GET.get("search_params")}%'),
            'date': appym.DATERMIT.like(f'%{request.GET.get("search_params")}%'),
            'amount': appym.AMTPAYM.like(f'%{request.GET.get("search_params")}%'),
            'invoice_id': appym.IDINVC.like(f'%{request.GET.get("search_params")}%'),
        }

        field_mapping_vendor = {
            'account_number': 'account_no__icontains',
            'sort_code': 'sort_code__icontains',
            'bank_name': 'bank_name__icontains',

        }

        search_params = request.GET.get('search_params')
        field_option = request.GET.get('filter_options')
        page_number = request.GET.get('page_number', 1)

        if field_option in field_mapping_transactions:
            transaction_info = ms_session.query(appym).filter(appym.IDVEND.in_(vendors),
                                                              field_mapping_transactions[field_option]).all()
            trans_infor_raw = []
            trans_info = []
            for transaction_info in transaction_info:
                transaction_info.IDVEND = transaction_info.IDVEND.strip()
                trans_infor_raw.append(transaction_info)
            for trans_inf in trans_infor_raw:
                transac_info = serialize_sqlalchemy_object(trans_inf)
                trans_info.append(transac_info)

            response_data = format_response_data(page_number, trans_info, vendor_info)
            return JsonResponse(response_data)

        elif field_option in field_mapping_vendor and search_params:
            vendor_info = BankDetails.objects.filter(**{field_mapping_vendor[field_option]: search_params}).values(
                'vendor_id', 'sort_code', 'account_no', 'account_name').all()
            vendor_ids = [vendor['vendor_id'] for vendor in vendor_info]
            trans_infor_raw = []
            trans_info = []
            transaction_info = ms_session.query(appym).filter(
                appym.IDVEND.in_(vendor_ids)).all()
            for transaction_in in transaction_info:
                transaction_in.IDVEND = transaction_in.IDVEND.strip()
                trans_infor_raw.append(transaction_in)
            for trans in trans_infor_raw:
                transaction_info = serialize_sqlalchemy_object(trans)
                trans_info.append(transaction_info)
            response_data = format_response_data(page_number, trans_info, vendor_info)

            return JsonResponse(response_data)

        else:
            response_data = {'transaction_info': [], 'vendor_info': [], 'number_of_pages': 1}
            return JsonResponse(response_data)

    except Exception as e:
        return JsonResponse({'message': f'An error occurred while processing your request {e}'}, status=500)


def format_response_data(page_number, transaction_info, vendor_info):
    """ Format Response data and return a dictionary containing the data"""
    if page_number is None:
        page_data, number_of_pages = paginate_data(transaction_info, 1)
        return {'transaction_info': list(page_data), 'vendor_info': list(vendor_info),
                'number_of_pages': number_of_pages}
    page_data, number_of_pages = paginate_data(transaction_info, int(page_number))

    return {'transaction_info': list(page_data), 'vendor_info': list(vendor_info), 'number_of_pages': number_of_pages}


def serialize_sqlalchemy_object(obj):
    # Get the class mapper for the object
    mapper = class_mapper(obj.__class__)
    # Get the columns from the mapper
    columns = [prop.key for prop in mapper.iterate_properties if hasattr(prop, "columns")]
    # Create a dictionary of the object's attributes
    data = {}
    for colmn in columns:
        data[colmn] = getattr(obj, colmn)
    # Serialize the dictionary as JSON
    return json.dumps(data, cls=DecimalEncoder)


def paginate_data(data, page_number, page_size=10):
    """ Paginate data and return page object and number of pages """
    paginator = CustomPaginator(data, page_size)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj, paginator.num_pages


def bankUploadViaForm(request):
    try:
        form = BankDetailsForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                if request.htmx:
                    return render(request, 'account-details.html', {'form': form})
                vendor = form.save(commit=False)
                sort_code = form.clean_sort_code()
                resp = requests.post(url=URL, headers=transaction_headers, json={"service": "BNK9901", "request": {}})
                resp = resp.json()
                if resp['operation_status'] == 'SUCCESS':
                    resp = resp['response']['bankList']
                    for resp in resp:
                        if f'{sort_code}' == resp['sortCode']:
                            bank_name = resp['bankName']
                            branch = resp['branchDesc']
                            vendor.bank_name = bank_name
                            vendor.branch = branch
                            vendor.save()
                            return redirect('webapp:bank-details')
                else:
                    return HttpResponse(f'Error saving bank details, Try again later', status=500)

        return render(request, 'account-details.html', {'form': form})
    except Exception as e:
        print(e)


def editBankUploadViaForm(request, acc_id):
    vendor = BankDetails.objects.filter(account_no=acc_id).first()
    form = BankDetailsForm(request.POST, instance=vendor)
    if request.method == 'POST':
        if form.is_valid():
            if request.htmx:
                return render(request, 'account-details.html', {'form': form})
            vendor = form.save(commit=False)
            sort_code = form.clean_sort_code()
            resp = requests.post(url=URL, headers=transaction_headers, json={"service": "BNK9901", "request": {}})
            resp = resp.json()
            if resp['operation_status'] == 'SUCCESS':
                resp = resp['response']['bankList']
                for resp in resp:
                    if f'{sort_code}' == resp['sortCode']:
                        bank_name = resp['bankName']
                        branch = resp['branchDesc']
                        vendor.bank_name = bank_name
                        vendor.branch = branch
                        vendor.save()
                        return redirect('webapp:bank-details')
            else:
                return HttpResponse('Error saving information, try again later')
        else:
            render(request, 'edit-vendor-bank.html',
                   {'form': BankDetailsForm(instance=vendor), 'acc_id': vendor.account_no})

    return render(request, 'edit-vendor-bank.html', {'form': BankDetailsForm(instance=vendor),
                                                     'acc_id': vendor.account_no})


@login_required(login_url='/')
def vendorBankDetails(request):
    data = BankDetails.objects.all().order_by()
    paginator = Paginator(data, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'bank_details': page_obj,
    }
    return render(request, 'vendor-bank-details.html', context)


def searchvendorBankDetails(request):
    if request.method == 'GET':
        vendor = request.GET['vendor']
        data = BankDetails.objects.filter(vendor_id=vendor).values('account_no', 'account_name', 'vendor_email',
                                                                   'vendor_id', 'vendor_mobile_number', 'sort_code'
                                                                   , 'branch', 'bank_name')

        return JsonResponse({'vendorinfo': list(data)}, status=200)


def bankUploadCSV(request):
    if request.method == 'POST':
        try:
            file = request.FILES['csvupload']
            df = pd.read_excel(file)
            df.fillna("", inplace=True)
            for index, row in df.iterrows():
                account_no = row['Account Number'],
                vendor_id = row['Vendor ID'],
                account_name = row['Account Name'],
                vendor_mobile_number = row['Vendor Mobile Number'],
                vendor_email = row['Vendor Email'],
                bank_name = ''
                branch = ''
                sort_code = row['Sort Code'],
                resp = requests.post(url=URL, headers=transaction_headers, json={"service": "BNK9901", "request": {}})
                resp = resp.json()
                if resp['operation_status'] == 'SUCCESS':
                    resp = resp['response']['bankList']
                    for resp in resp:
                        if f'{sort_code}' == resp['sortCode']:
                            bank_name = resp['bankName']
                            branch = resp['branchDesc']

                bank = BankDetails(account_no=account_no[0], vendor_id=vendor_id[0], account_name=account_name[0],
                                   vendor_mobile_number=vendor_mobile_number[0], vendor_email=vendor_email[0],
                                   bank_name=bank_name, sort_code=sort_code[0], branch=branch, )
                bank.save()
            return redirect('webapp:upload-bank-details-csv')
        except Exception as e:
            return HttpResponse(f'Error exporting data: {str(e)}', status=500)


def bankUploadCSVTemplate(request):
    try:
        b = io.BytesIO()
        df = pd.DataFrame(columns=[field.verbose_name for field in BankDetails._meta.get_fields()])
        writer = pd.ExcelWriter(b, engine='openpyxl')
        df.to_excel(writer, sheet_name='vendor bank details', index=False)
        df.drop('ID', axis=1)
        writer.save()
        response = HttpResponse(b.getvalue(),
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="Report1.xlsx"'
        return response
    except Exception as e:
        # Return an error response if an exception occurs
        return HttpResponse(f'Error exporting data: {str(e)}', status=500)


def forgotPassword(request):
    return render(request, 'forgot-password.html')


def search_invoice_id(request):
    """ Search by idinvc in Request list and return JSON resposne if found """
    if request.method == 'POST':
        if is_ajax(request):
            try:
                # Get invoice ids from request
                invoice_ids = json.loads(request.POST.get('invoice_ids[]'))
                transaction_info = []
                transaction_inf = ms_session.query(appym).filter(appym.IDINVC.in_(invoice_ids)).order_by(
                    appym.CNTBTCH.desc()).all()
                vendor_info = BankDetails.objects.values('vendor_id', 'sort_code', 'account_no', 'account_name').all()
                for t in transaction_inf:
                    t.IDVEND = t.IDVEND.strip()
                    transactions = serialize_sqlalchemy_object(t)
                    transaction_info.append(transactions)
                return JsonResponse(format_response_data(request.GET.get('page_number'),
                                                         transaction_info, vendor_info), safe=False)
            except Exception as e:
                print(e)
                message = 'Error: ' + str(e)
                return JsonResponse({'message': message}, safe=False)
        else:
            return JsonResponse({'message': 'Not an ajax request'}, safe=False)
    else:
        return JsonResponse({'message': 'Not a POST request'}, safe=False)


@login_required(login_url='/')
def homepage(request):
    # Get vendor info from the database
    vendor_info = BankDetails.objects.all()
    processed_dep = ProcessedDeposits.objects.all()
    vendors = [vendor.vendor_id for vendor in vendor_info]
    processed = [processed.invoiceid for processed in processed_dep]
    # Query payment transactions filtered by vendor ID
    payment_transactions_raw = ms_session.query(appym).filter(appym.IDVEND.in_(vendors),
                                                              not_(appym.IDINVC.in_(processed))).order_by(
        appym.CNTBTCH.desc()).all()
    # Strip whitespace from IDVEND field and add transactions to list
    payment_transactions = []
    for payment_trans in payment_transactions_raw:
        payment_trans.IDVEND = str(payment_trans.IDVEND).strip()
        payment_transactions.append(payment_trans)

    # Paginate the transaction list
    paginator = Paginator(payment_transactions, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Create context for the template
    context = {
        'transaction_info': page_obj,
        'vendor_info': vendor_info,
    }

    # Render the template with the contexta
    return render(request, 'homepage.html', context)


def post_transactions(request):
    """ Post transactions to API endpoint """
    if request.method == 'POST':
        invoice_ids = json.loads(request.POST.get('invoice_ids[]'))
        transaction_type = json.loads(request.POST.get('transaction_type'))
        transaction_info = ms_session.query(appym).filter(appym.IDINVC.in_(invoice_ids)).all()
        vendor_id = []
        vendor_ids = [transaction.IDVEND for transaction in transaction_info]
        for v in vendor_ids:
            v = v.strip()
            vendor_id.append(v)
        vendor_info = BankDetails.objects.filter(vendor_id__in=vendor_id).values().all()
        # Create a dictionary of vendor ids and their corresponding bsbno, accno, accname, idbank, amtpaym and codecurn

        vendor_dict = {}
        for vendor in vendor_info:
            vendor_dict[vendor['vendor_id']] = {'sort_code': vendor['sort_code'], 'account_no': vendor['account_no'],
                                                'account_name': vendor['account_name'],
                                                'vendor_mobile_number': vendor['vendor_mobile_number'],
                                                'vendor_email': vendor['vendor_email'], 'branch': vendor['branch']}

        for transaction in transaction_info:

            if transaction.IDVEND.strip() in vendor_dict:
                vendor_dict[transaction.IDVEND.strip()].update(
                    {'bank_name': transaction.IDBANK, 'amtpaym': str(transaction.AMTPAYM),
                     'codecurn': transaction.CODECURN, 'date': transaction.DATERMIT,
                     'transaction_type': transaction_type[transaction.IDINVC],
                     'invoice_id': transaction.IDINVC})

        for k, v in vendor_dict.items():
            trans_type = v['transaction_type']
            if trans_type == 'DDAC':
                response = postDDACTransaction(request, v)
                return JsonResponse(response, safe=False)
            elif trans_type == 'IFT':
                response = postFTTransaction(request, v)
                return JsonResponse({"resps": response[0], "stats": response[1]}, safe=False)
            elif trans_type == 'RTGS':
                response = postRTGSTransaction(request, v)
                return JsonResponse(response, safe=False)

            else:
                return JsonResponse({'message': 'Transaction Type Selected invalid'}, safe=False)
    else:
        return JsonResponse({'message': 'GET Request Not Allowed'}, status=400)


def transaction_history(request):
    data = ProcessedDeposits.objects.all().order_by('-timestamp')
    paginator = Paginator(data, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "transaction-history.html", {'transaction_info': page_obj})


def checkAccNumber(request):
    acc = request.GET.get('acc_no')
    data = {
        "service": "ZB0627",
        "request": {
            "accountNos": f"{acc}"
        }
    }
    response = requests.post(url=URL, headers={"Content-Type": "application/json; charset=utf-8", "authkey": INFO_KEY},
                             json=data)
    response = response.json()
    account_list = response['response']['accountList']
    return JsonResponse({'resp': list(account_list)})


def postDDACTransaction(request, transaction_dict):
    data = {
        "service": "BNK9900",
        "request": {
            "userName": "INFRATEL CORPORATION LIMITED",
            "customerId": "0036875",
            "ipAddress": "102.23.122.232",
            "srcAcc": "1010036875921",
            "destAcc": f"{transaction_dict['account_no']}",
            "amount": f"{transaction_dict['amtpaym']}",
            "destCurrency": "ZMW",
            "srcCurrency": "ZMW",
            "payCurrency": "ZMW",
            "transferTyp": "DDAC",
            "destBranch": f"{transaction_dict['branch']}",
            "srcBranch": "001",
            "bankName": f"{transaction_dict['bank_name']}",
            "sortCode": f"{transaction_dict['sort_code']}",
            "remarks": f"Invoice Payment from Infratel Cooperation Limited",
            "payDate": f"{transaction_dict['date']}",
            "beneName": f"{transaction_dict['account_name']}",
            "senderName": "INFRATEL CORPORATION LIMITED",
            "senderEmail": "",
            "sendermobileno": "211428700",
            "beneEmail": f"{transaction_dict['vendor_email']}",
            "beneMobileNo": f"{transaction_dict['vendor_mobile_number']}",
            "senderAddress1": "61 PROSPECT HILL LUSAKA",
            "senderAddress2": "Lusaka",
            "senderAddress3": "Zambia"
        }
    }
    print(data)
    response = requests.post(url=URL,
                             headers={"Content-Type": "application/json; charset=utf-8", "authkey": DDAC_KEY},
                             json=data)

    resp_json = response.json()
    print(resp_json)
    if resp_json['operation_status'] == 'SUCCESS':
        processed = ProcessedDeposits(vendorid=transaction_dict['account_name'],
                                      invoiceid=transaction_dict['invoice_id'], status=1,
                                      transaction_type="DDAC", processed_by=request.user.username)
        processed.save()
        return HttpResponse("success")
    else:
        return HttpResponse("failed")


def postRTGSTransaction(request, transaction_dict):
    data = {
        "service": "BNK9900",
        "request": {
            "userName": "INFRATEL CORPORATION LIMITED",
            "customerId": "0036875",
            "ipAddress": "102.23.122.232",
            "destAcc": f"{transaction_dict['account_no']}",
            "amount": f"{transaction_dict['amtpaym']}",
            "destCurrency": "ZMW",
            "srcCurrency": "ZMW",
            "payCurrency": "ZMW",
            "transferTyp": "RTGS",
            "destBranch": f"{transaction_dict['branch']}",
            "srcBranch": "001",
            "bankName": f"{transaction_dict['bank_name']}",
            "sortCode": f"{transaction_dict['sort_code']}",
            "remarks": f"Invoice Payment from Infratel Cooperation Limited",
            "payDate": f"{transaction_dict['date']}",
            "beneName": f"{transaction_dict['account_name']}",
            "senderName": "INFRATEL CORPORATION LIMITED",
            "senderEmail": "",
            "sendermobileno": "211428700",
            "beneEmail": f"{transaction_dict['vendor_email']}",
            "beneMobileNo": f"{transaction_dict['vendor_mobile_number']}",
            "senderAddress1": "61 PROSPECT HILL LUSAKA",
            "senderAddress2": "Lusaka",
            "senderAddress3": "Zambia"
        }
    }
    print(data)

    response = requests.post(url=URL,
                             headers={"Content-Type": "application/json; charset=utf-8", "authkey": API_KEY},
                             json=data)

    resp_json = response.json()
    print(resp_json)
    if resp_json["operation_status"] == "SUCCESS":
        processed = ProcessedDeposits(vendorid=transaction_dict['account_name'],
                                      invoiceid=transaction_dict['invoice_id'], status=1,
                                      transaction_type="RTGS", processed_by=request.user.username)
        processed.save()
        JsonResponse({'message': 'Transaction(s) Recieved and Posted'}, safe=False)
    else:
        JsonResponse({'message': 'Transaction(s) Posting failed '}, safe=False)


def postFTTransaction(request, transaction_dict):
    json = {
        "service": "CORE_BANKING_FT",
        "request": {
            "ftList": [
                {
                    "amount": f"{transaction_dict['amtpaym']}",
                    "remarks": "Invoice Payment from Infratel Cooperation Limited",
                    "bankCode": "0000",
                    "bankName": "",
                    "benName": "",
                    "beneEmail": "",
                    "benePhoneno": "",
                    "branchCode": "001",
                    "destinationAccount": "1010035376132",  # f"{transaction_dict['account_no']}",
                    "destinationBranch": "",
                    "destinationCurrency": "",
                    "nationalClearingCode": "00000",
                    "sourceAccount": "1010036875921",
                    "sourceBranch": "001",
                    "srcCurrency": "ZMW",
                    "swiftCode": "0000",
                    "transferTyp": "IAT",
                    "beneTransfer": False
                }
            ]
        }
    }
    response = requests.post(url=URL, headers={"Content-Type": "application/json; charset=utf-8", "authkey": IFT_KEY},
                             json=json)
    resp_json = response.json()
    response = resp_json['response']
    if 'status' in response:
        return response['message'], response['status']
    else:
        key = resp_json["response"]["randomKey"]
        req = resp_json["request"]["ftList"]
        otp = cache.get(request.user.username)
        ft_confirm_json = {
            "service": "CORE_BANKING_FT_CONFIRM",
            "request": {
                "bulkTransfer": False,
                "randomKey": f"{key}",
                "otp": f"{otp}",
                "ftList": req
            }
        }
    resp = requests.post(url=URL, headers={"Content-Type": "application/json; charset=utf-8", "authkey": IFT_KEY},
                         json=ft_confirm_json)
    ft_resp_json = resp.json()
    print(ft_resp_json)
    if ft_resp_json['response']['message'] == "Fund Transfer initiated successfully":
        processed = ProcessedDeposits(vendorid=transaction_dict['account_name'],
                                      invoiceid=transaction_dict['invoice_id'], status=1,
                                      transaction_type="IFT", processed_by=request.user.username)
        processed.save()
        return ft_resp_json['response']['message'], 200
    else:
        return ft_resp_json['response']['message'], 500
