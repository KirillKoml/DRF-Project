from rest_framework.serializers import ValidationError


def validate_links(value):
    """Делаю проверку, что начало ссылки начинается так, как ссылка из видео на YouTube."""
    if not value[:24] == 'https://www.youtube.com/':
        raise ValidationError('Ссылка должна быть обязательно с YouTube')