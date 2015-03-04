# -*- coding:utf-8 -*-

from rest_framework import serializers
# from rest_framework.validators import UniqueTogetherValidator

from rest_api.models import Performers, Requests


class PerformerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performers
        fields = (
            'id',
            'name',
            'active',
            # 'requests',
        )


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requests


class RequestGetSerializer(RequestSerializer):
    performer = PerformerSerializer()


class PerformerRequestsSerializer(serializers.ModelSerializer):
    requests = RequestSerializer(many=True, read_only=True)

    class Meta:
        model = Performers
        fields = (
            'id',
            'name',
            'active',
            'requests',
        )


# class RequestCheckSerializer(RequestSerializer):
#     class Meta:
#         fields = (
#             'in_number',
#             'out_number',
#         )
# class PerformerCheckSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Performers
#         fields = (
#             'name',
#         )


# class PerformerSerializer(serializers.ModelSerializer):
    # requests = serializers.StringRelatedField(many=True, read_only=True)
    # requests = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='api_performer_requests',
    #     lookup_field='name'
    # )
    # requests = serializers.HyperlinkedIdentityField(
    #     'requests',
    #     view_name='api_performer_requests',
    #     lookup_field='name'
    # )
    # requests = serializers.RelatedField(many=True, read_only=True)
    # requests = serializers.PrimaryKeyRelatedField(
    #     many=True,
    #     queryset= Requests.objects.all()
    # )
    # requests = PerformerRequests(many=True, queryset=Requests.objects.all())
    # requests = RequestSerializer(many=True)


# class RequestSerializer(serializers.ModelSerializer):
    # def __init__(self, *args, **kwargs):
    #     super(RequestSerializer, self).__init__(*args, **kwargs)
    #     self.fields['in_number'].error_messages['unique'] = u'My custom msg'

    # validators = [
    #     UniqueTogetherValidator(
    #         queryset=Requests.objects.all(),
    #         fields = ('in_number'),
    #         message='wrong in number'
    #     )
    # ]

    # performer = serializers.PrimaryKeyRelatedField(
    # performer = serializers.StringRelatedField(
    # performer = serializers.SlugRelatedField(
    # #     many = True,
    #     read_only = True,
    #     slug_field = 'name'
    # #     view_name='api_performer_detail',
    # #     queryset=Performers.objects.all()
    # )
    # fields = [
    #     'in_number',
    #     'out_number',
    #     'filling_date',
    #     'performance_date',
    #     'text',
    #     'applicant',
    #     'performer',
    # ]
    # performer = PerformerSerializer()
    # performer = serializers.Field
    # performer = PerformerSerializer(required=False)

    # def get_validation_exclusions(self):
    #   exclusions = super(RequestSerializer, self).get_validation_exclusions()
    #   return exclusions + ['performer']