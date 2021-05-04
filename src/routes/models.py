from django.core.exceptions import ValidationError
from django.db import models

from cities.models import City
from trains.models import Train


class Route(models.Model):
    name = models.CharField(max_length=50, unique=True,
                            verbose_name='Название маршрута')
    travel_times = models.PositiveSmallIntegerField(verbose_name='Общее время в пути')
    from_city = models.ForeignKey(City, on_delete=models.CASCADE,
                                  related_name='route_from_сity_set',
                                  verbose_name='Из какого города'
                                  )

    to_city = models.ForeignKey(City, on_delete=models.CASCADE,
                                  related_name='route_to_сity_set',
                                  verbose_name='В какой города'
                                  )

    trains = models.ManyToManyField('trains.Train', verbose_name='список поездов')

    def __str__(self):
        return f'Маршрут {self.name} из города {self.from_city}'


    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'
        ordering = ['travel_times']


def clean(self):
    if self.from_city == self.to_city:
        raise ValidationError('Изменить город прибытия')
    qs = Train.objects.filter(
        from_city=self.from_city, to_city=self.to_city,
        travel_time=self.travel_time).exclude(pk=self.pk)
    # Train == self.__class__
    if qs.exists():
        raise ValidationError('Изменить время в пути')


def save(self, *args, **kwargs):
    self.clean()
    super().save(*args, **kwargs)
