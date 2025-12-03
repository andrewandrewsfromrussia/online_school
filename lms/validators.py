from urllib.parse import urlparse

from rest_framework import serializers


def validate_youtube_url(value):
    """
    Разрешаем только ссылки на YouTube
    """
    if not value:
        return value

    parsed = urlparse(value)
    domain = parsed.netloc.lower()

    if "youtube.com" not in domain and "youtu.be" not in domain:
        raise serializers.ValidationError("Можно прикреплять только ссылки на YouTube.")

    return value
