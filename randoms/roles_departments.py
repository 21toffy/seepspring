from adminapp.models import Department, Role

# Create the departments
departments = [
    {'department_name': 'telemarketing', 'department_description': 'Telemarketing department'},
    {'department_name': 'admin', 'department_description': 'Admin department'},
    {'department_name': 'verification', 'department_description': 'Verification department'},
    {'department_name': 'collection', 'department_description': 'Collection department'},
    {'department_name': 'customer_service', 'department_description': 'Customer service department'},
    {'department_name': 'accountant', 'department_description': 'Accountant department'}
]

for department in departments:
    dept, created = Department.objects.get_or_create(department=department["department_name"], defaults={'department_description':department["department_description"]})
    

# Create the roles
roles = [
    {'role_name': 'leader', 'role_description': 'Leader role'},
    {'role_name': 'member', 'role_description': 'Member role'}
]

for role in roles:
    rolee, created = Role.objects.get_or_create(role_name=role["role_name"], defaults={'role_description':role["role_description"]})
