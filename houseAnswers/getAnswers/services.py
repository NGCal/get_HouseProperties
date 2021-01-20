from .models import Provider,Fields
from .exceptions import *
from .subservices import genericProviderCall
from .provider_subservices import *

class responseService():

    response = {
        "success":None,
        "data":None
    }

    providersClasses = {
        "houseDeets" : housedetailsProviderCall(),
        "allHouseInfo" : allhouseinfoProviderCall()
    }

    def getResponse(self,request,params):

        params = self.cleanParams(params)
        og_addr = params["address"]
        kPhrase = params["key_phrase"]
        try:
            fields = Fields.objects.values().filter(key_phrase=kPhrase)
            providers = list(Provider.objects.filter(id__in=fields.values("provider_id")).values("id","name","url").order_by("priority"))
        except:
            raise informationUnavailable()

        
        for provider in providers:
            for field in fields:
                if field["provider_id"] == provider["id"]:
                    params["property_name"] = field["name"]
             
            response = self.providersClasses[provider["name"]].getResponse(request,provider["url"],params)
            if response["success"] == True:
                break
        
        #print("this")
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


