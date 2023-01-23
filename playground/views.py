from django.core.cache import cache
from django.core.mail import EmailMessage, BadHeaderError
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from templated_mail.mail import BaseEmailMessage
from .tasks import notify_customers
from rest_framework.views import APIView
import requests
import logging

# @cache_page(10 * 60)
# def say_hello(request):
#     # try:
#     #    message = BaseEmailMessage(
#     #        template_name='emails/hello.html',
#     #        context={'name': 'Mosh'}
#     #    )
#     #    message.send(['john@moshbuy.com'])
#     # except BadHeaderError:
#     #     pass

#     #notify_customers.delay('Hello')
#     # if cache.get('httpbin_result') is None:
#     #     response = request.get('httpbin.org/delay/2')
#     #     data = response.json()
#     #     cache.set(key, data)
#     # return render(request, 'hello.html', {'name': cache.get.key})
#     # 
#     #response = request.get('httpbin.org/delay/2')
#     # data = response.json()
#     #return render(request, 'hello.html', {'name': 'Leon'})

#     pass

logger = logging.getLogger(__name__) #playground.views


class HelloView(APIView):
    def get(self, request):
        try:
            logger.info('Calling httpbin')
            response = requests.get('https://httpbin.org/delay/2')
            logger.info('Recieved response')
            data = response.json()
        except request.ConnectionError:
            logger.critical('Httpbin is offile')
        return render(request, 'hello.html', {'name': 'Leon'})
