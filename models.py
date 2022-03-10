from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rate = models.IntegerField (default = 0)

    def update_rating(self):
        postRate = self.post_set.aggregate(postRating=Sum('rate'))
        pRate = 0
        pRate += postRate.get('postRating')
        commentRate = self.comment_set.aggregate(commentRating=Sum('rate'))
        cRate = 0
        cRate = cRate + commentRate.get('commentRating')

        self.rate = pRate * 3 + cRate
        self.save()



class Category (models.Model):
    category = models.CharField(max_length=64, unique = True)


class Post(models.Model):
    author = models.ForeignKey("Author", on_delete=models.CASCADE)
    type = models.BooleanField(default=False)# 0 - статья, 1 новость
    time_in = models.DateTimeField(auto_now_add=True)
    heder = models.CharField(max_length=128, default="")
    text = models.TextField(null = True)
    rate = models.IntegerField(default=0)
    categories = models.ManyToManyField("Category", through='PostCategory')

    def like (self):
         self.rate += 1
         self.save()

    def dislike(self):
        self.rate -= 1
        self.save()

    def preview(self):
        s = self.text[0:123]+"..."
        return s


class  PostCategory (models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment (models.Model):
     post = models.ForeignKey("Post", on_delete=models.CASCADE)
     author = models.ForeignKey("Author",on_delete=models.CASCADE)# в данном решении комментировать могут только авторы но не все пользователи (User)
     text = models.TextField()
     time_in = models.DateTimeField(auto_now_add=True)
     rate = models.IntegerField(default=0)

     def like (self):
         self.rate += 1
         self.save()

     def dislike(self):
        self.rate -= 1
        self.save()