from django.db import models
from django.contrib.auth.models import User
from PIL import Image

from django.core.files.storage import default_storage as storage

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

# # i need to fix following code as it doesnt work with azure blob storage
        
#     def save(self):
#         super().save()

#         img = Image.open(self.image.path)
#         if img.height > 300 or img.width > 300:
#             output_size = (300,300)
#             img.thumbnail(output_size)
#             img.save(self.image.path)

# file = models.ImageField(upload_to='images/')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            # Open the image file using Django's storage API
            f = storage.open(self.image.name, 'r')
            image = Image.open(f)

            if image.height > 300 or image.width > 300:
                output_size = (300, 300)
                image.thumbnail(output_size)
                
                # Save the resized image back to storage
                f = storage.open(self.image.name, 'w')
                image.save(f, format='JPEG')

            f.close()   