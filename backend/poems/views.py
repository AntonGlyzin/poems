
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponse
import requests
from django.db.models import Prefetch, F, Count
from rest_framework import viewsets, filters
from antonio.settings import ME_CHAT_ID, TOKEN_BOT_GLYZIN, MY_HOST
from .serializers import PoemSlideSerializer, PoemsListSerializer, PoemsDetailSerializer, CommentListSerializer, AddCommentSerializer
from .models import Poem, Comment, Category
from rest_framework.views import APIView
from captcha.models import CaptchaStore
from rest_framework.response import Response
from django.utils import timezone
from base.views import add_file_access

def robots_txt(request):
    lines = [
        "User-Agent: *",
        f"Sitemap: {MY_HOST}maps/poem/sitemap.xml",
        f"Host: {MY_HOST}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

class CommentMe(APIView):
    def get(self, request, pk):
        sess = self.request.META.get('HTTP_X_CSRFTOKEN') or ''
        comments = list(Comment.activeted.filter(sess=sess, poem__id=pk).values('id'))
        return Response(comments)
    
class CategoryMe(APIView):
    def get(self, request):
        cat = list(Category.objects.all().values('name','slug')[::-1])
        return Response(cat)

class CreateComment(APIView):
    def post(self, request):
        # resText = request.body[::-1]
        # data = base64.b64decode(resText)
        # base64.b64encode(bytes('captcha=old', 'utf-8'))
        data = self.request.data
        # data = json.loads(request.body)
        captcha_0 = data['captcha_0']
        captcha_1 = data['captcha_1']
        # print(csrf(request).get('csrf_token'))
        try:
            CaptchaStore.remove_expired()
            captcha_1_low = captcha_1.lower()
            CaptchaStore.objects.get(
                response=captcha_1_low, hashkey=captcha_0, expiration__gt=timezone.now()
            ).delete()
        except:
            return Response(status=200, data='captcha=old')
        ip = self.request.META.get('HTTP_X_REAL_IP') or self.request.META.get('REMOTE_ADDR')\
                                                        or self.request.META.get('HTTP_X_FORWARDED_FOR')

        sess = self.request.META.get('HTTP_X_CSRFTOKEN') or ''
        data['ip'] = ip
        data['sess'] = sess
        serializer = AddCommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            try:
                name = data['name']
                body = data['body']
                body = f'От {name}\n\n Сообщение:\n{body}'
                params = {'chat_id':ME_CHAT_ID, 'text':body}
                requests.get(f'https://api.telegram.org/bot{TOKEN_BOT_GLYZIN}/sendmessage', params=params)
            except :
                pass
            return Response(status=200, data='sended')
        return Response(status=400)

class PoemSlide(viewsets.ModelViewSet):
    serializer_class = PoemSlideSerializer
    def get_queryset(self):
        count = self.kwargs.get('count', 3)
        poems = Poem.published.order_by('-count_view')[:count:-1]
        return poems

class PoemList(viewsets.ModelViewSet):
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['count_view', 'time_create', 'count_comments']
    ordering = ['-time_create']
    lookup_field = 'slug'
    def get_queryset(self):
        add_file_access(self.request)
        poems = Poem.published.filter(comments__active=1).annotate(count_comments=Count('comments__active'))
        if self.kwargs.get('search', []):
            poems = poems.filter(title__icontains=self.kwargs['search'])
        elif self.kwargs.get('cat', []):
            poems = poems.filter(cats__slug=self.kwargs['cat'])
        elif self.kwargs.get('slug', []):
            poems = poems.prefetch_related(
                Prefetch('comments', queryset=Comment.activeted.all())
            )
        return poems
    def retrieve(self, request, *args, **kwargs):
        try:
            poem = self.get_queryset().get(slug=kwargs['slug'])
            poem.count_view = F('count_view') + 1
            poem.save()
        except :
            pass
        return super().retrieve(request)
    def get_serializer_class(self):
        if self.action == 'list':
            return PoemsListSerializer
        elif self.action == "retrieve":
            return PoemsDetailSerializer
        
class CommentsList(viewsets.ModelViewSet):
    filter_backends = [filters.OrderingFilter]
    serializer_class = CommentListSerializer
    def cout_comment(self):
        count = Comment.activeted.count()
        return HttpResponse(count)
    def get_queryset(self):
        count = self.kwargs.get('count', 3)
        comm = Comment.activeted.order_by('-id')[:count]
        return comm
    def update(self, request, pk=None):
        sess = self.request.META.get('HTTP_X_CSRFTOKEN') or self.request.META.get('CSRF_COOKIE') or ''
        if not sess:
            raise Http404
        item = get_object_or_404(self.queryset, id=pk, sess=sess)
        item.active=False
        item.save()
        return Response(status=200)

