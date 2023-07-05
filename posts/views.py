from django.http import JsonResponse
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Post
from users.models import User
import json
import uuid
from django.core.cache import cache

CACHE_TTL = 3600  # Cache TTL in seconds


def get_unique_int():
    max_limit = 2147483646
    unique_uuid = uuid.uuid4()
    unique_int = int(unique_uuid.int) % max_limit
    return unique_int


class PostView(APIView):

    @staticmethod
    def get(request, post_id):
        try:
            cache_key = f'post:{post_id}'
            cached_data = cache.get(cache_key)
            if cached_data is not None:
                return JsonResponse({
                    'user_id': cached_data['user_id'],
                    'post_id': cached_data['post_id'],
                    'content': cached_data['content'],
                }, status=200)
            post = get_object_or_404(Post, post_id=post_id)
            return JsonResponse(
                {"post_id": post.post_id, "user_id": post.user_id, "content": post.content,
                 "post_date": post.post_date},
                status=200
            )

            cache_key = f'post:{user_id}'
            post_data_json = {
                'user_id': post.user_id,
                'post_id': post.post_id,
                'content': post.content,
                'post_date': post.post_date
            }
            cache.set(cache_key, post_data_json, CACHE_TTL)

        except Post.DoesNotExist:
            return JsonResponse({'error': 'post not found'}, status=404)

    @staticmethod
    def put(request, post_id):
        try:
            post = get_object_or_404(Post, post_id=post_id)
            body = json.loads(request.body)
            content = body.get("content") or post.content

            Post.objects.filter(post_id=post_id).update(content=content)
            cache_key = f'post:{post_id}'
            cache.delete(cache_key)
            post_data_json = {
                'user_id': post.user_id,
                'post_id': post.post_id,
                'content': content,
                'post_date': post.post_date
            }
            cache.set(cache_key, post_data_json, CACHE_TTL)

            return JsonResponse({"post_id": post_id, "content": content}, status=200)
        except Post.DoesNotExist:
            return JsonResponse({'error': 'post not found'}, status=404)

    @staticmethod
    def delete(request, post_id):
        try:
            post = get_object_or_404(Post, post_id=post_id)
            cache_key = f'post:{post_id}'
            cache.delete(cache_key)
            post.delete()
            return JsonResponse({"message": "Post deleted."}, status=200)
        except Post.DoesNotExist:
            return JsonResponse({'error': 'Post not found'}, status=404)


class PostsView(APIView):

    @staticmethod
    def post(request):
        body = json.loads(request.body)
        user_id = body.get("user_id")
        content = body.get("content")
        post_id = get_unique_int()

        user = User.objects.get(user_id=user_id)
        if user is None:
            return JsonResponse({"error": "User is not authorize to add post."}, status=401)

        if not user_id or not content:
            return JsonResponse({"error": "User ID and content are required."}, status=400)

        cache_key = f'post:{post_id}'
        post_data_json = {
            'user_id': user_id,
            'post_id': post_id,
            'content': content
        }
        cache.set(cache_key, post_data_json, CACHE_TTL)

        post = Post.objects.create(user_id=user_id, post_id=post_id, content=content)
        return JsonResponse({"post_id": post.post_id}, status=200)

    @staticmethod
    def get(request):
        posts = Post.objects.all()
        data = [{"post_id": post.post_id, "user_id": post.user_id, "content": post.content} for post in posts]
        return JsonResponse(data, safe=False)

