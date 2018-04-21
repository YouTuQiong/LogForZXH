# from django.contrib.auth.models import User, Group
from rest_framework import generics
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from ZXH.models import *


class LogSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')  # 只读

    class Meta:
        model = Log
        fields = ('id',
            'title',
                  'owner',
                  'mood',
                  'img',
                  'body',
                  'created_time',
                  'modified_time',
                  'excerpt',
                  'location',
                  'weather',
                  'tags',
                  'isShow',
                 )

    def update(self, instance, validated_data):

        instance.title =  validated_data.get('title', instance.title)
        instance.save()

        return instance


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = []
        model = User
        field = ('id', 'username')
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username')









