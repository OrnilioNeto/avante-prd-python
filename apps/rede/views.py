from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import render, get_object_or_404, redirect

from apps.accounts.models import User
from .models import Post, Follow, Like, Comentario


@login_required
def feed(request):
    user = request.user
    seguindo_ids = Follow.objects.filter(follower=user).values_list('following_id', flat=True)
    posts = Post.objects.filter(author__in=list(seguindo_ids) + [user.pk])

    liked_ids = Like.objects.filter(user=user, post=OuterRef('pk')).values('pk')
    posts = posts.annotate(curtido=Exists(liked_ids)).select_related('author').prefetch_related('comentarios__user')

    sugestoes = User.objects.filter(role__in=['professor', 'aluno']).exclude(
        pk__in=list(seguindo_ids) + [user.pk]
    ).exclude(is_superuser=True)[:6]

    seguindo_users = User.objects.filter(pk__in=seguindo_ids)
    seguidores_users = User.objects.filter(pk__in=Follow.objects.filter(following=user).values('follower'))

    return render(request, 'rede/feed.html', {
        'posts': posts,
        'sugestoes': sugestoes,
        'seguindo_users': seguindo_users,
        'seguidores_users': seguidores_users,
    })


@login_required
def criar_post(request):
    if request.method == 'POST':
        content = request.POST.get('content', '')
        image = request.FILES.get('image')
        Post.objects.create(author=request.user, content=content, image=image)
    return redirect('rede:feed')


@login_required
def curtir(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return redirect(request.META.get('HTTP_REFERER', 'rede:feed'))


@login_required
def comentar(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Comentario.objects.create(user=request.user, post=post, content=content)
    return redirect(request.META.get('HTTP_REFERER', 'rede:feed'))


@login_required
def excluir_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author == request.user or request.user.is_superuser:
        post.delete()
    return redirect('rede:feed')


@login_required
def seguir(request, user_id):
    target = get_object_or_404(User, pk=user_id)
    if target != request.user:
        follow, created = Follow.objects.get_or_create(follower=request.user, following=target)
        if not created:
            follow.delete()
    return redirect(request.META.get('HTTP_REFERER', 'rede:feed'))


@login_required
def perfil(request, user_id):
    profile_user = get_object_or_404(User, pk=user_id)
    posts = Post.objects.filter(author=profile_user).select_related('author')
    seguidores = Follow.objects.filter(following=profile_user).count()
    seguindo = Follow.objects.filter(follower=profile_user).count()
    ja_segue = Follow.objects.filter(follower=request.user, following=profile_user).exists()

    return render(request, 'rede/perfil.html', {
        'profile_user': profile_user,
        'posts': posts,
        'seguidores': seguidores,
        'seguindo': seguindo,
        'ja_segue': ja_segue,
    })


@login_required
def seguindo(request):
    users = User.objects.filter(
        pk__in=Follow.objects.filter(follower=request.user).values('following')
    )
    return render(request, 'rede/seguindo.html', {'users': users})
