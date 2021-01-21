from django.shortcuts import render
from .models import Provider,Fields
from .exceptions import *

import requests

class genericProviderCall():

    """
    This class purpose is to serve as a template for any new provider class
    These are the variables/methods that always have to change:
        url_cache_value : used to save the url of a provider on memory when the query is about the last received address
        info_cache_value : used to save the response of a same address to the same provider on memory
    
    These are the most frequently changed variables/methods:
        formatResponse(self,data): used to format the data send by the provider
        getPropertyValue(self,data): used to obtain the requested field
        auth_type: used to set the authentication type on the request
    
    These are the usually changed variables/methods:
        urlFields["paramsNames"]: contains the names of the parameters that have to be send to the provider 
        IN THE ORDER that they have to be written

        urlFields["separator"]: contains the replacement of " " for the address field

        NOTE: if any of those fields has to be change the entire urlFields dcitionar has to be declare

    
    """

    urlFields={
        "paramsNames":{
            0:"address",
            1:"zipcode",
            2:"unit",
            3:"state",
            4:"city"
        },
        "separator":"%20"
    }

    url_cache_value = "house_provider"
    info_cache_value = url_cache_value +"_info"
    auth_type="Authentication"

    def getResponse(self,request,url,params):
        provider_is_cached = (self.url_cache_value in request.session)
        info_is_cached = (self.info_cache_value in request.session)

        auth = params.pop("auth_key")
        
        self.urlFields["paramsValues"] = params
        f_url = self.formatURL(url)
        print(f_url)

        if (provider_is_cached and f_url != request.session[self.url_cache_value]) or not provider_is_cached or not info_is_cached:
            try:
                request.session[self.url_cache_value] = f_url            
                response = requests.get(f_url,headers={self.auth_type:auth})
                request.session[self.info_cache_value] = response.json()
            except:
                response = {"success": False, "data": f_url +" "+providerUnavailable().default_detail}
                return response 
        
        response = self.formatResponse(request.session[self.info_cache_value])


        return response

        
    def formatResponse(self,data):
        response = {}
        if "property/details" not in data.keys():
            response["success"] = False
            response["data"] = data
            print(data)
            return response
        
        if data["property/details"]["api_code_description"] != "ok":
            response["success"] = False
            response["data"] = data
            return response

        data = data["property/details"]["result"]["property"]
        data = self.getPropertyValue(data)

        if data == "Property not Found":
            response["success"] = False
            response["data"] = data
            return response
        
        response["success"] = True
        response["data"] = data
        return response
        

    def getPropertyValue(self,data):
        field_name = self.urlFields["paramsValues"]["property_name"]
        key_phrase = self.urlFields["paramsValues"]["key_phrase"]

        if field_name not in data.keys() or data[field_name] is None or str(data[field_name]).strip().lower() == "null" or str(data[field_name]).strip() == "":
            return "Property not Found"
        data = {
            key_phrase:data[field_name]
        }

        return data
    
    def formatURL(self,url):
        try:
            paramsvalues = self.urlFields["paramsValues"]
            paramsnames = self.urlFields["paramsNames"]

            paramsvalues["address"]= self.replaceSpaces(paramsvalues["address"])
            f_url = url +"?"
            pos = 0

            for key in paramsvalues.keys():
                if key == "key_phrase" or key == "property_name":
                    continue
                f_url = f_url + paramsnames[pos] + "=" + paramsvalues[key] +"&"
                pos = pos + 1
        
        except:
            return "Failed to build URL"
        return f_url[:-1]
    
    def replaceSpaces(self,adr):
        adr = adr.strip()
        adr = adr.replace(" ",self.urlFields["separator"])
        return adr

