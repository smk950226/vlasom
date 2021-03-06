import json
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView

from apps.contents.models import Contents, Category
from .models import Like, Interest



@login_required
def like_create(request, pk):
    contents = get_object_or_404(Contents, id=pk)

    if Like.objects.filter(user = request.user).filter(contents = contents).exists():
        Like.objects.filter(user = request.user).filter(contents = contents).delete()
        contents.like_count = Like.objects.filter(user = request.user).filter(contents = contents).count()
        contents.save()
        message = '좋아요 취소.'
    else:
        Like.objects.create(user = request.user, contents = contents)
        contents.like_count = Like.objects.filter(user = request.user).filter(contents = contents).count()
        contents.save()
        message = '좋아요.'
    
    context = {'message': message,}

    return render(request, 'preference/_like.html', {
        'like_count': contents.like_count,
    })

@login_required
def interest_create_contents(request, pk):
    contents = get_object_or_404(Contents, id=pk)

    if Interest.objects.filter(user = request.user).filter(contents = contents).exists():
        Interest.objects.filter(user = request.user).filter(contents = contents).delete()
        contents.interest_count = Interest.objects.filter(user = request.user).filter(contents = contents).count()
        contents.save()
        message = '찜하기를 취소하였습니다.'
    else:
        Interest.objects.create(user = request.user, contents = contents)
        contents.interest_count = Interest.objects.filter(user = request.user).filter(contents = contents).count()
        contents.save()
        message = '찜하였습니다.'
    
    context = {'message': message,}

    return HttpResponse(json.dumps(context), content_type="application/json")

@login_required
def interest_create_category(request, pk):
    category = get_object_or_404(Category, id=pk)

    if Interest.objects.filter(user = request.user).filter(category = category).exists():
        Interest.objects.filter(user = request.user).filter(category = category).delete()
        category.interest_count =  Interest.objects.filter(user = request.user).filter(category = category).count()
        category.save()
        message = '찜하기를 취소하였습니다.'
    elif len(Interest.objects.filter(user = request.user, contents__isnull = True)) >= 5:
        message = '카테고리는 최대 5개만 관심등록할 수 있습니다.'
    else:
        Interest.objects.create(user = request.user, category = category)
        category.interest_count =  Interest.objects.filter(user = request.user).filter(category = category).count()
        category.save()
        message = '찜하였습니다.'
    
    context = {'message': message,}

    return HttpResponse(json.dumps(context), content_type="application/json")


class InterestContentsList(ListView):
    model = Contents
    template_name = 'preference/interest/interest_contents_list.html'
    paginate_by = 30

    def get_queryset(self):
        return Interest.objects.filter(user = self.request.user, category__isnull = True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_menu'] = Category.objects.all()
        return context
    
    