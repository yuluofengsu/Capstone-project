# Create your views here.
from rest_framework.decorators import api_view, authentication_classes

from myapp.auth.authentication import AdminTokenAuthtication
from myapp.handler import APIResponse
from myapp.models import Comment, CommunityComment
from myapp.permission.permission import isDemoAdminUser
from myapp.serializers import CommentSerializer, CommunityCommentSerializer


@api_view(['GET'])
def list_api(request):
    if request.method == 'GET':
        type_filter = request.GET.get('type', 'all') # book, post, event
        
        all_data = []
        
        # Book Comments
        if type_filter == 'all' or type_filter == 'book':
            comments = Comment.objects.select_related("book").all().order_by('-comment_time')
            comment_serializer = CommentSerializer(comments, many=True)
            comment_data = comment_serializer.data
            for item in comment_data:
                item['id'] = 'book_' + str(item['id'])
                item['type'] = 'book'
            all_data.extend(comment_data)

        # Community Comments
        if type_filter == 'all' or type_filter == 'post' or type_filter == 'event':
            query = CommunityComment.objects.select_related("post", "event")
            if type_filter == 'post':
                query = query.filter(post__isnull=False)
            elif type_filter == 'event':
                query = query.filter(event__isnull=False)
            
            community_comments = query.all().order_by('-create_time')
            community_serializer = CommunityCommentSerializer(community_comments, many=True)
            community_data = community_serializer.data
            for item in community_data:
                item['id'] = 'community_' + str(item['id'])
                # Distinguish subtype for clarity, though it's still 'community' table
                if item.get('post'):
                    item['type'] = 'post'
                    item['title'] = item.get('post_title', '')
                elif item.get('event'):
                    item['type'] = 'event'
                    item['title'] = item.get('event_title', '')
                else:
                    item['type'] = 'community' # fallback
                    item['title'] = ''
                
                # Use create_time as comment_time for sorting/display consistency
                item['comment_time'] = item['create_time']
            all_data.extend(community_data)

        # Sort by comment_time desc
        all_data.sort(key=lambda x: x['comment_time'], reverse=True)

        return APIResponse(code=0, msg='查询成功', data=all_data)


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def create(request):
    if isDemoAdminUser(request):
        return APIResponse(code=1, msg='演示帐号无法操作')

    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return APIResponse(code=0, msg='创建成功', data=serializer.data)
    else:
        print(serializer.errors)

    return APIResponse(code=1, msg='创建失败')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def update(request):
    if isDemoAdminUser(request):
        return APIResponse(code=1, msg='演示帐号无法操作')

    try:
        pk = request.GET.get('id', -1)
        # Check type or try both?
        # Update usually takes simple ID in current frontend.
        # But wait, frontend "Edit" might not be supported for community comments yet or needs adjustment.
        # The user only asked for "Can see comments" and "Title".
        # Let's assume Update is for Book Comments primarily unless requested.
        # If pk starts with 'book_', strip it.
        if str(pk).startswith('book_'):
            real_id = pk.split('_')[1]
            comments = Comment.objects.get(pk=real_id)
            serializer = CommentSerializer(comments, data=request.data)
        elif str(pk).startswith('community_'):
            real_id = pk.split('_')[1]
            comments = CommunityComment.objects.get(pk=real_id)
            serializer = CommunityCommentSerializer(comments, data=request.data)
        else:
            # Fallback for old calls
            comments = Comment.objects.get(pk=pk)
            serializer = CommentSerializer(comments, data=request.data)

    except (Comment.DoesNotExist, CommunityComment.DoesNotExist):
        return APIResponse(code=1, msg='对象不存在')

    if serializer.is_valid():
        serializer.save()
        return APIResponse(code=0, msg='更新成功', data=serializer.data)

    return APIResponse(code=1, msg='更新失败')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def delete(request):
    if isDemoAdminUser(request):
        return APIResponse(code=1, msg='演示帐号无法操作')

    try:
        ids = request.GET.get('ids')
        ids_arr = ids.split(',')
        
        book_ids = []
        community_ids = []
        
        for id_str in ids_arr:
            if id_str.startswith('book_'):
                book_ids.append(id_str.split('_')[1])
            elif id_str.startswith('community_'):
                community_ids.append(id_str.split('_')[1])
            else:
                # Fallback
                book_ids.append(id_str)

        if book_ids:
            Comment.objects.filter(id__in=book_ids).delete()
        
        if community_ids:
            CommunityComment.objects.filter(id__in=community_ids).delete()
            
    except Exception as e:
        return APIResponse(code=1, msg='删除失败')

    return APIResponse(code=0, msg='删除成功')
