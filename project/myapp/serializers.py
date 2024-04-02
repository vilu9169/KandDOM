from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework.serializers import ModelSerializer, Serializer
from .models import CustomUser



class UserModelSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'phone', 'company_name', 'job_title', 'office_situated']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
    def to_representation(self, instance):
        """Overriding to remove Password Field when returning Data"""
        ret = super().to_representation(instance)
        ret.pop('password', None)
        return ret