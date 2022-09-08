from django.urls import path, re_path
from .views import CommentMe, CreateComment, PoemList, CommentsList, PoemSlide,CategoryMe

urlpatterns = [
    re_path(r'^(cat/(?P<cat>\w*)/)?$', PoemList.as_view({'get': 'list'})),
    re_path(r'^search/(?P<search>\w+)/$', PoemList.as_view({'get': 'list'})),
    path('poem/<str:slug>', PoemList.as_view({'get': 'retrieve'}), name='show_poem'),
    path('slide/<int:count>/', PoemSlide.as_view({'get': 'list'})),
    path('comment/<int:count>/', CommentsList.as_view({'get': 'list'})),
    path('comment/', CommentsList.cout_comment),
    path('comment/<int:pk>/', CommentsList.as_view({'get': 'update'})),
    path('comment/me/<int:pk>/', CommentMe.as_view()),
    path('add/comment/', CreateComment.as_view()),
    path('all/category/', CategoryMe.as_view()),
]