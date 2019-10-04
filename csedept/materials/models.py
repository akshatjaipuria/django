from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.

sem_choices = (
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (7, '7'),
    (8, '8'),
)


class Post(models.Model):
    title = models.CharField(max_length=250, unique=True)
    semester = models.IntegerField(choices=sem_choices, default=3)
    slug = models.SlugField(blank=True)
    description = models.TextField()
    document = models.FileField(upload_to='documents', blank=True)
    posted = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

        def __unicode__(self):
            return u'%s' % self.title

    def get_absolute_url(self):
        return reverse('materials.views.post', args=[self.slug])

    @property
    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug
        super().save(*args, **kwargs)
