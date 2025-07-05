## Integrating the Chatbot with Django Backend

You can use the chatbot logic in your Django backend by importing the `run_chatbot_with_json` function from `main.py`. This allows you to accept JSON input and return JSON output via an API endpoint.

### Example Django View

```
# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from main import run_chatbot_with_json

@csrf_exempt
def chatbot_view(request):
    if request.method == 'POST':
        try:
            input_json = json.loads(request.body)
            output = run_chatbot_with_json(input_json)
            return JsonResponse(output, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'POST request required'}, status=400)
```

### Add to urls.py

```
# urls.py
from django.urls import path
from .views import chatbot_view

urlpatterns = [
    path('chatbot/', chatbot_view, name='chatbot'),
]
```

### Usage
- Send a POST request with your JSON payload to `/chatbot/`.
- The response will be the chatbot's output as JSON.

This makes it easy to integrate the chatbot into any Django-based API or web application.
