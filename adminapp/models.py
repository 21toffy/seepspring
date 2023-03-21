from django.db import models
from common.models import BaseModel
from accounts.models import CustomUser








class Department(BaseModel):
    department_name = models.CharField(max_length=225, null=True, blank=True)
    department_description = models.CharField(max_length=225, null=True, blank=True)

    def __str__(self):
        return self.department_name + " Department "
    

class Role(BaseModel):
    role_name = models.CharField(max_length=225, null=True, blank=True)
    role_description = models.CharField(max_length=225, null=True, blank=True)

    def __str__(self):
        return self.role_name + " role "
    

class Employee(BaseModel):
    user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, null=True, blank=True, on_delete=models.CASCADE)
    default_passsword = models.CharField(max_length=100, null=True, blank=True)

    




