from rest_framework import serializers
from .. import models
from ..models import Post, Comment, Category


class PostSerializer(serializers.Serializer):

    CAT_CHOICES = [(cat.pk, str(cat)) for cat in Category.objects.all()]

    post_id = serializers.AutoField(read_only=True)
    title = serializers.CharField()
    content = serializers.TextField()
    cat = serializers.ChoiceField(choices=CAT_CHOICES)
    post_image = serializers.ImageField()
    created_at = serializers.DateTimeField()

    def create(self, validated_data):
        return Post.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.cat = validated_data.get('cat', instance.cat)
        instance.post_image = validated_data.get('post_image', instance.post_image)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.save()
        return instance

class CommentSerializer(serializers.Serializer):
    comment_id = serializers.AutoField(read_only=True)
    content = serializers.CharField()
    created_at = serializers.DateTimeField()
    post = serializers.PrimaryKeyRelatedField(Post, on_delete=models.CASCADE, related_name='comments')
    
    def create(self, validated_data):
        return Comment.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.content = validated_data.get('content', instance.content)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.save()
        return instance