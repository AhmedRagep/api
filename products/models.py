from django.db import models
from django.conf import settings
from django.db.models import Q
# Create your models here.
User = settings.AUTH_USER_MODEL

class ProductQuerySet(models.QuerySet):
    def is_public(self):
        return self.filter(public=True)

    def search(self, query, user=None):
        lookup = Q(title__icontains=query) | Q(content__icontains=query)
        qs = self.is_public().filter(lookup)
        if user is not None:
            qs2 = self.filter(user=user).filter(lookup)
            qs = (qs | qs2).distinct()
        return qs

class ProductManager(models.Manager):
    def get_queryset(self, *args,**kwargs):
        return ProductQuerySet(self.model, using=self._db)

    def search(self, query, user=None):
        return self.get_queryset().search(query, user=user)

class Product(models.Model):
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=50)
    content = models.TextField(null=True, blank=True)
    price = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2, default=99.99)
    public = models.BooleanField(default=True)

    objects = ProductManager()
    
    #@property
    def __str__(self):
       return self.title

    def get_descount(self):
       return "122"
