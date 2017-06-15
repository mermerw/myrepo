from django.db import models


class MyModel(models.Model):
    uid = models.PositiveIntegerField()

    class Meta:
        db_table = u'myapp_tab'
