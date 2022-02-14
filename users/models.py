from django.db import models


class Messages(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True, verbose_name='ID')
    id_user = models.ForeignKey('User', models.DO_NOTHING, db_column='IDUser', blank=True, null=True,
                                verbose_name='Пользователь')
    message = models.TextField(db_column='Message', verbose_name='Текст сообщения')
    date = models.DateTimeField(db_column='Date', verbose_name='Дата сообщения')

    def __str__(self):
        return f'{self.id_user} - {self.date}'

    class Meta:
        managed = False
        db_table = 'messages'
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class User(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True, verbose_name='ID')
    login = models.CharField(db_column='Login', max_length=100, verbose_name='Логин')
    first_name = models.CharField(db_column='FirstName', max_length=100, verbose_name='Имя')
    last_name = models.CharField(db_column='LastName', max_length=100, verbose_name='Фамилия')
    patronymic = models.CharField(db_column='Patronymic', max_length=100, blank=True, null=True,
                                  verbose_name='Отчество')
    email = models.CharField(max_length=100, blank=True, null=True, verbose_name='Email')
    phone = models.CharField(db_column='Phone', max_length=20, verbose_name='Телефон')
    password = models.CharField(db_column='Password', max_length=100, verbose_name='Пароль')

    def __str__(self):
        return f'{self.login}'

    class Meta:
        managed = False
        db_table = 'user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
