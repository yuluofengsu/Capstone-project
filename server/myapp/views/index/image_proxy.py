from django.http import HttpResponse
import requests
from rest_framework.decorators import api_view, permission_classes, authentication_classes

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def image_proxy(request):
    url = request.GET.get('url')
    if not url:
        return HttpResponse(status=404)

    headers = {
        'Referer': 'https://book.douban.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, stream=True, timeout=10)
        return HttpResponse(
            response.content,
            content_type=response.headers.get('content-type', 'image/jpeg')
        )
    except Exception as e:
        print(f"Proxy Error: {e}")
        return HttpResponse(status=500)
