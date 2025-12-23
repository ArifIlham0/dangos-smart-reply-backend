from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    is_superuser = serializers.BooleanField(default=False, required=False)
    username = serializers.CharField(required=False)
    image = serializers.ImageField(required=False, allow_null=True)
    image_url = serializers.SerializerMethodField()
    
    class Meta(object):
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'image', 'image_url', 'is_superuser', 'is_active', 'date_joined']

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('image', None)
        representation['image'] = representation.pop('image_url')
        return representation
    
class SmartReplySerializer(serializers.Serializer):
    url = serializers.URLField()
    question = serializers.CharField()