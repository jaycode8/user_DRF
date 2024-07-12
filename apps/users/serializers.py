from rest_framework import serializers
from .models import Users
from django.contrib.auth.hashers import make_password

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = "__all__"

    def create(self, validated_data):
        password = validated_data['password']
        hashed_password = make_password(password)
        instance = super().create(validated_data)
        instance.password = hashed_password
        instance.save()
        return instance