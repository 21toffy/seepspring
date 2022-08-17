from django.contrib import admin

from .models import (
CustomUser,
EmploymentDuration,
SalaryRange,
Employmentinformation,
EmergencyContact,
ColleagueContact,
BankAccountDetails,

UserEmploymentDuration,
UserSalaryRange,

)



admin.site.register(CustomUser)
admin.site.register(EmploymentDuration)
admin.site.register(SalaryRange)
admin.site.register(Employmentinformation)
admin.site.register(EmergencyContact)
admin.site.register(ColleagueContact)
admin.site.register(BankAccountDetails)


admin.site.register(UserEmploymentDuration)
admin.site.register(UserSalaryRange)
