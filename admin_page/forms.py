from django import forms
from employees.models import Employees
from assets.models import Devices


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employees
        fields = ('first_name', 'last_name', 'eid', 'department', 'title', 'mobilephone', 'location')


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Devices
        fields = ('device_type', 'device_vendor', 'device_title', 'device_model', 'serial_number', 'device_status', 'user_id', \
                    'supplier', 'purchase_date', 'device_warranty', 'comments')