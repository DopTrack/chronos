'''
Created on 23 feb. 2016

@author: richardberg
'''

'''
from models import Student


class AuthorizationBackend(object):
    """
    """

    def authenticate(self, username=None, password=None):
        students = Student.objects.filter(name=username, password=password)
        if len(students) > 0:
            return students[0]

    def get_user(self, user_id):
        return Student.objects.get(pk=user_id)
'''