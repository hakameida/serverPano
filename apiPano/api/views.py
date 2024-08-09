# views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser,AllowAny
from rest_framework.response import Response
from apiPano.api.serializers import PostSerializer, UserSerializer, PostImageSerializer
from apiPano.models import Post,PostImage
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
import json
class PostPagination(PageNumberPagination):
    page_size = 3  # Adjust the page size as needed

@api_view(['GET'])
@permission_classes([AllowAny])
def viewPosts(request):
    paginator = PostPagination()
    posts = Post.objects.all()
    result_page = paginator.paginate_queryset(posts, request)
    serializer = PostSerializer(result_page, many=True, context={'request': request})
    print(serializer.data)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def viewPost(request, pk):
    try:
        post = Post.objects.get(id=pk)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=404)
    serializer = PostSerializer(post, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['POST'])
def addPost(request):
    title = request.data.get('title')
    content = request.data.get('content')
    images = request.FILES.getlist('images')  # Handle file uploads here

    # Create Post
    post_data = {
        'title': title,
        'content': content
    }
    post_serializer = PostSerializer(data=post_data)

    if post_serializer.is_valid():
        post = post_serializer.save()
        for image in images:
            image_data = {
                'image': image,
            }
            image_serializer = PostImageSerializer(data=image_data)
            if image_serializer.is_valid():
                image_serializer.save(post=post)
            else:
                return Response(image_serializer.errors, status=400)

        return Response(post_serializer.data, status=201)
    else:
        return Response(post_serializer.errors, status=400)
@api_view(['PUT'])
def updatePost(request, pk):
    try:
            post = Post.objects.get(id=pk)
    except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=400)

    title = request.data.get('title')
    content = request.data.get('content')
    new_images = request.FILES.getlist('images')  # Handle file uploads here
    images_to_remove = request.data.get('images_to_remove', [])

    # Convert JSON string to Python list if necessary
    if isinstance(images_to_remove, str):
        images_to_remove = json.loads(images_to_remove)

    # Update Post
    post_data = {
        'title': title,
        'content': content
    }
    post_serializer = PostSerializer(instance=post, data=post_data, partial=True)

    if post_serializer.is_valid():
        post = post_serializer.save()

        # Handle new images
        for image in new_images:
            image_data = {
                'image': image,
            }
            image_serializer = PostImageSerializer(data=image_data)
            if image_serializer.is_valid():
                image_serializer.save(post=post)
            else:
                return Response(image_serializer.errors, status=400)

        # Handle images to remove
        for image_name in images_to_remove:
            images = PostImage.objects.filter(post=post, image__icontains=image_name)
            for image in images:
                image.delete()

        return Response(post_serializer.data, status=200)
    else:
        return Response(post_serializer.errors, status=400)

@api_view(['DELETE'])

def deletePost(request, pk):
    try:
        post = Post.objects.get(id=pk)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=404)

    post.delete()
    return Response({'message': 'Post deleted'}, status=204)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    print(email,password    )
    user = authenticate(request, email=email, password=password)
    print(user)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Send user data including is_admin in the response
        user_data = {
            'email': user.email,
            'is_admin': user.is_admin  # Include is_admin in the response
        }
        
        return Response({
            'access': access_token,
            'refresh': str(refresh),
            'user': user_data
        })
    return Response({'error': 'Invalid credentials'}, status=400)



@api_view(['GET'])
@permission_classes([AllowAny])
def search_posts(request):
    query = request.GET.get('query', '')  # Retrieve 'query' parameter from URL
    if not query:
        return Response([], status=200)  # Return empty list if no query

    # Filter posts based on query
    posts = Post.objects.filter(title__icontains=query) | Post.objects.filter(content__icontains=query)
    
    serializer = PostSerializer(posts, many=True, context={'request': request})
    # print(serializer.data)
    return Response(serializer.data, status=200)