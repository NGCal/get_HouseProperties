from django.test import TestCase
from .models import Provider,Fields
from django.utils import timezone
from .api import *
from .services import responseService
from .subservices import *
from .serializers import *
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

#custom api test
class getResponseApi(APITestCase):
    """
    docstring
    """
    def test_successfulResponse_string(self):

        """
        Expected Response:
            Status code : 200
            Format: {
                'success': True, 
                'data': 
                    {
                        'style': 'parisian'
                        }, '
                received_parameters': 
                    {
                        'key_phrase': 'style', 
                        'address': '123 home street', 
                        'zipcode': '07065'
                        }
                    }
        """
        
        user = User.objects.create_user(username="test",password="testpassword")
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url = "%s?key_phrase=style&address=123 home street&zipcode=07065"%reverse('answers')
        self._populateProvandF()
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(),{'success': True, 'data': {'style': 'parisian'}, 'received_parameters': {'key_phrase': 'style', 'address': '123 home street', 'zipcode': '07065'}})

    def test_successfulResponse_boolean(self):

        """
        Expected Response:
            Status code : 200
            Format: {
                'success': True, 
                'data': {
                    'pool': True
                    }, 
                'received_parameters': {
                    'key_phrase': 'pool', 
                    'address': '123 home street', 
                    'zipcode': '07065'
                    }
                }
        """
        
        user = User.objects.create_user(username="test",password="testpassword")
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url = "%s?key_phrase=pool&address=123 home street&zipcode=07065"%reverse('answers')
        self._populateProvandF()
        
        response = self.client.get(url)
       
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(),{'success': True, 'data': {'pool': True}, 'received_parameters': {'key_phrase': 'pool', 'address': '123 home street', 'zipcode': '07065'}})

    def test_successfulResponse_numeric(self):

        """
        Expected Response:
            Status code : 200
            {
                'success': True, 
                'data': {
                    'number_of_bedrooms': 4
                    }, 
                'received_parameters': {
                    'key_phrase': 'number_of_bedrooms', 
                    'address': '10455 Yukatan Avenue', 
                    'zipcode': '80225', 
                    'city': 'Amazing'
                    }
            }
        """
        
        user = User.objects.create_user(username="test",password="testpassword")
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url = "%s?key_phrase=number_of_bedrooms&address=10455 Yukatan Avenue&zipcode=80225&city=Amazing"%reverse('answers')
        self._populateProvandF()
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(),{'success': True, 'data': {'number_of_bedrooms': 4}, 'received_parameters': {'key_phrase': 'number_of_bedrooms', 'address': '10455 Yukatan Avenue', 'zipcode': '80225', 'city': 'Amazing'}})
    

    def test_nonexitent_field_onProviderAPI(self):

        """
        Expected Response:
            Status code : 404
            {
                'success': False, 
                'data': 'Property not Found', 
                'received_parameters': {
                    'key_phrase': 'full_bath_count', 
                    'address': '10455 Yukatan Avenue', 
                    'zipcode': '80225', 
                    'city': 'Amazing'
                    }
            }
        """
        
        user = User.objects.create_user(username="test",password="testpassword")
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url = "%s?key_phrase=full_bath_count&address=10455 Yukatan Avenue&zipcode=80225&city=Amazing"%reverse('answers')
        self._populateProvandF()
        
        response = self.client.get(url)
       
        self.assertEqual(response.status_code,404)
        self.assertEqual(response.json(),{'success': False, 'data': 'Property not Found', 'received_parameters': {'key_phrase': 'full_bath_count', 'address': '10455 Yukatan Avenue', 'zipcode': '80225', 'city': 'Amazing'}})
    
    def test_keyParameter_notSend_endpoint(self):

        """
        The required parameters are:
            key_phrase:Property required to answer the question
            address:Street number and name of house/building or appartment
            zipcode:zipcode of the city of the house/building or appartment
        
        Expected Response1:
            Status code : 400
            {
                'sucess': False, 
                'data': 'Parameters validation failed or requested key_phrase is not available', 
                'received_parameters': {
                    'key_phrase': None, 
                    'address': '10455 Yukatan Avenue', 
                    'zipcode': '80225', 
                    'unit': None, 
                    'state': None, 
                    'city': None
                    }
            }
        Expected Response2:
            Status code : 400
            {
                'sucess': False, 
                'data': 'Parameters validation failed or requested key_phrase is not available', 
                'received_parameters': {
                    'key_phrase': sewer, 
                    'address': None, 
                    'zipcode': '80225', 
                    'unit': None, 
                    'state': None, 
                    'city': None
                    }
            }
        
        Expected Response3:
            Status code : 400
            {
                'sucess': False, 
                'data': 'Parameters validation failed or requested key_phrase is not available', 
                'received_parameters': {
                    'key_phrase': sewer, 
                    'address': '10455 Yukatan Avenue', 
                    'zipcode': None, 
                    'unit': None, 
                    'state': None, 
                    'city': None
                    }
            }
        """
        
        user = User.objects.create_user(username="test",password="testpassword")
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url = "%s?address=10455 Yukatan Avenue&zipcode=80225"%reverse('answers')
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json(),{'sucess': False, 'data': 'Parameters validation failed or requested key_phrase is not available', 'received_parameters': {'key_phrase': None, 'address': '10455 Yukatan Avenue', 'zipcode': '80225', 'unit': None, 'state': None, 'city': None}})

        url = "%s?key_phrase=sewer&zipcode=80225"%reverse('answers')
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json(),{'sucess': False, 'data': 'Parameters validation failed or requested key_phrase is not available', 'received_parameters': {'key_phrase': 'sewer', 'address': None, 'zipcode': '80225', 'unit': None, 'state': None, 'city': None}})

        url = "%s?key_phrase=sewer&address=10455 Yukatan Avenue"%reverse('answers')
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json(),{'sucess': False, 'data': 'Parameters validation failed or requested key_phrase is not available', 'received_parameters': {'key_phrase': 'sewer', 'address': '10455 Yukatan Avenue', 'zipcode': None, 'unit': None, 'state': None, 'city': None}})

    def test_invalidParameter_Send_toendpoint(self):

        """
        An invalid parameter would be:
            key_phrase:Not exisyent
            address:non alphanumeric
            zipcode:non alphanumeric or numeric with more or less than five digits
        
        Expected Response1:
            Status code : 400
            {
                'sucess': False, 
                'data': 'Parameters validation failed or requested key_phrase is not available', 
                'received_parameters': {
                    'key_phrase': sewer_system, 
                    'address': '10455 Yukatan Avenue', 
                    'zipcode': '80225', 
                    'unit': None, 
                    'state': None, 
                    'city': None
                    }
            }
        Expected Response2:
            Status code : 400
            {
                'sucess': False, 
                'data': 'Parameters validation failed or requested key_phrase is not available', 
                'received_parameters': {
                    'key_phrase': sewer, 
                    'address': 10455 (00l $tr33!, 
                    'zipcode': '80225', 
                    'unit': None, 
                    'state': None, 
                    'city': None
                    }
            }
        
        Expected Response3:
            Status code : 400
            {
                'sucess': False, 
                'data': 'Parameters validation failed or requested key_phrase is not available', 
                'received_parameters': {
                    'key_phrase': sewer, 
                    'address': '10455 Yukatan Avenue', 
                    'zipcode': 802@25, 
                    'unit': None, 
                    'state': None, 
                    'city': None
                    }
            }
        """
        
        user = User.objects.create_user(username="test",password="testpassword")
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url = "%s?key_phrase=sewer_system&address=10455 Yukatan Avenue&zipcode=80225"%reverse('answers')
        
        response = self.client.get(url)
       
        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json(),{'sucess': False, 'data': 'Parameters validation failed or requested key_phrase is not available', 'received_parameters': {'key_phrase': 'sewer_system', 'address': '10455 Yukatan Avenue', 'zipcode': '80225', 'unit': None, 'state': None, 'city': None}})

        url = "%s?key_phrase=sewer&address=10455 (00l $tr33!&zipcode=80225"%reverse('answers')
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json(),{'sucess': False, 'data': 'Parameters validation failed or requested key_phrase is not available', 'received_parameters': {'key_phrase': 'sewer', 'address': '10455 (00l $tr33!', 'zipcode': '80225', 'unit': None, 'state': None, 'city': None}})

        url = "%s?key_phrase=sewer&address=10455 Yukatan Avenue&zipcode=802@25"%reverse('answers')
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json(),{'sucess': False, 'data': 'Parameters validation failed or requested key_phrase is not available', 'received_parameters': {'key_phrase': 'sewer', 'address': '10455 Yukatan Avenue', 'zipcode': '802@25', 'unit': None, 'state': None, 'city': None}})


    def test_notFound_ProviderClass(self):

        """
        Expected Response:
            Status code : 422
            {
                'success': False, 
                'data': 'Provider class not available', 
                'received_parameters': {
                    'key_phrase': 'sewer', 
                    'address': '10455 Yukatan Avenue', 
                    'zipcode': '80225', 
                    'city': 'Amazing'
                    }
            }
        """
        
        user = User.objects.create_user(username="test",password="testpassword")
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url = "%s?key_phrase=sewer&address=10455 Yukatan Avenue&zipcode=80225&city=Amazing"%reverse('answers')
       
        provider = Provider.objects.create(name="Good House Information",url="https://fd34f8e2-6052-483a-9b8e-f7ecdffe3711.mock.pstmn.io/home/details",priority="1",auth_key="PMAK-6009c2980e728d00379f8a45-e79c6092ce3471ee4624089615bf406923")
        Fields.objects.create(name="sewer",key_phrase="sewer",provider=provider)
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code,422)
        self.assertEqual(response.json(),{'success': False, 'data': 'Provider class not available', 'received_parameters': {'key_phrase': 'sewer', 'address': '10455 Yukatan Avenue', 'zipcode': '80225', 'city': 'Amazing'}})

    
    def test_unreachableURL(self):

        """
        Expected Response:
            {
                'success': False, 
                'data': 'https://goodhouseinfo.com/api/house/info?address=10455%20Yukatan%20Avenue&zipcode=80225&city=Amazing Provider temporarily unavailable, try again later.', 
                'received_parameters': {
                    'key_phrase': 'sewer', 
                    'address': '10455 Yukatan Avenue', 
                    'zipcode': '80225', 
                    'city': 'Amazing'
                        }
                }
        """
        
        user = User.objects.create_user(username="test",password="testpassword")
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url = "%s?key_phrase=sewer&address=10455 Yukatan Avenue&zipcode=80225&city=Amazing"%reverse('answers')
       
        provider = Provider.objects.create(name="zillow Library",url="https://goodhouseinfo.com/api/house/info",priority="1")
        Fields.objects.create(name="sewer",key_phrase="sewer",provider=provider)
        
        response = self.client.get(url)
       
        self.assertEqual(response.status_code,503)
        self.assertEqual(response.json(),{'success': False, 'data': 'https://goodhouseinfo.com/api/house/info?address=10455%20Yukatan%20Avenue&zipcode=80225&city=Amazing Provider temporarily unavailable, try again later.', 'received_parameters': {'key_phrase': 'sewer', 'address': '10455 Yukatan Avenue', 'zipcode': '80225', 'city': 'Amazing'}})

    def test_responseStructureChange(self):

        """
        Expected Response:
           {
               'success': False, 
               'data': 'The structure of the information sent by the provider changed', 
               'received_parameters': {
                   'key_phrase': 'sewer', 
                   'address': '10455 Yukatan Avenue', 'zipcode': '80225', 'city': 'Amazing'}}
        """
        
        user = User.objects.create_user(username="test",password="testpassword")
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url = "%s?key_phrase=sewer&address=10455 Yukatan Avenue&zipcode=80225&city=Amazing"%reverse('answers')
       
        provider = Provider.objects.create(name="Home Documentation",url="https://26dba07c-dfe2-40c0-90bd-3b2c789f1600.mock.pstmn.io/location/house/info",priority="1")
        Fields.objects.create(name="sewer",key_phrase="sewer",provider=provider)
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code,422)
        self.assertEqual(response.json(),{'success': False, 'data': 'The structure of the information sent by the provider changed', 'received_parameters': {'key_phrase': 'sewer', 'address': '10455 Yukatan Avenue', 'zipcode': '80225', 'city': 'Amazing'}})

    
    
    def _populateProvandF(self):
        p1 = Provider.objects.create(name="PropertyKnowledge",url="https://26dba07c-dfe2-40c0-90bd-3b2c789f1600.mock.pstmn.io/location/house/info",priority="2")
        p2 = Provider.objects.create(name="zillow Library",url="https://fd34f8e2-6052-483a-9b8e-f7ecdffe3711.mock.pstmn.io/home/details",priority="1")

        Fields.objects.create(name="sewerSystem",key_phrase="sewer",provider=p1)
        Fields.objects.create(name="sewerSys",key_phrase="sewer",provider=p2)
        Fields.objects.create(name="constructionStyle",key_phrase="style",provider=p1)
        Fields.objects.create(name="buildStyle",key_phrase="style",provider=p2)
        Fields.objects.create(name="hasPool",key_phrase="pool",provider=p2)
        Fields.objects.create(name="no_of_beds",key_phrase="number_of_bedrooms",provider=p1)
        Fields.objects.create(name="fullBath",key_phrase="full_bath_count",provider=p1)




