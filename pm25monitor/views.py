import logging
import requests

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render

GOOGLE_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbwzdVmaCSMkEcwmrA70U4IFKKY2GX01OPJIUXs_Eye-zkG-1UYbCglbk8LmCXIyPAneEg/exec'

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
            'date': data.get('date', 'N/A'),
            'time': data.get('time', 'N/A'),
            'avg_pm25': data.get('avg_pm25', 'N/A')
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
