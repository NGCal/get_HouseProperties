from django.test import TestCase
from .models import Provider,Fields
from django.utils import timezone
from tastypie.test import ResourceTestCaseMixin
from .api import *
from .services import responseService
from .subservices import *
from .serializers import *
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

#models Test
class providerandfieldsTest(TestCase):
    
    #Provider Tests
    def create_provider1(self,name="PropertyKnowledge",url="https://propertyknowled.com/api/houseinfo/details",priority="2"):
        return Provider.objects.create(name=name,url=url,priority=priority,created_at=timezone.now())
    def create_provider2(self,name="zillow Library",url="https://zillow.com/api/library/properties/info",priority="1"):
        return Provider.objects.create(name=name,url=url,priority=priority,created_at=timezone.now())
    
    def test_providerA_creation(self):
        providerA = self.create_provider1()

        self.assertTrue(isinstance(providerA,Provider))
        self.assertEqual(providerA.__str__(),providerA.name)
    def test_providerB_creation(self):
        providerB = self.create_provider2()

        self.assertTrue(isinstance(providerB,Provider))
        self.assertEqual(providerB.__str__(),providerB.name)

    #Fields Test
    
    def create_field1(self,name="sewerSystem",key_phrase="sewer_system"):
        provider= self.create_provider1()
        return Fields.objects.create(name=name,key_phrase=key_phrase,provider=provider)
    
    def create_field2(self,name="sewerSys",key_phrase="sewer_system",provider="5"):
        provider= self.create_provider2()
        return Fields.objects.create(name=name,key_phrase=key_phrase,provider=provider)
    
    def create_field3(self,name="constructionStyle",key_phrase="style",provider="4"):
        provider= self.create_provider1()
        return Fields.objects.create(name=name,key_phrase=key_phrase,provider=provider)
    
    def create_field4(self,name="buildStyle",key_phrase="style",provider="5"):
        provider= self.create_provider2()
        return Fields.objects.create(name=name,key_phrase=key_phrase,provider=provider)
    
    def create_field5(self,name="garage",key_phrase="garage_type_parking",provider="5"):
        provider= self.create_provider2()
        return Fields.objects.create(name=name,key_phrase=key_phrase,provider=provider)

    def test_field1_creation(self):
        field = self.create_field1()

        self.assertTrue(isinstance(field,Fields))
        self.assertEqual(field.__str__(),field.name)
    
    def test_field2_creation(self):
        field = self.create_field2()

        self.assertTrue(isinstance(field,Fields))
        self.assertEqual(field.__str__(),field.name)
    
    def test_field3_creation(self):
        field = self.create_field3()

        self.assertTrue(isinstance(field,Fields))
        self.assertEqual(field.__str__(),field.name)
    
    def test_field4_creation(self):
        field = self.create_field4()

        self.assertTrue(isinstance(field,Fields))
        self.assertEqual(field.__str__(),field.name)

    def test_field5_creation(self):
        field = self.create_field5()

        self.assertTrue(isinstance(field,Fields))
        self.assertEqual(field.__str__(),field.name)
    

#custom api test
class getResponseApi(ResourceTestCaseMixin,TestCase):
    """
    docstring
    """
    def test_get_api_json(self):
        resp = self.api_client.get("/api/answers?key_phrase=sewer&address=butts street&zipcode=00765", format="json")
        self.assertValidJSONResponse(resp)
