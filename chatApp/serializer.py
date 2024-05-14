from accounts.models import ChatMessages
from rest_framewok import serializers

class ChatSerializer(serializer.Serializers):
    class Meta:
        model = ChatMessages
        fields = ('id', 'sender', 'reciever','message', 'is_read', 'created_at', 'updated_at')
        extra_kwargs = {
            "sender": {"required": True},
            "reciever": {"required": False}
            }