from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from myapp.models import User


# 后台接口认证
class AdminTokenAuthtication(BaseAuthentication):
    def authenticate(self, request):
        adminToken = request.META.get("HTTP_ADMINTOKEN")
        print("检查adminToken==>" + str(adminToken))
        
        # 如果没有adminToken，则跳过此认证，交给下一个认证类或视图
        if not adminToken:
            return None
            
        users = User.objects.filter(admin_token=adminToken)
        """
        判定条件：
            1. 传了adminToken 
            2. 查到了该帐号 
            3. 该帐号是管理员或演示帐号
        """
        if users.count() == 0 or users[0].role == '2':
            raise exceptions.AuthenticationFailed("AUTH_FAIL_END")
        else:
            print('adminToken验证通过')
            return (users[0], adminToken)


# 前台接口认证
class TokenAuthtication(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get("HTTP_TOKEN")
        print("检查token==>" + str(token))
        # print("Headers keys:", [k for k in request.META.keys() if k.startswith('HTTP')])
        
        # 如果没有token，则跳过此认证
        if not token:
            return None
            
        users = User.objects.filter(token=token)
        print("查找到用户数量:", users.count())
        """
        判定条件：
            1. 传了token 
            2. 查到了该帐号 
        """
        if users.count() == 0:
            print("前端认证失败: Token无效或用户不存在")
            raise exceptions.AuthenticationFailed("AUTH_FAIL_FRONT")
        
        user = users[0]
        print(f"Token验证通过, 用户: {user.username}, 角色: {user.role}")
        return (user, token)
