from django.shortcuts import render

# Create your views here.
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from lunch_menu.serializers import LoginSerializer


class MenuView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'menu.html'

    def get(self, request):
        return Response()

class LoginView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'Login.html'

    def get(self, request):
        return Response({'serializer': LoginSerializer()})
