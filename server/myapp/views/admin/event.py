from rest_framework.decorators import api_view, authentication_classes
from myapp.auth.authentication import AdminTokenAuthtication
from myapp.handler import APIResponse
from myapp.models import ReadingEvent
from myapp.permission.permission import isDemoAdminUser
from myapp.serializers import ReadingEventSerializer

@api_view(['GET'])
def list_api(request):
    if request.method == 'GET':
        events = ReadingEvent.objects.all().order_by('-create_time')
        serializer = ReadingEventSerializer(events, many=True, context={'request': request})
        return APIResponse(code=0, msg='查询成功', data=serializer.data)

@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def create(request):
    if isDemoAdminUser(request):
        return APIResponse(code=1, msg='演示帐号无法操作')

    serializer = ReadingEventSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return APIResponse(code=0, msg='创建成功', data=serializer.data)
    else:
        print(serializer.errors)
        return APIResponse(code=1, msg='创建失败', data=serializer.errors)

@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def update(request):
    if isDemoAdminUser(request):
        return APIResponse(code=1, msg='演示帐号无法操作')

    try:
        pk = request.GET.get('id', -1)
        event = ReadingEvent.objects.get(pk=pk)
    except ReadingEvent.DoesNotExist:
        return APIResponse(code=1, msg='对象不存在')

    serializer = ReadingEventSerializer(event, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return APIResponse(code=0, msg='更新成功', data=serializer.data)
    else:
        print(serializer.errors)
        return APIResponse(code=1, msg='更新失败', data=serializer.errors)

@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def delete(request):
    if isDemoAdminUser(request):
        return APIResponse(code=1, msg='演示帐号无法操作')

    try:
        ids = request.GET.get('ids')
        ids_arr = ids.split(',')
        ReadingEvent.objects.filter(id__in=ids_arr).delete()
    except ReadingEvent.DoesNotExist:
        return APIResponse(code=1, msg='对象不存在')

    return APIResponse(code=0, msg='删除成功')
