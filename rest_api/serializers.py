#-*- coding:utf-8 -*-
from rest_framework import serializers

# from rest_api.serializers import *
from request_form.models import Performers, Requests

class PerformerSerializer(serializers.ModelSerializer):
    # requests = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='api_performer_requests', lookup_field='name')
    # requests = serializers.HyperlinkedIdentityField('requests', view_name='api_performer_requests', lookup_field='name')
    # requests = serializers.RelatedField(many=True, read_only=True)
    # requests = serializers.PrimaryKeyRelatedField(many=True, queryset= Requests.objects.all())
    requests = serializers.StringRelatedField(many=True)
    # requests = RequestSerializer(many=True)

    #requests = serializers.PrimaryKeyRelatedField(many=True, queryset=Requests.objects.all())
    class Meta:
        model = Performers
        fields = (
            'id',
            'name',
            'requests',
        )


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requests
    # performer = serializers.PrimaryKeyRelatedField(
    # # performer = serializers.HyperlinkedRelatedField(
    # #     many = True,
    # #     read_only= True,
    # #     view_name='api_performer_detail',
    #     queryset=Performers.objects.all()
    # )
    # fields = [
    #     'in_number',
    #     'out_number',
    #     'filling_date',
    #     'performance_date',
    #     'text',
    #     'applicnat',
    #     'performer',
    # ]
    #performer = PerformerSerializer()
    #performer = PerformerSerializer(required=False)

    #def get_validation_exclusions(self):
    #    # Need to exclude `author` since we'll add that later based off the request
    #    exclusions = super(RequestSerializer, self).get_validation_exclusions()
    #    return exclusions + ['performer']


