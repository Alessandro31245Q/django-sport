from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_up = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category_name

STATUS_CHOICES = (
    ("Ocupado", "Ocupado"),
    ("Disponible", "Disponible")
)

class Court(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    featured_image = models.ImageField(upload_to='uploads/%Y/%m/%d')
    short_description = models.TextField(max_length=500)
    sport_body = models.TextField(max_length=2000)
    status = models.TextField(max_length=20, choices=STATUS_CHOICES, default="Disponible")
    barrio = models.CharField(max_length=100, default="Sin barrio")
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
class SportRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    court = models.ForeignKey(Court, on_delete=models.CASCADE)
    score = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'court')  # Un usuario solo puede calificar una vez por Court

    def __str__(self):
        return f'{self.user.username} - {self.court.title} - {self.score}'
    
class Amistad(models.Model):
    usuario1 = models.ForeignKey(User, related_name='amigos1', on_delete=models.CASCADE)
    usuario2 = models.ForeignKey(User, related_name='amigos2', on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.usuario1.username} - {self.usuario2.username}"

    class Meta:
        unique_together = ('usuario1', 'usuario2')  # Para evitar relaciones duplicadas

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mensaje de {self.sender.username} a {self.receiver.username}"
