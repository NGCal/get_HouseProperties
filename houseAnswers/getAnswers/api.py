from django.http import JsonResponse
from rest_framework.views import APIView
from .models import Provider,Fields
from rest_framework import viewsets, permissions
from .serializers import ProviderSerializer, FieldsSerializer,ResponseFormatter
from .services import *
import requests

class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.all().order_by("priority")
    permission_classes = [
        permissions.AllowAny
    ]

    serializer_class = ProviderSerializer


class FieldsViewSet(viewsets.ModelViewSet):
    queryset = Fields.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]

    serializer_class = FieldsSerializer

class ResponseViewSet(APIView):
     
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
            self.dto["success"] = False
            self.dto["message"] = "Parameters validation failed or requested key_phrase is not available"
            
            data = ResponseFormatter(self.dto).data
            return JsonResponse(data, status=400)
        
        response = responseService().getResponse(request,params)

        if not response["success"]:
            return JsonResponse(response, status=404)

        return JsonResponse(response, status=200)
    
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