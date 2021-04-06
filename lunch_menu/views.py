from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from lunch_menu.serializers import LoginSerializer, MenuSerializer, ChoiceSerializer


class MenuView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'menu.html'

    def get(self, request):
        return Response({'menu_serializer': MenuSerializer(), "choice_serializer": ChoiceSerializer()})


class ChoiceView(CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    serializer_class = ChoiceSerializer
    template_name = 'choices.html'

    def get(self, request):
        return Response({"choice_serializer": ChoiceSerializer()})

    def post(self, request, *args, **kwargs):
        self.create(request, *args, **kwargs)
        return Response({"choice_serializer": ChoiceSerializer()})


class LoginView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'login.html'

    def get(self, request):
        return Response({'serializer': LoginSerializer()})
