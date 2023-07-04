import json
import uuid
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from .models import User
from django.core.cache import cache

CACHE_TTL = 3600  # Cache TTL in seconds


def get_unique_int():
    max_limit = 2147483646
    unique_uuid = uuid.uuid4()
    unique_int = int(unique_uuid.int) % max_limit
    return unique_int


class UserDetailView(APIView):

    @staticmethod
    def post(request):
        body = json.loads(request.body)
        username = body.get('username')
        email = body.get('email')
        password = body.get('password')
        encrypted_password = make_password(password)
        user_id = get_unique_int()

        if not username or not email or not password:
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'User already exist'}, status=403)

        user = User.objects.create(user_id=user_id, username=username, email=email, password=encrypted_password)

        cache_key = f'user:{user_id}'
        user_data_json = {
            'user_id': user.user_id,
            'username': user.username,
            'email': user.email,
            'password': user.password
        }
        cache.set(cache_key, user_data_json, CACHE_TTL)
        return JsonResponse({'user_id': user.user_id}, status=200)

    @staticmethod
    def put(request, user_id):
        try:
            user = User.objects.get(user_id=user_id)
            if request.method == 'PUT' or request.method == 'PATCH':
                body = json.loads(request.body)
                username = body.get('username') or user.username
                email = body.get('email') or user.email
                password = ''
                if body.get('password'):
                    password = make_password(body.get('password'))
                else:
                    password = user.password

                User.objects.filter(user_id=user_id).update(username=username, email=email, password=password)
                cache_key = f'user:{user_id}'
                cache.delete(cache_key)
                user_data_json = {
                    'user_id': user_id,
                    'username': username,
                    'email': email,
                    'password': password
                }
                cache.set(cache_key, user_data_json, CACHE_TTL)

                return JsonResponse({
                    'user_id': user_id,
                    'username': username,
                    'email': email
                }, status=200)
            else:
                return JsonResponse({'error': 'Invalid request method'}, status=405)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

    @staticmethod
    def get(request, user_id):
        try:
            if request.method == 'GET':
                cache_key = f'user:{user_id}'
                cached_data = cache.get(cache_key)
                if cached_data is not None:
                    return JsonResponse({
                        'user_id': cached_data['user_id'],
                        'username': cached_data['username'],
                        'email': cached_data['email'],
                    }, status=200)

                user = User.objects.get(user_id=user_id)
                return JsonResponse({
                    'user_id': user_id,
                    'username': user.username,
                    'email': user.email,
                }, status=200)
            else:
                return JsonResponse({'error': 'Invalid request method'}, status=405)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
