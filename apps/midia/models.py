from django.db import models


class MidiaTreino(models.Model):
    class Tipo(models.TextChoices):
        FOTO = 'foto', 'Foto'
        VIDEO = 'video', 'Vídeo'

    titulo = models.CharField(max_length=255, verbose_name='Título')
    descricao = models.TextField(blank=True, verbose_name='Descrição')
    tipo = models.CharField(max_length=10, choices=Tipo.choices, verbose_name='Tipo')
    arquivo = models.ImageField(upload_to='midias/', blank=True, verbose_name='Arquivo')
    url_youtube = models.URLField(blank=True, verbose_name='URL do YouTube')
    data_publicacao = models.DateField(verbose_name='Data de Publicação')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Mídia de Treino'
        verbose_name_plural = 'Mídias de Treino'
        ordering = ['-data_publicacao']

    def __str__(self):
        return self.titulo
