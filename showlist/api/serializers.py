from asyncore import read
from platform import platform

from rest_framework import serializers
from showlist.models import Review, ShowList, StreamPlatform


# Serializer for Review Using serializers.ModelSerializer
class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        exclude = ('show_list',)
        # fields = '__all__'
# ...


# Serializer for ShowList Using serializers.ModelSerializer
class ShowListSerializer(serializers.ModelSerializer):
    # adding non existent field to serializer by using SerializerMethodField
    # len_name = serializers.SerializerMethodField()
    # ...

    # Serializer relationship
    # reviews = ReviewSerializer(many=True, read_only=True)
    # ...
    platform_name = serializers.CharField(
        source='platform.name', read_only=True)  # why this doesn't work

    class Meta:
        model = ShowList
        fields = '__all__'

    # def get_len_name(self, obj):
    #     return len(obj.name)

    # Object Validation
    # def validate(self, data):
    #     if data['name'] == data['description']:
    #         raise serializers.ValidationError(
    #             'Name and Description cannot be the same')

    #     return data
    # ...

    # Field Validation
    # def validate_name(self, value):
    #     if len(value) < 3:
    #         raise serializers.ValidationError(
    #             'Name must be at least 3 characters long')

    #     return value
    # ...
# ...


# Serializer for StreamPlatform Using serializers.ModelSerializer
class StreamPlatformSerializer(serializers.ModelSerializer):
    # Serializer relationship
    show_list = ShowListSerializer(many=True, read_only=True)
    # ...

    class Meta:
        model = StreamPlatform
        fields = '__all__'
# ...


# Using serializers.Serializer
'''
class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    is_active = serializers.BooleanField()

    def create(self, validated_data):
        return Movie.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.is_active = validated_data.get(
            'is_active', instance.is_active)
        instance.save()
        return instance
'''
# ...
