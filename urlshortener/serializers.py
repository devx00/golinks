from urlshortener.models import Link
from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    links = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='slug')

    class Meta:
        model = User
        fields = ['id', 'username', 'links']


class LinkSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    click_count = serializers.ReadOnlyField()
    class Meta:
        model = Link
        fields = ['slug', 'created_at', 'click_count', 'url', 'owner']
