from urlextract import URLExtract
from rest_framework.serializers import ValidationError

youtube_urls = ['https://youtube.com', 'http://youtube.com', 'https://www.youtube.com', 'https://www.youtube.com',
                'youtu.be/', 'youtube.com', 'http://youtu.be/', 'https://youtu.be/']


def validate_data(value):
    extractor = URLExtract()
    urls_in_text = extractor.find_urls(value)
    validated_list = []
    for url in urls_in_text:
        for item in youtube_urls:
            if url.startswith(item):
                validated_list.append(url)
    if len(validated_list) < len(urls_in_text):
        raise ValidationError('Ссылки разрешены только на YOUTUBE.COM')