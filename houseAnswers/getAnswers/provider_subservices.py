from django.shortcuts import render
from .models import Provider,Fields
from .exceptions import *
from .subservices import genericProviderCall

import requests

class allhouseinfoProviderCall(genericProviderCall):
    
    url_cache_value = "AHI"
    urlFields={
        "paramsNames":{
            "address":"addr",
            "zipcode":"zip",
            "unit":"unit",
            "state":"state",
            "city":"city"
        },
        "separator":"+"
    }
    info_cache_value =  url_cache_value +"_info"
    
   
class housedetailsProviderCall(genericProviderCall):
    url_cache_value = "h_details"
    urlFields={
        "paramsNames":{
            "address":"address",
            "zipcode":"zip",
            "unit":"aptno",
            "state":"state",
            "city":"city"
        },
        "separator":"%20"
    }
    info_cache_value =  url_cache_value +"_info"
    auth_type="X-Api-Key"

class homedocumentationProviderCall(genericProviderCall):
    url_cache_value = "hDoc_details"
    info_cache_value =  url_cache_value +"_info"

class zillowLibraryCall(genericProviderCall):
    url_cache_value = "z_library"
    info_cache_value =  url_cache_value +"_info"
    auth_type="X-Api-Key"

    def formatResponse(self,data):
        response = {}
        """
        if "result" not in data.keys():
            response["success"] = False
            response["data"] = data
            print(data)
            return response
        """
        try:
            if data["result"]["status"] != "OK":
                response["success"] = False
                response["data"] = data
                return response

            data = data["result"]["property"]
        except:
            response["success"] = False
            response["data"] = structureChangedAPI().default_detail
            response["code"] = structureChangedAPI().status_code
            print(data)
            return response
        
        data = self.getPropertyValue(data)

        if data == "Property not Found":
            response["success"] = False
            response["data"] = data
            response["code"] = 404
            return response
        
        response["success"] = True
        response["data"] = data
        response["code"] = 200
        return response
    
class propertyknowledgeCall(genericProviderCall):
    url_cache_value = "p_knowledge"
    info_cache_value =  url_cache_value +"_info"


    def formatResponse(self,data):
        response = {}
        """
        if "info" not in data.keys():
            response["success"] = False
            response["data"] = data
            return response
        """
        try:
            if data["info"]["requestinfo"]["status"] != "OK":
                response["success"] = False
                response["data"] = data
                return response

            data = data["info"]["property_details"]
        except:
            response["success"] = False
            response["data"] = structureChangedAPI().default_detail
            response["code"] = structureChangedAPI().status_code
            return response    
        
       
        data = self.getPropertyValue(data)

        if data == "Property not Found":
            response["success"] = False
            response["data"] = data
            response["code"] = 404
            return response
        
        response["success"] = True
        response["data"] = data
        response["code"] = 200
        return response

