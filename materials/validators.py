from rest_framework.serializers import ValidationError

def validate_youtube_url(value):
    """Разрешает только ссылки, содержащие youtube.com или youtu.be"""
    if value:
        url_lower = value.lower()
        if 'youtube.com' not in url_lower and 'youtu.be' not in url_lower:
            raise ValidationError('Разрешены ссылки только на видеохостинг youtube.com')
