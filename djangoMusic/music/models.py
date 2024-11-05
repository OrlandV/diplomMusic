from django.db import models
from .fields import fields


class Name(models.Model):
    name = models.CharField(fields()[20][1], max_length=fields()[20][3])

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class MediaFormat(models.Model):
    name = models.CharField(fields()[20][1], max_length=fields(f=True)[20][3])

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'media_format'


class Label(Name):
    class Meta(Name.Meta):
        db_table = 'label'


class Manufacturer(Name):
    class Meta(Name.Meta):
        db_table = 'manufacturer'


class Names(models.Model):
    name_original = models.CharField(fields()[2][1], max_length=fields()[2][3], blank=True, null=True)
    name_romaji = models.CharField(fields()[3][1], max_length=fields()[3][3], blank=True, null=True)
    name_english = models.CharField(fields()[4][1], max_length=fields()[4][3], blank=True, null=True)

    def __str__(self):
        return self.name_romaji

    class Meta:
        abstract = True


class Album(Names):
    date = models.DateField(fields()[13][1])
    catalog_number = models.CharField(fields()[14][1], max_length=fields()[14][3], blank=True, null=True)
    count_of_discs = models.IntegerField(fields()[15][1], default=1)
    count_of_tracks = models.IntegerField(fields()[16][1], default=1)
    media_format = models.ForeignKey(MediaFormat, models.RESTRICT, 'fk_album_media_format')
    label = models.ForeignKey(Label, models.RESTRICT, 'fk_album_label')
    manufacturer = models.ForeignKey(Manufacturer, models.RESTRICT, 'fk_album_manufacturer')
    notes = models.CharField(fields()[12][1], max_length=fields()[12][3], blank=True, null=True)

    class Meta(Names.Meta):
        db_table = 'album'


class OSTFrom(Names):
    date = models.DateField(fields()[13][1], blank=True)

    class Meta(Names.Meta):
        db_table = 'ost_from'


class Author(models.Model):
    name_original = models.CharField(fields()[21][1], max_length=fields()[21][3], blank=True, null=True)
    name_romaji = models.CharField(fields()[22][1], max_length=fields()[22][3], blank=True, null=True)

    def __str__(self):
        return self.name_romaji

    class Meta:
        db_table = 'author'


class Track(Names):
    album = models.ForeignKey(Album, models.RESTRICT, 'fk_track_album')
    number_in_album = models.IntegerField(fields()[6][1], default=1)
    duration = models.TimeField(fields()[7][1])
    notes = models.CharField(fields()[12][1], max_length=fields()[12][3], blank=True, null=True)
    ost_from = models.ManyToManyField(OSTFrom)
    # performer = models.ManyToManyField(Author, through='Performer')
    # lyricist = models.ManyToManyField(Author, through='Lyricist')
    # composer = models.ManyToManyField(Author, through='Composer')
    # arranger = models.ManyToManyField(Author, through='Arranger')

    class Meta(Names.Meta):
        db_table = 'track'


class Performer(models.Model):
    track_id = models.ForeignKey(Track, models.RESTRICT, 'fk_performer_track')
    author_id = models.ForeignKey(Author, models.RESTRICT, 'fk_performer_author')

    class Meta:
        db_table = 'performer'


class Lyricist(models.Model):
    track_id = models.ForeignKey(Track, models.RESTRICT, 'fk_lyricist_track')
    author_id = models.ForeignKey(Author, models.RESTRICT, 'fk_lyricist_author')

    class Meta:
        db_table = 'lyricist'


class Composer(models.Model):
    track_id = models.ForeignKey(Track, models.RESTRICT, 'fk_composer_track')
    author_id = models.ForeignKey(Author, models.RESTRICT, 'fk_composer_author')

    class Meta:
        db_table = 'composer'


class Arranger(models.Model):
    track_id = models.ForeignKey(Track, models.RESTRICT, 'fk_arranger_track')
    author_id = models.ForeignKey(Author, models.RESTRICT, 'fk_arranger_author')

    class Meta:
        db_table = 'arranger'


# class Search(models.Manager):
#     def __init__(self, filter):
#         super().__init__()
#
#     def get_queryset(self):
#         return super().get_queryset().filter()
