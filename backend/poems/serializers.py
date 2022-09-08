from rest_framework import serializers
from .models import Poem, Comment

class PoemSlideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poem
        fields = ('title', 'slug', 'photo')
        
class PoemsListSerializer(serializers.ModelSerializer):
    cats = serializers.SlugRelatedField(slug_field='slug', read_only=True)
    count_comments = serializers.IntegerField()
    class Meta:
        model = Poem
        fields = ('id', 'get_author', 'title', 'slug', 'photo', 'time_create', 'count_view', 'cats', 'count_comments')

class PoemCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poem
        fields = ('id', 'title', 'slug')

class CommentListSerializer(serializers.ModelSerializer):
    poem = PoemCommentSerializer()
    class Meta:
        model = Comment
        fields = ('id', 'name', 'body', 'created', 'poem')
        

class AddCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('name', 'body', 'poem', 'sess', 'ip', 'telegram')

class CommentPoemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'name', 'body')

class PoemsDetailSerializer(serializers.ModelSerializer):
    comments = CommentPoemSerializer(many=True)
    cats = serializers.SlugRelatedField(slug_field='slug', read_only=True)
    count_comments = serializers.IntegerField()
    class Meta:
        model = Poem
        fields = ('id', 'get_author', 'link_stih', 'content','title', 'slug', 'photo', 'time_create',
                  'count_view', 'count_comments', 'cats', 'key_words', 'description', 'comments', 'key_words')