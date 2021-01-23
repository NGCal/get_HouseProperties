from django.http import JsonResponse
from rest_framework.views import APIView
from .models import Provider,Fields
from rest_framework import viewsets, permissions
from .serializers import ProviderSerializer, FieldsSerializer,ResponseFormatter
from .services import *
from .exceptions import *
import requests

class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.all().order_by("priority")
    permission_classes = [
        permissions.IsAuthenticated
    ]

    serializer_class = ProviderSerializer


class FieldsViewSet(viewsets.ModelViewSet):
    queryset = Fields.objects.all()
    permission_classes = [
        permissions.IsAuthenticated
    ]

    serializer_class = FieldsSerializer

class ResponseViewSet(APIView):

    permission_classes = [permissions.IsAuthenticated]
     
    dto = {
            "success":None,
            "message":None
        }
  
    def get(self,request):
        
        params = {
            "key_phrase":request.query_params.get("key_phrase"),
            "address":request.query_params.get("address"),
            "zipcode":request.query_params.get("zipcode"),
            "unit":request.query_params.get("unit"),
            "state":request.query_params.get("state"),
            "city":request.query_params.get("city")

        }

        self.dto["request"] = params

        if not self._validateData(params):
            response = {
                "sucess":False,
                "data":parametersValidationFailed().default_detail,
                "received_parameters":params
            }
            return JsonResponse(response, status=parametersValidationFailed().status_code)
        
        response = responseService().getResponse(request,params)
        status = response.pop("code")

        if not response["success"]:
            return JsonResponse(response, status=status)

        return JsonResponse(response, status=status)
    
    def _validateData(self,params):
        if params["key_phrase"] is None or params["address"] is None or params["zipcode"] is None:
            return False
        return self._validKeyPhrase(params["key_phrase"]) and self._validZipcode(params["zipcode"])
    
    def _validKeyPhrase(self,kPhrase):
        return Fields.objects.values("name").distinct().filter(key_phrase=kPhrase).exists()

    def _validZipcode(self,zip):
        try:
            if len(zip) == 5 and zip.isnumeric():
                return True
        except:
                return False
        return False