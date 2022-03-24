from django.db import models
from django.urls import reverse


class Area(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True, verbose_name='ID')
    name = models.CharField(db_column='Name', unique=True, max_length=100, verbose_name='Наименование')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        managed = False
        db_table = 'area'
        verbose_name = 'Район'
        verbose_name_plural = 'Районы'


class Deposit(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True, verbose_name='ID')
    name = models.CharField(db_column='Name', max_length=200, verbose_name='Наименование')
    id_license = models.ForeignKey('License', models.DO_NOTHING, db_column='IDLicense',
                                   verbose_name='Государственный регистрационный номер', related_name='license')
    id_area = models.ForeignKey(Area, models.DO_NOTHING, db_column='IDArea', verbose_name='Район')
    NOT_MASTERED = 'Не освоен'
    POORLY_MASTERED = 'Слабо освоен'
    MASTERED = 'Освоен'
    degree_of_development = [
        (NOT_MASTERED, 'Не освоен'),
        (POORLY_MASTERED, 'Слабо освоен'),
        (MASTERED, 'Освоен')
    ]
    development = models.CharField(db_column='Development', max_length=30, blank=True, null=True,
                                   choices=degree_of_development, default=NOT_MASTERED, verbose_name='Степень освоения')
    a_b_c1 = models.FloatField(db_column='A+B+C1, kg', blank=True, null=True, verbose_name='Запасы (A+B+C1)')
    c2 = models.FloatField(db_column='C2, kg', blank=True, null=True, verbose_name='Запасы (C2)')
    off_balance = models.FloatField(db_column='Off-balance, kg', blank=True, null=True,
                                    verbose_name='Забалансовые запасы')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        managed = False
        db_table = 'deposit'
        verbose_name = 'Месторождение'
        verbose_name_plural = 'Месторождения'


class SubsoilUsers(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True, verbose_name='ID')
    name = models.CharField(db_column='Name', max_length=100, verbose_name='Наименование')
    tin = models.CharField(db_column='TIN', unique=True, max_length=12, verbose_name='ИНН')
    iec = models.CharField(db_column='IEC', max_length=9, blank=True, null=True, verbose_name='КПП')
    psrn_psrnsp = models.CharField(db_column='PSRN/PSRNSP', unique=True, max_length=15, verbose_name='ОГРН')
    date_of_registration = models.DateField(db_column='DateOfRegistration', verbose_name='Дата регистрации')
    director = models.CharField(db_column='Director', max_length=100, verbose_name='Руководитель')

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('subsoil_user_detail', kwargs={'pk': self.id})

    class Meta:
        managed = True
        db_table = 'subsoil_user'
        verbose_name = 'Недропользователь'
        verbose_name_plural = 'Недропользователи'


class License(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True, verbose_name='ID')
    name = models.CharField(db_column='Name', max_length=15, verbose_name='Наименование')
    id_subsoil_users = models.ForeignKey(SubsoilUsers, models.DO_NOTHING, db_column='IDSubsoilUsers',
                                         verbose_name='Недропользователь')
    start_date = models.DateField(db_column='StartDate', verbose_name='Дата начала срока действия лицензии')
    end_date = models.DateField(db_column='EndDate', verbose_name='Дата окончания срока действия лицензии')
    cancelled = models.BooleanField(db_column='Cancelled', verbose_name='Действие лицензии прекращено')
    destination = models.CharField(db_column='Destination', max_length=255, verbose_name='Целевое назначение лицензии')
    diversion = models.CharField(db_column='Diversion', max_length=30, verbose_name='Статус отвода')

    def __str__(self):
        return f'{self.name}'

    def get_deposit(self):
        deposit = self.license.first()
        return deposit.name if deposit else '-'

    get_deposit.short_description = 'Месторождение'

    class Meta:
        managed = False
        db_table = 'license'
        verbose_name = 'Лицензия'
        verbose_name_plural = 'Лицензии'


class Localities(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True, verbose_name='ID')
    name = models.CharField(db_column='Name', max_length=100, verbose_name='Наименование')
    id_area = models.ForeignKey(Area, models.DO_NOTHING, db_column='IDArea', verbose_name='Район',
                                related_name='localities')
    id_locality_type = models.ForeignKey('LocalitiesType', models.DO_NOTHING, db_column='IDLocalityType',
                                         verbose_name='Тип')

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('locality_detail', kwargs={'pk': self.id})

    class Meta:
        managed = False
        db_table = 'locality'
        verbose_name = 'Населенный пункт'
        verbose_name_plural = 'Населенные пункты'


class LocalitiesType(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True, verbose_name='ID')
    name = models.CharField(db_column='Name', unique=True, max_length=100, verbose_name='Наименование')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        managed = False
        db_table = 'locality_type'
        verbose_name = 'Тип населенных пунктов'
        verbose_name_plural = 'Типы населенных пунктов'


class LocalitiesDeposit(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True, verbose_name='ID')
    id_locality = models.ForeignKey(Localities, models.DO_NOTHING,
                                    db_column='IDLocality', verbose_name='Населенный пункт')
    id_deposit = models.ForeignKey(Deposit, models.DO_NOTHING, db_column='IDDeposit', verbose_name='Месторождение')
    direction = models.CharField(db_column='Direction', max_length=20, verbose_name='Направление')
    distance = models.FloatField(db_column='Distance', verbose_name='Расстояние')

    def __str__(self):
        return f'{self.id_locality} - {self.id_deposit}'

    class Meta:
        managed = False
        db_table = 'locality_deposit'
        verbose_name = 'Связь месторождений с населенными пунктами'
        verbose_name_plural = 'Связи месторождений с населенными пунктами'
