from .models import Provider,Fields
from .exceptions import *
from .subservices import genericProviderCall
from .provider_subservices import *

class responseService():

    providersClasses = {
        "houseDeets" : housedetailsProviderCall(),
        "allHouseInfo" : allhouseinfoProviderCall(),
        "PropertyKnowledge":propertyknowledgeCall(),
        "zillow Library":zillowLibraryCall(),
        "Home Documentation":homedocumentationProviderCall()
    }

    def getResponse(self,request,params):

        params = self.cleanParams(params)
        og_addr = params["address"]
        kPhrase = params["key_phrase"]
        response = {
            "success":False
        }
        try:
            fields = Fields.objects.values().filter(key_phrase=kPhrase)
            providers = list(Provider.objects.filter(id__in=fields.values("provider_id")).values("id","name","url","auth_key").order_by("priority"))
            
        except:
            response = {"success": False, "data":informationUnavailable().default_detail, "code":informationUnavailable().status_code}
            return response 

        
        for provider in providers:
            for field in fields:
                if field["provider_id"] == provider["id"]:
                    params["property_name"] = field["name"]
            
            params["auth_key"] = provider["auth_key"]
            try:
                response = self.providersClasses[provider["name"]].getResponse(request,provider["url"],params)
            except:
                del(params["auth_key"])
                response = {"success": False, "data":providerclassUnavailable().default_detail, "code":providerclassUnavailable().status_code}
            
            if response["success"] == True:
                break
        
        
        params["address"] = og_addr
        params.pop("property_name")
        response["received_parameters"] = params
        
        return response
        
    
    def cleanParams(self,params):
        parameters = params.copy()
        for key in params.keys():
            if parameters[key] is None:
                parameters.pop(key)
        return parameters


