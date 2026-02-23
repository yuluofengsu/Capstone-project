from rest_framework.decorators import api_view, authentication_classes
from myapp.handler import APIResponse
from myapp.models import CommunityPost, ReadingEvent, CommunityComment
from myapp.serializers import CommunityPostSerializer, ReadingEventSerializer, CommunityCommentSerializer
from myapp.auth.authentication import TokenAuthtication

# Post Views
@api_view(['GET'])
@authentication_classes([])
def post_list(request):
    order = request.GET.get("order", 'recent')
    if order == 'recent':
        orderBy = '-create_time'
    else:
        orderBy = '-like_count'
    posts = CommunityPost.objects.all().order_by(orderBy)
    serializer = CommunityPostSerializer(posts, many=True, context={'request': request})
    return APIResponse(code=0, msg='查询成功', data=serializer.data)

@api_view(['POST'])
@authentication_classes([TokenAuthtication])
def post_create(request):
    print("DEBUG: post_create called")
    print("DEBUG: request.user:", request.user)
    print("DEBUG: request.data:", request.data)
    
    data = request.data.copy()
    if request.user and hasattr(request.user, 'id'):
        print("DEBUG: User authenticated, ID:", request.user.id)
        data['user'] = request.user.id
    else:
        print("DEBUG: User NOT authenticated or no ID")
    
    serializer = CommunityPostSerializer(data=data, context={'request': request})
    if serializer.is_valid():
        print("DEBUG: Serializer valid. Saving...")
        try:
            serializer.save()
            print("DEBUG: Saved successfully")
            return APIResponse(code=0, msg='创建成功', data=serializer.data)
        except Exception as e:
            print("DEBUG: Save failed:", e)
            return APIResponse(code=1, msg='保存失败: ' + str(e))
            
    print("Post Create Error:", serializer.errors)
    return APIResponse(code=1, msg='创建失败', data=serializer.errors)

@api_view(['GET'])
@authentication_classes([TokenAuthtication])
def post_detail(request):
    pk = request.GET.get('id')
    try:
        post = CommunityPost.objects.get(pk=pk)
        post.views += 1
        post.save()
        serializer = CommunityPostSerializer(post, context={'request': request})
        return APIResponse(code=0, msg='查询成功', data=serializer.data)
    except CommunityPost.DoesNotExist:
        return APIResponse(code=1, msg='帖子不存在')

@api_view(['POST'])
@authentication_classes([TokenAuthtication])
def post_delete(request):
    pk = request.GET.get('id')
    try:
        post = CommunityPost.objects.get(pk=pk)
        # Check permission: Only author or admin can delete
        is_admin = False
        if request.user and hasattr(request.user, 'role') and str(request.user.role) == '0':
            is_admin = True
            
        if post.user != request.user and not is_admin:
            return APIResponse(code=1, msg='无权删除')
            
        post.delete()
        return APIResponse(code=0, msg='删除成功')
    except CommunityPost.DoesNotExist:
        return APIResponse(code=1, msg='帖子不存在')

@api_view(['POST'])
@authentication_classes([TokenAuthtication])
def post_like(request):
    pk = request.GET.get('id')
    try:
        post = CommunityPost.objects.get(pk=pk)
        user = request.user
        if not user or not hasattr(user, 'id'):
            return APIResponse(code=1, msg='请先登录')
        
        if post.liked_users.filter(id=user.id).exists():
             post.liked_users.remove(user)
             post.like_count -= 1
             post.save()
             return APIResponse(code=0, msg='取消点赞成功')
             
        post.liked_users.add(user)
        post.like_count += 1
        post.save()
        return APIResponse(code=0, msg='点赞成功')
    except CommunityPost.DoesNotExist:
        return APIResponse(code=1, msg='帖子不存在')

# Event Views
@api_view(['GET'])
@authentication_classes([])
def event_list(request):
    events = ReadingEvent.objects.all().order_by('-create_time')
    serializer = ReadingEventSerializer(events, many=True, context={'request': request})
    return APIResponse(code=0, msg='查询成功', data=serializer.data)

@api_view(['GET'])
@authentication_classes([])
def event_detail(request):
    pk = request.GET.get('id')
    try:
        event = ReadingEvent.objects.get(pk=pk)
        serializer = ReadingEventSerializer(event, context={'request': request})
        return APIResponse(code=0, msg='查询成功', data=serializer.data)
    except ReadingEvent.DoesNotExist:
        return APIResponse(code=1, msg='活动不存在')

# Comment Views
@api_view(['GET'])
@authentication_classes([])
def comment_list(request):
    post_id = request.GET.get('postId') or request.GET.get('post_id')
    event_id = request.GET.get('eventId') or request.GET.get('event_id')
    if post_id:
        comments = CommunityComment.objects.filter(post_id=post_id).order_by('-create_time')
    elif event_id:
        comments = CommunityComment.objects.filter(event_id=event_id).order_by('-create_time')
    else:
        return APIResponse(code=1, msg='参数错误')
    
    serializer = CommunityCommentSerializer(comments, many=True, context={'request': request})
    return APIResponse(code=0, msg='查询成功', data=serializer.data)

@api_view(['POST'])
@authentication_classes([TokenAuthtication])
def comment_create(request):
    data = request.data.copy()
    if request.user and hasattr(request.user, 'id'):
        data['user'] = request.user.id

    serializer = CommunityCommentSerializer(data=data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return APIResponse(code=0, msg='创建成功', data=serializer.data)
    return APIResponse(code=1, msg='创建失败', data=serializer.errors)

@api_view(['POST'])
@authentication_classes([TokenAuthtication])
def comment_delete(request):
    ids = request.GET.get('ids')
    if not ids:
        return APIResponse(code=1, msg='参数错误')
    ids_arr = ids.split(',')
    
    # Check permission: Only owner or admin can delete
    user = request.user
    if not user or not hasattr(user, 'id'):
        return APIResponse(code=1, msg='请先登录')
        
    comments = CommunityComment.objects.filter(id__in=ids_arr)
    for comment in comments:
        if comment.user.id != user.id:
            # Check if admin
            if hasattr(user, 'role') and str(user.role) == '0':
                continue
            return APIResponse(code=1, msg='无权删除他人评论')
            
    comments.delete()
    return APIResponse(code=0, msg='删除成功')
