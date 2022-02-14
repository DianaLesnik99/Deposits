from django.db import models


class Area(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', unique=True, max_length=100)  # Field name made lowercase.

    def __str__(self):
        return f'{self.name}'

    class Meta:
        managed = True
        db_table = 'area'
        verbose_name = 'Район'
        verbose_name_plural = 'Районы'


class Deposit(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=200)  # Field name made lowercase.
    idlicense = models.ForeignKey('License', models.DO_NOTHING, db_column='IDLicense')  # Field name made lowercase.
    idarea = models.ForeignKey(Area, models.DO_NOTHING, db_column='IDArea')  # Field name made lowercase.
    development = models.CharField(db_column='Development', max_length=30, blank=True, null=True)  # Field name made lowercase.
    a_b_c1_kg = models.FloatField(db_column='A+B+C1, kg', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    c2_kg = models.FloatField(db_column='C2, kg', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    off_balance_kg = models.FloatField(db_column='Off-balance, kg', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    def __str__(self):
        return f'{self.name}'

    class Meta:
        managed = False
        db_table = 'deposit'
        verbose_name = 'Месторождение'
        verbose_name_plural = 'Месторождения'


class Enterprise(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.
    tin = models.CharField(db_column='TIN', unique=True, max_length=12)  # Field name made lowercase.
    iec = models.CharField(db_column='IEC', max_length=9, blank=True, null=True)  # Field name made lowercase.
    psrn_psrnsp = models.CharField(db_column='PSRN/PSRNSP', unique=True, max_length=15)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dateofregistration = models.DateField(db_column='DateOfRegistration')  # Field name made lowercase.
    director = models.CharField(db_column='Director', max_length=100)  # Field name made lowercase.

    def __str__(self):
        return f'{self.name}'

    class Meta:
        managed = False
        db_table = 'enterprise'
        verbose_name = 'Недропользователь'
        verbose_name_plural = 'Недропользователи'


class License(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=15)  # Field name made lowercase.
    identerprise = models.ForeignKey(Enterprise, models.DO_NOTHING, db_column='IDEnterprise')  # Field name made lowercase.
    startdate = models.DateField(db_column='StartDate')  # Field name made lowercase.
    enddate = models.DateField(db_column='EndDate')  # Field name made lowercase.
    cancelled = models.BooleanField(db_column='Cancelled')  # Field name made lowercase.
    destination = models.CharField(db_column='Destination', max_length=255)  # Field name made lowercase.
    diversion = models.CharField(db_column='Diversion', max_length=30)  # Field name made lowercase.

    def __str__(self):
        return f'{self.name}'

    class Meta:
        managed = False
        db_table = 'license'
        verbose_name = 'Лицензия'
        verbose_name_plural = 'Лицензии'


class Messages(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    iduser = models.ForeignKey('User', models.DO_NOTHING, db_column='IDUser', blank=True, null=True)  # Field name made lowercase.
    message = models.TextField(db_column='Message')  # Field name made lowercase.
    date = models.DateTimeField(db_column='Date')  # Field name made lowercase.

    # def __str__(self):
    #     return f'{self.name}'

    class Meta:
        managed = False
        db_table = 'messages'
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Municipality(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.
    iddeposit = models.ForeignKey(Deposit, models.DO_NOTHING, db_column='IDDeposit')  # Field name made lowercase.
    idarea = models.ForeignKey(Area, models.DO_NOTHING, db_column='IDArea')  # Field name made lowercase.
    idmunicipalitytype = models.ForeignKey('MunicipalityType', models.DO_NOTHING, db_column='IDMunicipalityType')  # Field name made lowercase.
    direction = models.CharField(db_column='Direction', max_length=20)  # Field name made lowercase.
    distance = models.FloatField(db_column='Distance')  # Field name made lowercase.

    def __str__(self):
        return f'{self.name}'

    class Meta:
        managed = False
        db_table = 'municipality'
        verbose_name = 'Населенный пункт'
        verbose_name_plural = 'Населенные пункты'


class MunicipalityType(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', unique=True, max_length=100)  # Field name made lowercase.

    def __str__(self):
        return f'{self.name}'

    class Meta:
        managed = False
        db_table = 'municipalitytype'
        verbose_name = 'Тип населенных пунктов'
        verbose_name_plural = 'Типы населенных пунктов'


class User(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    login = models.CharField(db_column='Login', max_length=100)  # Field name made lowercase.
    firstname = models.CharField(db_column='FirstName', max_length=100)  # Field name made lowercase.
    lastname = models.CharField(db_column='LastName', max_length=100)  # Field name made lowercase.
    patronymic = models.CharField(db_column='Patronymic', max_length=100, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(db_column='Phone', max_length=20)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=100)  # Field name made lowercase.

    def __str__(self):
        return f'{self.login}'

    class Meta:
        managed = False
        db_table = 'user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
