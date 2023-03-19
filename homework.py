from news.models import *
#   Создать двух пользователей (с помощью метода User.objects.create_user).
user1 = User.objects.create_user(username='username1', first_name='FirstName1')
user2 = User.objects.create_user(username='username2', first_name='FirstName2')
#   Создать два объекта модели Author, связанные с пользователями.
author1 = Author.objects.create(authorUser=user1)
author2 = Author.objects.create(authorUser=user2)
#   Добавить 4 категории в модель Category.
category1 = Category.objects.create(categoryName='IT')
category2 = Category.objects.create(categoryName='Sport')
category3 = Category.objects.create(categoryName='Art')
category4 = Category.objects.create(categoryName='Politics')
#   Добавить 2 статьи и 1 новость.
article1 = Post.objects.create(author=author1, categoryType='AR', title='Article 1', text='Article Text 1')
article2 = Post.objects.create(author=author2, categoryType='AR', title='Article 2', text='Article Text 2')
news1 = Post.objects.create(author=author1, categoryType='NW', title='News 1', text='News Text 1')
#   Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий).
PostCategory.objects.create(postThrough=article1, categoryThrough=category1)
PostCategory.objects.create(postThrough=article1, categoryThrough=category3)
PostCategory.objects.create(postThrough=article2, categoryThrough=category4)
PostCategory.objects.create(postThrough=news1, categoryThrough=category2)
PostCategory.objects.create(postThrough=news1, categoryThrough=category3)
#   Создать как минимум 4 комментария к разным объектам модели Post (в каждом объекте должен быть как минимум один комментарий).
comment1 = Comment.objects.create(commentPost=article1, commentUser=user2, text='Comment Text 1')
comment2 = Comment.objects.create(commentPost=article1, commentUser=user1, text='Comment Text 2')
comment3 = Comment.objects.create(commentPost=article2, commentUser=user1, text='Comment Text 3')
comment4 = Comment.objects.create(commentPost=news1, commentUser=user2, text='Comment Text 4')
#   Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов.
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
#   Обновить рейтинги пользователей.
author1.update_rating()
author2.update_rating()


# Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).
best_user = Author.objects.order_by('-ratingAuthor').values('authorUser__username', 'ratingAuthor').first()
print(f"Лучший пользователь: {best_user['authorUser__username']} с рейтингом {best_user['ratingAuthor']}")

# Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи, основываясь на лайках/дислайках к этой статье.
best_article = Post.objects.filter(categoryType='AR').order_by('-rating').first()
print('Лучшая статья:', best_article.dateCreation.strftime('%d.%m.%y %H:%M:%S'), best_article.author.authorUser.username,
      best_article.title, best_article.preview(), sep='\n')

# Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.
comments = Comment.objects.filter(commentPost=best_article)
for c in comments:
      print(f"дата: {c.dateCreation.strftime('%d.%m.%y %H:%M:%S')}, пользователь: {c.commentUser.username}, "
            f"рейтинг {c.rating}, текст комментария: {c.text}")
