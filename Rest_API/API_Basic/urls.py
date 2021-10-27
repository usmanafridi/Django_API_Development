
from django.urls import path
from .views import ArticleAPIView, article_detail, ArticleDetails, GenericAPIView

urlpatterns = [
    #path('article/', article_list),
     path('article/', ArticleAPIView.as_view()),   #the as_view is used becuase it is class
     path('detail/<int:pk>/', article_detail),
     path('detail/<int:id>/', ArticleDetails.as_view()), 
     path('generic/article/<int:id>', GenericAPIView.as_view()), 
]