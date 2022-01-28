from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True, style={
        'input_type': 'password'
    })

    class Meta:
        model = User
        fields = ['url', 'email', 'username', 'password']
