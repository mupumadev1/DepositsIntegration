import json

import requests
from django.forms import forms, ModelForm

from .models import BankDetails

URL = "http://41.175.13.198:7664/api/json/commercials/zicb/banking"
API_KEY = "jVKRmqnoqsmoMXfhgaEjeXKctmtWdMpaPKINOfaiglVaWkVraFYngtYcfspiitZIcKjfZUwPTPHRNUrIgdiAyqpgplQFDJYwDCvzdUnnxalobZxzOCMWVKhVQZYiEfukQUCTeXOhKAIXTWSLszsFmuwZAGwTmpBUTjraYerObIOEAJbmEffhhxRgsglFAPPkKVCIzNkyzCaMxyIuNVdjHURqzqimwoPfkugKrgBNCTOZWYrUVyXKbGaeUayugjUFfbdboEOwipAQxQgTDrfpBGcSVELjqtrqTtlElIShCwUErSqvZVGneqWXEvuRwOqbVtJSbqZyReGCpRyXaivqoDSycUpDYnSymrcwQBDSTZRVIKALobWZxHQpVeTCfEhqDqfMydQqVjRpSaljyIRoIXDkhqhuEsZWVKZmgcbPxvTPSAuCoIvYfjdoFRZVemldnYZctyjTUTtmfiQQPRibOHwVEbstjZacCLHwgXPxtzRtdSypEjJcdkCUnfulNPtlSheLzNgtpAdQjWcuruYNtIgreCZELvbYxxYDlwWIngVmuzLTERviDjwYjeaeVnJxWecdIeLylpLKNHPobrXnJBltzgknhsqdKlKtoRqQobuvoCGVySOoTDPFhzjjeZGscCOvgKecixZdgXrRnghhsCuefYzgiCrHzmAaObiHIKPWxuFJkBaXxhNYOjSVyUmOFIxIkdeJSNDAIGldCMuUsExwPhoIrjcoACqLuUxvTlnGKpXrpCZhkbsUtUiCnLOtzZhjjFbrXxZSNPwOcCuLTCqzgxnBZrCcBEOevMIaRutODtwpJiRZGqpdQziPNyVwVdLxBwsZpZcVUAgTKjjaHHBFfFXtVrakSIosGVlQILvLiVgLgtFVXaEPwIdpCBuAJRpsRkoFUHKXVoiKFiLGsQaXxxiMCNdFcDVwrlYIiPxwKjbMptVUrPijJHbMYXHHppplksabPCparawfDYUwVIHVlgJZDceJOWfJdSWzUOfvrHUiFrAzrbSQmWrVEPhOpMmErnYBBfvxBPEWMeDkhzqTpbOCYHDfxGPJDiAVAMOcXKvOWIFzGQmZCaeMbRHXLNiANlbXYZprypSTIuJziqwUPctZL"
transaction_headers = {"Content-Type": "application/json; charset=utf-8", "authkey": API_KEY}


class BankDetailsForm(ModelForm):
    def __int__(self, *args, **kwargs):
        super(BankDetailsForm, *args, **kwargs)
        self.fields['account_no'].label = "Account Number"
        self.fields['vendor_id'].label = "Vendor ID"
        self.fields['account_name'].label = "Account Name"
        self.fields['vendor_mobile_number'].label = "Vendor Mobile Number"
        self.fields['vendor_email'].label = "Vendor Email"
        self.fields['sort_code'].label = "Sort Code"

    def clean_sort_code(self):
        try:
            sortcode = self.cleaned_data.get('sort_code')
            resp = requests.post(url=URL, headers=transaction_headers, json={"service": "BNK9901", "request": {}})
            resp = resp.json()
            found = False
            sortc = resp['response']['bankList']
            for sortc in sortc:
                if f'{sortcode}' == sortc['sortCode']:
                    found = True
                    return sortcode
            if not found:
                raise forms.ValidationError('Sort Code Entered is invalid.')
        except Exception as e:
           print(e)


    class Meta:
        model = BankDetails
        fields = ['account_no','account_name','vendor_id','vendor_email','vendor_mobile_number','sort_code']
