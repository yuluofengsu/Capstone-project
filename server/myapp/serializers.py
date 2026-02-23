from rest_framework import serializers
import urllib.parse

from myapp.models import Book, Classification, Tag, User, Comment, Record, LoginLog, Borrow, BorrowLog, OpLog, Banner, \
    Ad, Notice, ErrorLog, Address, CommunityPost, ReadingEvent, CommunityComment


def rewrite_cover_url(url, request):
    if url and 'doubanio.com' in str(url):
        encoded_url = urllib.parse.quote(str(url))
        proxy_path = f'/myapp/index/image/proxy?url={encoded_url}'
        if request:
            return request.build_absolute_uri(proxy_path)
        else:
            return f'http://127.0.0.1:8000{proxy_path}'
    return url


class BookSerializer(serializers.ModelSerializer):
    # 额外字段
    classification_title = serializers.ReadOnlyField(source='classification.title')

    class Meta:
        model = Book
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.cover and str(instance.cover).startswith('http'):
            ret['cover'] = rewrite_cover_url(str(instance.cover), self.context.get('request'))
        return ret


class DetailBookSerializer(serializers.ModelSerializer):
    # 额外字段
    classification_title = serializers.ReadOnlyField(source='classification.title')

    class Meta:
        model = Book
        # 排除多对多字段
        exclude = ('wish', 'collect',)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.cover and str(instance.cover).startswith('http'):
            ret['cover'] = rewrite_cover_url(str(instance.cover), self.context.get('request'))
        return ret


class UpdateBookSerializer(serializers.ModelSerializer):
    # 额外字段
    classification_title = serializers.ReadOnlyField(source='classification.title')

    class Meta:
        model = Book
        # 排除多对多字段
        exclude = ('wish', 'collect',)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.cover and str(instance.cover).startswith('http'):
            ret['cover'] = rewrite_cover_url(str(instance.cover), self.context.get('request'))
        return ret


class ListBookSerializer(serializers.ModelSerializer):
    # 额外字段
    classification_title = serializers.ReadOnlyField(source='classification.title')

    class Meta:
        model = Book
        # 排除字段
        exclude = ('wish', 'collect', 'description',)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.cover and str(instance.cover).startswith('http'):
            ret['cover'] = rewrite_cover_url(str(instance.cover), self.context.get('request'))
        return ret


class ClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classification
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = User
        fields = '__all__'
        # exclude = ('password',)


class CommentSerializer(serializers.ModelSerializer):
    comment_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    # 额外字段
    title = serializers.ReadOnlyField(source='book.title')
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ['id', 'content', 'comment_time', 'like_count', 'book', 'user', 'title', 'username']


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = '__all__'


class LoginLogSerializer(serializers.ModelSerializer):
    log_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = LoginLog
        fields = '__all__'


class OpLogSerializer(serializers.ModelSerializer):
    re_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = OpLog
        fields = '__all__'


class ErrorLogSerializer(serializers.ModelSerializer):
    log_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = ErrorLog
        fields = '__all__'


class BorrowSerializer(serializers.ModelSerializer):
    borrow_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    expect_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    return_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    # extra
    username = serializers.ReadOnlyField(source='user.username')
    title = serializers.ReadOnlyField(source='book.title')
    cover = serializers.FileField(source='book.cover', required=False)

    class Meta:
        model = Borrow
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.book and instance.book.cover and str(instance.book.cover).startswith('http'):
            ret['cover'] = rewrite_cover_url(str(instance.book.cover), self.context.get('request'))
        return ret


class BorrowLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowLog
        fields = '__all__'


class BannerSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    # extra
    title = serializers.ReadOnlyField(source='book.title')

    class Meta:
        model = Banner
        fields = '__all__'


class AdSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = Ad
        fields = '__all__'


class NoticeSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = Notice
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = Address
        fields = '__all__'


class CommunityPostSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    username = serializers.ReadOnlyField(source='user.username')
    avatar = serializers.FileField(source='user.avatar', required=False)
    nickname = serializers.ReadOnlyField(source='user.nickname')

    class Meta:
        model = CommunityPost
        fields = '__all__'


class ReadingEventSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    end_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = ReadingEvent
        fields = '__all__'


class CommunityCommentSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    username = serializers.ReadOnlyField(source='user.username')
    avatar = serializers.FileField(source='user.avatar', required=False)
    nickname = serializers.ReadOnlyField(source='user.nickname')

    class Meta:
        model = CommunityComment
        fields = '__all__'
