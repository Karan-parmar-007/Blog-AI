from django.db import models
from accounts.models import MyUser

class Category(models.Model):
    def __str__(self):
        return self.title
    cat_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)

    

class Post(models.Model):
    def __str__(self):
        return self.title
    
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=4000)
    cat = models.ForeignKey(Category, on_delete=models.CASCADE)
    post_image = models.ImageField(upload_to="media/")
    video_file = models.FileField(upload_to="videos/", blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    user_id = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True)

class Comment(models.Model):
    def __str__(self):
        return self.comment_id
    comment_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True)


class Like(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  


class AnonymousPost(models.Model):
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="anonymous_images/")
    video = models.FileField(upload_to="anonymous_videos/", blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=False)


    def __str__(self):
        return self.title
