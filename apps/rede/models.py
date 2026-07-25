from django.db import models
from django.conf import settings


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(blank=True, verbose_name='Texto')
    image = models.ImageField(upload_to='rede/', blank=True, verbose_name='Imagem')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-created_at']

    def total_likes(self):
        return self.likes.count()

    def total_comments(self):
        return self.comentarios.count()

    def __str__(self):
        return f'{self.author.get_full_name() or self.author.username}: {self.content[:50]}'


class Follow(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='seguindo')
    following = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='seguidores')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Seguir'
        verbose_name_plural = 'Seguindo'
        unique_together = ('follower', 'following')

    def __str__(self):
        return f'{self.follower} segue {self.following}'


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='curtidas')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Curtida'
        verbose_name_plural = 'Curtidas'
        unique_together = ('user', 'post')

    def __str__(self):
        return f'{self.user} curtiu {self.post.id}'


class Comentario(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comentarios')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comentarios')
    content = models.TextField(verbose_name='Comentário')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.user}: {self.content[:50]}'
