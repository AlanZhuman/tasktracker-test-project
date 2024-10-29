from rest_framework import serializers
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='id', read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('user_id', 'name', 'email', 'telegram', 'password')
        read_only_fields = ('user_id', '')

    def create(self, validated_data):
        # Создаем пользователя
        user = User.objects.create_user(
            name=validated_data['name'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        # Находим или создаем группу 'R-user' и добавляем пользователя
        r_user_group = Group.objects.get(name='R-user')
        user.groups.add(r_user_group)

        return user
    
class UserUpdateSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = User
        fields = ('user_id', 'name', 'email', 'telegram')
        read_only_fields = ('user_id', 'name')

class UserInnerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='id', read_only=True)
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('user_id', 'name', 'role')
        read_only_fields = ('user_id', 'role')

class UserRoleSetSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='id', read_only=True)
    role = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('user_id', 'role')
        read_only_fields = ('user_id', '')

    def update(self, instance, validated_data):
        permission = validated_data.get('role')

        if permission == 'CUD' or permission == 'CUD-user':
            cud_user_group = Group.objects.get(name='CUD-user')
            instance.groups.add(cud_user_group)
            return instance
        
        elif permission == 'Pm' or permission == 'Pm-user':
            pm_user_group = Group.objects.get(name='Pm-user')
            instance.groups.add(pm_user_group)
            return instance

        else: return False
