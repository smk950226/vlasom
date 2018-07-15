import json
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from apps.contents.models import Contents
from .models import Like



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

    return HttpResponse(json.dumps(context), content_type="application/json")