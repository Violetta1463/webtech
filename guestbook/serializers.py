from rest_framework import serializers
from .models import Entry
class EntrySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    image_url = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Entry
        fields = ['id','name','message','created_at','user','image_url']
    def get_user(self,obj): return obj.user.username if obj.user else None
    def get_image_url(self,obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image,'url'):
            url = obj.image.url
            return request.build_absolute_uri(url) if request else url
        return None
    def validate_message(self, value):
        if 'http://' in value or 'https://' in value: raise serializers.ValidationError('Ссылки запрещены')
        return value
