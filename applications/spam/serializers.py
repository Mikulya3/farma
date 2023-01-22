from django.contrib.auth import get_user_model
from rest_framework import serializers
from applications.spam.models import Spam
from main.tasks import spam_message

User = get_user_model()
class SpamSerializer(serializers.ModelSerializer):
    email =serializers.EmailField(required=False)
    class Meta:
        model = Spam
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        spam = Spam.objects.create(email=request.user.email)
        spam_message.delay(User.email)
        return spam

