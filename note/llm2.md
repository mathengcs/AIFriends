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
