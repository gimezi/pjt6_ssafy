from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from .models import Board, Comment
from .forms import BoardForm, CommentForm
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

# Create your views here.
@require_http_methods(["GET"])
def index(request):
    boards = Board.objects.all().order_by('-created_at')
    context = {
        'boards': boards
    }
    return render(request, 'boards/index.html', context)


@require_http_methods(["GET", "POST"])
def detail(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        if request.user == board.author:    # 글 주인과 접속한 사람이 같을 때만
            board.delete()
            return redirect('boards:index')

    comments = board.comments.all()
    comment_form = CommentForm()
    
    context = {
        'board': board,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'boards/detail.html', context)



@require_http_methods(["GET", "POST"])
@login_required
def update(request, pk):
    board = get_object_or_404(Board, pk=pk)

    if request.method == 'POST':
        form = BoardForm(request.POST, instance=board)
        if form.is_valid() and request.user == board.author:
            form.save()
            return redirect('boards:detail', board.pk)
    else:
        form = BoardForm(instance=board)
    context = {
        'board': board,
        'form': form,
    }        
    return render(request, 'boards/update.html', context)

@require_http_methods(["GET", "POST"])
@login_required
def create(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.author = request.user
            new.save()
            return redirect('boards:index')
    else:
        form = BoardForm()
    context = {
        'form': form,
    }
    return render(request, 'boards/create.html', context)

@require_http_methods(["POST"])
@login_required
def comment(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.board = board
            comment.save()
            return redirect('boards:detail', board.pk)

@require_http_methods(["POST"])
@login_required
def comment_detail(request, board_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == 'POST' and request.user == comment.author:
        comment.delete()
        return redirect('boards:detail', board_pk)