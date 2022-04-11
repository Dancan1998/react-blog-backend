from django.urls import path
from .views import get_all_categories

urlpatterns = [
    # path('blog_list', BlogList.as_view()),
    path('category_list', get_all_categories),
    # path('blog_detail/<int:pk>/', BlogDetail.as_view()),
]
