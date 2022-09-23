from django.urls import reverse,path,include
from rest_framework import status
from rest_framework.test import APITestCase,URLPatternsTestCase

from .models import User


#Todo test for User model
# assert for token lenght and is_verified

class RegisterTestCase (APITestCase):
  
 
  def test_create_account(self) -> None:
    

    data = {
      
      "username" : "idan",
      "email" : "idan@gmail.com",
      "password":"password22",
      "first_name":"hwhd",
      "last_name":"dfjjfje",
      "address":"4,Lagos Nigeria",
      "phone_number":"+2348102045787",
    }

    url  = reverse('account:user-list')
    response = self.client.post(url,data,format='json')
    self.assertEqual(response.status_code,status.HTTP_201_CREATED)
    self.assertLessEqual(len(User.objects.get().token),60)
    self.assertEqual(User.objects.get().username,"idan")
    
    

 

