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
        user = User.objects.create_user(
            name=validated_data['name'],
            email=validated_data['email'],
            password=validated_data['password'],
            telegram=validated_data['telegram']
        )

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

class UserNameOnlySerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = User
        fields = ('user_id', 'name')
        read_only_fields = ('user_id',)
    
    def to_internal_value(self, data):
        name = data.get('name')
        if not name:
            raise serializers.ValidationError({"name": "This field is required."})

        try:
            # Fetch the existing user by name
            user = User.objects.get(name=name)
            return user
        except User.DoesNotExist:
            raise serializers.ValidationError({"name": "User with this name does not exist."})

class CeleryUserNameOnlySerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = User
        fields = ('user_id', 'name')
        read_only_fields = ('user_id',)

class UserRoleSetSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='id', read_only=True)
    role = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('user_id', 'role')
        read_only_fields = ('user_id', '')

    def update(self, instance, validated_data):
        isSet = self.context.get('isSet')
        permission = validated_data.get('role')

        if isSet:
            if permission == 'CRUD' or permission == 'CRUD-user':
                cud_user_group = Group.objects.get(name='CRUD-user')
                instance.groups.add(cud_user_group)
                return instance
            
            elif permission == 'Pm' or permission == 'Pm-user':
                pm_user_group = Group.objects.get(name='Pm-user')
                instance.groups.add(pm_user_group)
                return instance
            else: return False
        else:
            if permission == 'CRUD' or permission == 'CRUD-user':
                cud_user_group = Group.objects.get(name='CRUD-user')
                instance.groups.remove(cud_user_group)
                return instance
            
            elif permission == 'Pm' or permission == 'Pm-user':
                pm_user_group = Group.objects.get(name='Pm-user')
                instance.groups.remove(pm_user_group)
                return instance
            else: return False
