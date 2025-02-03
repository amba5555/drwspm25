import logging
import requests

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render

GOOGLE_SCRIPT_URL = 'https://script.googleusercontent.com/macros/echo?user_content_key=ogFERX1HH3F6EIzu_JIdXg28akMlQWg-TMBPrBgQtyDQ76kx1NCyIAT7dlxT3DxCbtCF0cWn3tv2yd6ZWR6ksgWlpkFR2-r3m5_BxDlH2jW0nuo2oDemN9CCS2h10ox_1xSncGQajx_ryfhECjZEnJY3Gg1SgdkFV1dxD6V36nin0xcZKRaadKAWz44YP5FD9GjcVZRQccOn_xDcPFEweWFjVAWOBZRRoxM84HFoUQrouxKkSt0DNw&lib=MwMPtSVnqjpV6XcwrtYJ1uh9RNx0BfzFA'

def index(request):  # <-- This function must exist
    return render(request, 'pm25monitor/index.html')

logger = logging.getLogger(__name__)


def get_pm25(request):
    try:
        response = requests.get(GOOGLE_SCRIPT_URL, timeout=15)
        data = response.json()

        if data.get('status') == 'error':
            return JsonResponse({'error': data.get('error')}, status=500)
            
        return JsonResponse({
            'pm25': data.get('pm25', 'N/A'),
            'timestamp': data.get('timestamp'),
            'avg_pm25': data.get('avg_pm25', 'N/A')
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
