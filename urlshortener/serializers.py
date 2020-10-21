from urlshortener.models import Link
from django.contrib.auth.models import User
from rest_framework import serializers



class LinkSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    click_count = serializers.ReadOnlyField()
    class Meta:
        model = Link
        fields = ['slug', 'created_at', 'click_count', 'url', 'owner']


class UserSerializer(serializers.ModelSerializer):
    # links = serializers.SlugRelatedField(
    #     many=True, read_only=True, slug_field='slug')
    links = LinkSerializer(many=True, read_only=True)

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = User.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'links']
