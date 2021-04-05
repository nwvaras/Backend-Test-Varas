from django.shortcuts import render

# Create your views here.
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView


class MenuView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'menu.html'

    def get(self, request):
        return Response()