#models Test
class providerandfieldsTest(TestCase):
    
    #Provider Tests
    def create_provider1(self,name="PropertyKnowledge",url="https://26dba07c-dfe2-40c0-90bd-3b2c789f1600.mock.pstmn.io/location/house/info",priority="2"):
        return Provider.objects.create(name=name,url=url,priority=priority,created_at=timezone.now())
    def create_provider2(self,name="zillow Library",url="https://fd34f8e2-6052-483a-9b8e-f7ecdffe3711.mock.pstmn.io/home/details",priority="1",auth_key="PMAK-6009c2980e728d00379f8a45-e79c6092ce3471ee4624089615bf406923"):
        return Provider.objects.create(name=name,url=url,priority=priority,created_at=timezone.now(),auth_key=auth_key)
    
    def test_providerA_creation(self):
        providerA = self.create_provider1()

        self.assertTrue(isinstance(providerA,Provider))
        self.assertEqual(providerA.__str__(),providerA.name)
    def test_providerB_creation(self):
        providerB = self.create_provider2()

        self.assertTrue(isinstance(providerB,Provider))
        self.assertEqual(providerB.__str__(),providerB.name)

    #Fields Test
    
    def create_field1(self,name="sewerSystem",key_phrase="sewer"):
        provider= self.create_provider1()
        return Fields.objects.create(name=name,key_phrase=key_phrase,provider=provider)
    
    def create_field2(self,name="sewerSys",key_phrase="sewer",provider="5"):
        provider= self.create_provider2()
        return Fields.objects.create(name=name,key_phrase=key_phrase,provider=provider)
    
    def create_field3(self,name="constructionStyle",key_phrase="style",provider="4"):
        provider= self.create_provider1()
        return Fields.objects.create(name=name,key_phrase=key_phrase,provider=provider)
    
    def create_field4(self,name="buildStyle",key_phrase="style",provider="5"):
        provider= self.create_provider2()
        return Fields.objects.create(name=name,key_phrase=key_phrase,provider=provider)
    
    def create_field5(self,name="hasPool",key_phrase="pool",provider="5"):
        provider= self.create_provider2()
        return Fields.objects.create(name=name,key_phrase=key_phrase,provider=provider)
    
    def create_field6(self,name="no_of_beds",key_phrase="number_of_bedrooms",provider="4"):
        provider= self.create_provider1()
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
    


