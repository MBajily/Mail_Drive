from rest_framework.serializers import ModelSerializer
from core.models import Company, Employee, Email, Email_File, Drive_File


class CompanySerializer(ModelSerializer):
	class Meta:
		model = Company
		fields = '__all__'


class EmployeeSerializer(ModelSerializer):
	class Meta:
		model = Employee
		fields = '__all__'


class EmailSerializer(ModelSerializer):
	class Meta:
		model = Email
		fields = '__all__'


class EmailFilesSerializer(ModelSerializer):
	class Meta:
		model = Email_File
		fields = '__all__'


class DriveSerializer(ModelSerializer):
	class Meta:
		model = Drive_File
		fields = '__all__'

