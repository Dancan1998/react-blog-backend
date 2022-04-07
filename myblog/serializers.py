from rest_framework import serializers
from .models import Blog, Category
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BlogSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Blog
        fields = ['id', 'timestamp', 'updated', 'blog_image', 'category', 'description', 'author', 'title']

    def create(self, validated_data):
        """
        Create and return a new `Blog` instance, given the validated data.
        """
        # First remove category field from validated data because it points to category
        category = validated_data.pop('category')
        # Was getting orderedDict but as list=> [orderedDict], this way you can not get the single object
        # Loop through the orderedDict and use default dict to convert to regular python dictionary
        for category_orderedDict in category:
            normal_dict = dict(category_orderedDict)
        author_id = self.context['request'].user.id
        author = User.objects.get(pk=author_id)
        blog_instance = Blog.objects.create(author=author, **validated_data)
        # loop through the category and create a new category
        for _ in category:
            cat = Category.objects.get(name=normal_dict['name'])
            blog_instance.category.add(cat)
        return blog_instance

    def create_or_update_categories(self, categories):
        categories_ids = []
        for category in categories:
            cat_instance, created = Category.objects.update_or_create(pk=category.get('id'), defaults=category)
            categories_ids.append(cat_instance.pk)
        return categories_ids

    def update(self, instance, validated_data):
        category = validated_data.pop('category', [])
        instance.category.set(self.create_or_update_categories(category))
        fields = ['description', 'blog_image', 'title']
        for field in fields:
            try:
                setattr(instance, field, validated_data[field])
            except KeyError:  # validated_data may not contain all fields during HTTP PATCH
                pass
        instance.save()
        return instance


