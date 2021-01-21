from django.shortcuts import render
from .models import Provider,Fields
from .exceptions import *
from .subservices import genericProviderCall

import requests

class allhouseinfoProviderCall(genericProviderCall):
    
    url_cache_value = "AHI"
    urlFields={
        "paramsNames":{
            0:"addr",
            1:"zip",
            2:"unit",
            3:"state",
            4:"city"
        },
        "separator":"+"
    }
    info_cache_value =  url_cache_value +"_info"
    
   
class housedetailsProviderCall(genericProviderCall):
    url_cache_value = "h_details"
    urlFields={
        "paramsNames":{
            0:"address",
            1:"zip",
            2:"aptno",
            3:"state",
            4:"city"
        },
        "separator":"%20"
    }
    info_cache_value =  url_cache_value +"_info"
    auth_type="X-Api-Key"       

