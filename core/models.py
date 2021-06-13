import os

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Box(models.Model):

    name = models.CharField(max_length=20, unique=True, db_index=True,
        verbose_name='Name', help_text='Box name.', 
        validators=[
            RegexValidator(
                regex='^[a-z0-9]([_](?![_])|[a-z0-9])+[a-z0-9]$',
                message='Name must have only alphanumeric chars and "_".',
                code='invalid_name'
            ),
        ]
    )
    creator = models.ForeignKey(User, on_delete=models.CASCADE, 
        verbose_name='Creator', help_text='Box creator.')            
    description = models.TextField(blank=True,
        verbose_name='Description', help_text='Box description.')
    public = models.BooleanField(
        verbose_name='Public', help_text='If the box is public or private.')        
    downloads = models.PositiveIntegerField(editable=False, default=0,
        verbose_name='Downloads', help_text='Number of Downloads.')
    last_download_at = models.DateTimeField(auto_now=False, 
        editable=False, null=True,
        verbose_name='Last Download at', help_text='Last download time.')

    def __str__(self):
        return self.name        

    class Meta:
        verbose_name = 'Box'
        verbose_name_plural = 'Boxes'        
    

class BoxVersion(models.Model):
    
    KIND_CHOICES = (
        ("vb", "VirtualBox"),
        ("lv", "Libvirt"),
        ("vw", "VMware"),
    )

    def box_version_path(instance, filename):
        filename = '{}-{}.box'.format(instance.box.name, instance.name)
        path = os.path.join('boxes', instance.box.name, filename)
        return path

    box = models.ForeignKey(Box, on_delete=models.CASCADE, 
        verbose_name='Box Version', help_text='Box version.')
    name = models.CharField(max_length=20, unique=True, db_index=True,
        editable=False, verbose_name='Name', help_text='Box version name.', 
        validators=[
            RegexValidator(
                regex='^[a-z0-9]([_](?![_])|[a-z0-9])+[a-z0-9]$',
                message='Name must have only alphanumeric chars and "_".',
                code='invalid_name'
            ),
        ]
    )       
    kind = models.CharField(max_length=2, choices=KIND_CHOICES, 
        verbose_name='Kind', help_text='Box version kind.')  
    description = models.TextField(blank=True,
        verbose_name='Description', help_text='Box version description.')
    created_at = models.DateTimeField(auto_now=True, 
        verbose_name='Created at', help_text='Box creation time.')
    hash = models.CharField(max_length=40, unique=True, db_index=True, 
        verbose_name='Hash', help_text='SHA1 hash of the box.')
    file = models.FileField(upload_to=box_version_path,  max_length=255,
        verbose_name='File', help_text='Box file.')        

    def __str__(self):
        return self.name        

    class Meta:
        verbose_name = 'Box Version'
        verbose_name_plural = 'Box Versions'                     