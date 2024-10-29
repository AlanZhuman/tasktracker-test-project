from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = User
        fields = ('user_id', 'name', 'email', 'telegram')
        read_only_fields = ('user_id', '')

class UserUpdateSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = User
        fields = ('user_id', 'name', 'email', 'telegram')
        read_only_fields = ('user_id', 'name')

class UserInnerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = User
        fields = ('user_id', 'name')
        read_only_fields = ('user_id', '')