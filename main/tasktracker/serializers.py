from rest_framework import serializers
from .models import Task, User, Status
from user.serializers import UserInnerSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

class TaskSerializer(serializers.ModelSerializer):
    task_id = serializers.IntegerField(source='id', read_only=True)
    executor = UserInnerSerializer(many=True)
    observers = UserInnerSerializer(many=True)

    class Meta:
        model = Task
        fields = ('task_id', 'name', 'slug', 'description', 'executor', 'observers', 'status', 'time_start', 'time_end', 'time_deadline')
        read_only_fields = ('task_id', 'slug', 'status', 'time_start', 'time_end')  

    def create(self, validated_data):
        executor_data = validated_data.pop('executor', [])
        observers_data = validated_data.pop('observers', [])

        task = Task.objects.create(**validated_data)
        if executor_data:
            for user_data in executor_data:
                user_name = user_data['name']
                try:
                    user = User.objects.get(name=user_name)
                    task.executor.add(user)
                except ObjectDoesNotExist:
                    continue
        
        if observers_data:
            for user_data in observers_data:
                user_name = user_data['name']
                try:
                    user = User.objects.get(name=user_name)
                    task.observers.add(user)
                except ObjectDoesNotExist:
                    continue

        return task

    def update(self, instance, validated_data):
        executor_data = validated_data.pop('executor', [])
        observers_data = validated_data.pop('observers', [])
        
        # Обновляем основные поля задачи
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.time_deadline = validated_data.get('time_deadline', instance.time_deadline)
        instance.save()

        # Обновляем исполнителей
        if executor_data:
            instance.executor.clear()  # Очистить текущих исполнителей
            for user_data in executor_data:
                user_name = user_data['name']
                try:
                    user = User.objects.get(name=user_name)
                    instance.executor.add(user)
                except ObjectDoesNotExist:
                    continue  # Игнорируем пользователей, которые не найдены
        
        # Обновляем наблюдателей
        if observers_data:
            instance.observers.clear()  # Очистить текущих наблюдателей
            for user_data in observers_data:
                user_name = user_data['name']
                try:
                    user = User.objects.get(name=user_name)
                    instance.observers.add(user)
                except ObjectDoesNotExist:
                    continue  # Игнорируем пользователей, которые не найдены

        return instance

class TaskObserveSerializer(serializers.ModelSerializer):
    task_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = Task
        fields = ('task_id', 'slug')
        read_only_fields = ('task_id', 'slug')  

    def update(self, instance, validated_data):
        isObserve = self.context.get('isObserve')
        user = self.context.get('user_instance')
        user_name = user.name
        if not user_name:
            return False
        if isObserve:
            try:
                user = User.objects.get(name=user_name)
                instance.observers.add(user)
            except ObjectDoesNotExist:
                return False
        else:
            try:
                user = User.objects.get(name=user_name)
                instance.observers.remove(user)
            except ObjectDoesNotExist:
                return False
        
        return instance



class StatusSerializer(serializers.ModelSerializer):
    edit_author = UserInnerSerializer()

    class Meta:
        model = Status
        fields = ('previous_status', 'set_status', 'task', 'edit_author')
        read_only_fields = ('previous_status', 'task')

    def update(self, instance, validated_data):
        status_copy = instance.status # Нужно чтобы скопировать старый статус в Status.previous_status

        # Присвоение инстансу (Task-объекту) нового статуса из set_status и последующее сохранение
        instance.status = validated_data.get('set_status')

        if validated_data.get('set_status') == Task.Statuses.ACTIVE:
            instance.time_start = timezone.now()
        elif validated_data.get('set_status') == Task.Statuses.DONE:
            instance.time_end = timezone.now()

        instance.save()
        # Получение имени автора из data и попытка получить весь объект User (Нужен при создании или изменении Status-объекта)
        name_data = validated_data.get('edit_author', 'unknown')
        name = name_data['name']
        try:
            user_author = User.objects.get(name=name)
        except ObjectDoesNotExist:
            return False
        
        # Смотрим, существует ли уже привязанный к Task-объекту, объект Status, если нет, то создаем, а если есть, то обновляем
        try:
            status_rel = instance.status_log
            status_rel.previous_status = status_copy
            status_rel.set_status = validated_data.get('set_status', status_rel.set_status)
            status_rel.edit_author = user_author
            status_rel.save()
        # Status-объект не существует - создаем
        except ObjectDoesNotExist:
            validated_data.pop('edit_author', None)
            status_rel = Status.objects.create(edit_author=user_author, task=instance, **validated_data)     
        # Возвращаем информацию об созданном (измененном) объекте Status
        return status_rel
