from rest_framework.serializers import ModelSerializer
from core.models import Drive_File


class DriveSerializer(ModelSerializer):
	class Meta:
		model = Drive_File
		fields = '__all__'

