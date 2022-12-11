from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class Podhod(models.Model):
    podhod = models.CharField(max_length=100, blank=True, verbose_name='Подход', null=True)

    class Meta:
        app_label = 'naviway'
        verbose_name = 'Подход'
        verbose_name_plural = 'Подход'

    def __str__(self):
        return self.podhod

    def fortest(self):
        return self.podhod


class Page(models.Model):
    pageid = models.IntegerField(blank=True, verbose_name='Страница - номер', null=True)
    pageparid = models.IntegerField(blank=True, verbose_name='Группа страницы', null=True)
    pagename = models.CharField(max_length=255, blank=True, verbose_name='название и URL страницы', null=True)
    menuname = models.CharField(max_length=150, blank=True, verbose_name='меню', null=True)
    pagetitle = models.CharField(max_length=255, blank=True, verbose_name='Title страницы', null=True)
    pagekeywords = models.CharField(max_length=650, blank=True, verbose_name='keywords страницы', null=True)
    pagedescription = models.CharField(max_length=1000, blank=True, verbose_name='Метатег description страницы',
                                       null=True)
    pagecontent = models.TextField(blank=True, verbose_name='Контент страницы', null=True)
    sort = models.IntegerField(blank=True, verbose_name='сортировка', null=True,
                               validators=[MinValueValidator(0), MaxValueValidator(300)])
    pageimg = models.CharField(max_length=255, blank=True, verbose_name='URL страницы', null=True)

    class Meta:
        verbose_name = 'Контентные страницы'
        verbose_name_plural = 'основные страницы'
        # app_label = "navirator"

    def __str__(self):
        return f'{self.menuname} {self.pageid}'

    def fortest(self):
        return self.pagename

class Texniki(models.Model):
    id_texnik = models.IntegerField(blank=True, verbose_name='Техника - номер', null=True)
    name = models.CharField(max_length=81, blank=True, verbose_name='Наме техники', null=True)
    anotacia = models.TextField(blank=True, verbose_name='Анотация', null=True)
    texnika = models.TextField(blank=True, verbose_name='Контент страницы', null=True)
    koment_spec = models.TextField(blank=True, verbose_name='Комментарий специалиста', null=True)
    id_podxod = models.IntegerField(blank=True, verbose_name='принадлежность техники', null=True)
    istochnik = models.CharField(max_length=100, blank=True, verbose_name='Авторство техники', null=True)
    sex = models.CharField(max_length=20, blank=True, verbose_name='Ограничения по полу', null=True)
    kol_people = models.CharField(max_length=20, blank=True, verbose_name='Нужно людей', null=True)
    age = models.CharField(max_length=50, blank=True, verbose_name='возрастные ограничения', null=True)

    class Meta:
        app_label = 'naviway'
        verbose_name = 'Техники'
        verbose_name_plural = 'Техники'
        ordering = ('name',)

    def agehuman(self):
        if self.age == "adult":
            agehuman = "для взрослых"
        elif self.age == "school_old":
            agehuman = "для школьников и старше"
        elif self.age == "preschool":
            agehuman = "для дошкольников"
        elif self.age == "school_teens":
            agehuman = "для школьников и подростков"
        elif self.age == "teens":
            agehuman = "для подростков  и старше"
        elif self.age == "teens_old":
            agehuman = "для подростков"
        elif self.age == "preschool_school":
            agehuman = "для дошкольников и школьников"
        elif self.age == "school":
            agehuman = "для школьников"
        else:
            agehuman = "для любого возраста"
        return agehuman

    def peoplehuman(self):
        if self.kol_people == "bin":
            peoplehuman = "в паре"
        elif self.kol_people == "group":
            peoplehuman = "в группе"
        elif self.kol_people == "ind":
            peoplehuman = "индивидуально"
        else:
            peoplehuman = ""
        return peoplehuman

    def sexhuman(self):
        if self.sex == "w":
            sexhuman = "для женщин"
        elif self.sex == "m":
            sexhuman = "для мужчин"
        else:
            sexhuman = "для любого пола"
        return sexhuman

    def cutanotacia(self):
        return self.anotacia[:210]

    def __str__(self):
        return self.name

    def fortest(self):
        return self.name


class Targ(models.Model):
    cel_texniki = models.CharField(max_length=100, blank=True, verbose_name='Наименование', null=True)
    koment_cel = models.TextField(blank=True, verbose_name='описание направления', null=True)

    class Meta:
        verbose_name = 'Направления техник'
        verbose_name_plural = 'Направления техник'

    def __str__(self):
        return self.cel_texniki

    def fortest(self):
        return self.cel_texniki

class Targetteh(models.Model):
    id_texnik = models.IntegerField(blank=True, verbose_name='Техника - номер', null=True)
    id_cel = models.IntegerField(blank=True, verbose_name='цель техники', null=True)

    class Meta:
        verbose_name = 'Связь Направлений и техник'
        verbose_name_plural = 'Связь Направлений и техник'

    def __str__(self):
        return self.id_cel

    def fortest(self):
        return self.id_cel


class Cursceteh(models.Model):
    id_cource = models.IntegerField(blank=True, verbose_name='Курс - номер', null=True)
    id_tex = models.IntegerField(blank=True, verbose_name='Номер техники к курсу', null=True)
    n_por = models.IntegerField(blank=True, verbose_name='Порядок в курсе', null=True)

    class Meta:
        verbose_name = 'Связь Курсов и техник'
        verbose_name_plural = 'Связь Курсов и техник'

    def __str__(self):
        return self.id_cource

    def fortest(self):
        return self.id_tex


class Cursce(models.Model):
    name_cource = models.CharField(max_length=50, blank=True, verbose_name='Наименование', null=True)
    koment_cource = models.TextField(blank=True, verbose_name='описание курса', null=True)

    class Meta:
        verbose_name = 'Курсы описалово'
        verbose_name_plural = 'курсы описалово'

    def __str__(self):
        return self.name_cource

    def fortest(self):
        return self.name_cource
