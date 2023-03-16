from news.models import *

user1 = User.objects.create_user(username='username1', first_name='FirstName1')
user2 = User.objects.create_user(username='username2', first_name='FirstName2')

author1 = Author.objects.create(authorUser=user1)
author2 = Author.objects.create(authorUser=user2)

category1 = Category.objects.create(categoryName='IT')
category2 = Category.objects.create(categoryName='Sport')
category3 = Category.objects.create(categoryName='Art')
category4 = Category.objects.create(categoryName='Politics')

article1 = Post.objects.create(author=author1, categoryType='AR', title='Article 1', text='Article Next 1')
article2 = Post.objects.create(author=author2, categoryType='AR', title='Article 2', text='Article Next 2')
news1 = Post.objects.create(author=author1, categoryType='NW', title='News 1', text='News Next 1')

PostCategory.objects.create(postThrough=article1, categoryThrough=category1)
PostCategory.objects.create(postThrough=article1, categoryThrough=category3)
PostCategory.objects.create(postThrough=article2, categoryThrough=category4)
PostCategory.objects.create(postThrough=news1, categoryThrough=category2)
PostCategory.objects.create(postThrough=news1, categoryThrough=category3)

comment1 = Comment.objects.create(commentPost=article1, commentUser=user2, text='Comment Text 1')
comment2 = Comment.objects.create(commentPost=article1, commentUser=user1, text='Comment Text 2')
comment3 = Comment.objects.create(commentPost=article2, commentUser=user1, text='Comment Text 3')
comment4 = Comment.objects.create(commentPost=news1, commentUser=user2, text='Comment Text 4')

article1.like()
article1.like()
article1.like()
article1.like()
article2.like()
article2.like()
news1.like()
news1.like()
article1.dislike()

comment1.like()
comment1.like()
comment1.like()
comment1.like()
comment2.like()
comment2.like()
comment3.like()
comment1.dislike()
comment4.dislike()

author1.update_rating()
author2.update_rating()






