from django.db import models

class Image(models.Model):
    image_id        = models.CharField(max_length=32, blank=True, null=True)
    file            = models.ImageField()
    order           = models.IntegerField(blank=True, null=True)
    caption         = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return str(self.file.url)
    
    class Meta:
        ordering = ['order']