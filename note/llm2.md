前端匹配任意路径的方式：
```shell
path: '/:pathMatch(.*)*'
```
ctrl+shift+F全局搜索

创建models.ImageField之前需要先安装Pillow包：
```shell
pip install Pillow


python manage.py makemigrations
python manage.py migrate
```


login.py：登录。使用用户名 + 密码登录，在cookie中设置refresh_token，并返回access_token和用户信息
register.py：注册账号。创建账号后返回refresh_token、access_token和用户信息
logout.py：退出登录。删除cookie中的refresh_token
refresh_token.py：使用cookie中的refresh_token刷新access_token

```shell
function closeMenu() {
  const element = document.activeElement
  if (element && element instanceof HTMLElement) element.blur()
}
```
4.5 给前端路由添加守卫
在AIFriends/frontend/src/router/index.js中添加守卫，当前端路径需要登录且当前未登录时，自动跳转到登录页面。

4.6 第一次打开网站时，从云端加载用户信息
在AIFriends/backend/web/views/user/account/目录下实现get_user_info.py
在AIFriends/frontend/src/store/user.js中添加hasPulledUserInfo状态。
在路由守卫中添加hasPulledUserInfo判断。
在AIFriends/frontend/src/App.vue中动态加载用户信息。
信息加载完成后，需要再次判断是否要路由到登录页面，这次用router.replace()，防止用户后退到授权页面。
在导航栏中添加HasPulledUserInfo判断。
4.7 将前端代码打包到后端
在AIFriends/backend/web/urls.py中添加匹配任意路径的路由：
re_path(r'^(?!media/|static/|assets/).*$', index): 在前端任意路径下刷新时，django都自动路由到根路径下，剩下的路由交由前端处理
