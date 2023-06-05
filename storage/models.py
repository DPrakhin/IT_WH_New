from django.db import models
from users.models import NewUser
from employees.models import Employees

class RequestDevice(models.Model):
    code = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, verbose_name='Користувач')
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE, verbose_name='Працівник')
    item = models.CharField(max_length=250, null=False, verbose_name='Тип обладнання')
    status = models.CharField(max_length=120, default='У очікуванні завершення', null=False, verbose_name='Статус')
    datetime = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(max_length=500, verbose_name='Додаток')

    def __str__(self) -> str:
        return str(self.code)
