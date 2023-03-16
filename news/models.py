from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def update_rating(self):     # Рейтинг состоит из следующих слагаемых:
        #  суммарный рейтинг статей автора умножается на 3;
        postRat = self.post_set.all().aggregate(sum=Sum('rating'))['sum']
        #  суммарный рейтинг все.х комментариев автора;
        userRat = self.authorUser.comment_set.all().aggregate(sum=Sum('rating'))['sum']
        #  суммарный рейтинг всех комментариев к статьям автора.
        commentRat = Comment.objects.filter(post__author=self.authorUser).aggregate(sum=Sum('rating'))['sum']
        self.ratingAuthor = postRat * 3 + userRat + commentRat
        self.save()


class Category(models.Model):
    categoryName = models.CharField(max_length=64, unique=True)


ARTICLE = 'AR'
NEWS = 'NW'
POST_TYPE = [
    (ARTICLE, 'Статья'),
    (NEWS, 'Новость')
    ]


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categoryType = models.CharField(max_length=2, choices=POST_TYPE, default=ARTICLE)
    dateCreation = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + '...'


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.commentUser.username

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


