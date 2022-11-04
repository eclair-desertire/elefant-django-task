from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)
from apps.catalog.managers import UserManager
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class Review(models.Model):
    review_id=models.AutoField(primary_key=True)
    explanation=models.TextField('Описание',blank=True,null=True)
    rate=models.IntegerField(
        verbose_name='Оценка',
        default=1,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ]
    )

class Genre(models.Model):
    genre_id=models.AutoField(primary_key=True)
    genre_name=models.CharField('Жанр',max_length=255,default='',unique=True)


    def __str__(self) -> str:
        return self.genre_name

class Book(models.Model):
    book_id=models.AutoField(primary_key=True)
    book_name=models.CharField('Наименование книги',max_length=255,default='')

    genre_name=models.ForeignKey(
        Genre,
        related_name='books',
        to_field='genre_name',
        db_column='genre',
        on_delete=models.CASCADE
    )

    author=models.CharField('Автор',max_length=255,default='',blank=True,null=True)
    description=models.TextField('Описание книги',default='',blank=True,null=True)
    published_date=models.DateField()
    avg_rate=models.IntegerField('Средний рейтинг книги',default=0)

    reviews=models.ManyToManyField(
        Review,
        related_name='books',
        blank=True,
        null=True
    )

    @classmethod
    def calculate_avg_rate(self):
        if self.reviews:

            for i in self.reviews:
                self.avg_rate+=i

            self.avg_rate/=len(self.reviews)

            self.save()
            



    def __str__(self) -> str:
        return self.book_name+'. Автор: '+self.author

class User(AbstractBaseUser, PermissionsMixin):
    
    objects = UserManager()

    IS_ACTIVE = (
        (True, 'Не заблокирован'),
        (False, 'Заблокирован'),
    )

    id = models.AutoField(primary_key=True)
    username = models.EmailField('email', max_length=50, default='', unique=True)

    fav_books=models.ManyToManyField(
        Book,
        related_name='users',
        blank=True,
        null=True
    )

    reviews=models.ManyToManyField(
        Review,
        related_name='users',
        blank=True,
        null=True
    )

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(
        default=True,
        choices=IS_ACTIVE,
        verbose_name='Статус доступа',
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return str(self.username)



