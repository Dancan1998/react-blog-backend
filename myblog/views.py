from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import  Category
from .serializers import CategorySerializer
from rest_framework.views import APIView
from django.http import Http404


@api_view(['GET'])
def get_all_categories(request):
    """List all categories"""
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# class BlogList(APIView):
#     """List all blogs ro create a new blog"""
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request, format=None):
#         blogs = Blog.objects.all()
#         serializer = BlogSerializer(blogs, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = BlogSerializer(data=request.data, context={'request': request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class BlogDetail(APIView):
#     permission_classes = [IsAuthenticated]
#     """Retrieve, update or delete a code snippet"""
#
#     def get_object(self, pk):
#         try:
#             return Blog.objects.get(pk=pk)
#         except Blog.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         blog = self.get_object(pk)
#         serializer = BlogSerializer(blog)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         blog = self.get_object(pk)
#         serializer = BlogSerializer(blog, data=request.data,  context={'request': request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         blog = self.get_object(pk)
#         blog.delete()
#         return Response({'success': 'deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
#
#
