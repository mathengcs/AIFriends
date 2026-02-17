上节课的补丁：

将导航栏中的创作按钮的路由重置成create-index
在AIFriends/backend/web/views/create/character/remove.py中添加逻辑：
删除角色前，先删除头像和背景图片
1. 实现个人主页
1.1 创建后端
在AIFriends/backend/web/views/create/character/目录下实现：

get_list.py：返回角色列表和作者信息。
然后添加路由。

1.2 实现前端
在AIFriends/frontend/src/views/user/space/components/目录下创建空组件：

UserInfoField.vue：展示个人信息
在AIFriends/frontend/src/components/character/目录下创建空组件：

Character.vue：展示角色卡片
在AIFriends/frontend/src/views/user/space/SpaceIndex.vue中对接后端。

网格布局：可以根据屏幕宽度自动决定每行的元素数量，并将元素均匀排列在屏幕上；当最后一行元素不足时会左对齐。

<div class="grid grid-cols-[repeat(auto-fill,minmax(240px,1fr))] gap-9 mt-12 justify-items-center w-full px-9">
...
</div>
实现渐变色，最下面是黑色40%透明，最上面是完全透明：

bg-linear-to-t from-black/40 to-transparent
流式加载新角色：

<script setup>
const sentinelRef = useTemplateRef('sentinel-ref')
let observer = null

function checkSentinelVisible() {  // 判断哨兵是否能被看到
  if (!sentinelRef.value) return false

  const rect = sentinelRef.value.getBoundingClientRect()
  return rect.top < window.innerHeight && rect.bottom > 0
}

onMounted(async () => {
  await loadMore()  // 加载新元素

  observer = new IntersectionObserver(
    entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          loadMore()
        }
      })
    },
    {root: null, rootMargin: '2px', threshold: 0}
  )

  //监听哨兵元素， 每次哨兵被看到时，都会触发一次
  observer.observe(sentinelRef.value)
})

onBeforeUnmount(() => {
  observer?.disconnect()  // 解绑监听器
})
</script>

<template>
...
<!-- 设置哨兵 -->
<div ref="sentinel-ref" class="h-2"></div>
...
</template>
添加修改角色、删除角色功能。

观察删除角色后，对应的头像和背景图片是否被删除。

观察流式加载。

用其他账号再创建一个角色。

1.3 将前端代码打包到后端
2. 实现首页
2.1 创建后端
在AIFriends/backend/web/views/homepage/目录下实现：

index.py：返回所有角色列表
然后添加路由。

2.2 实现前端
实现AIFriends/frontend/src/views/homepage/HomepageIndex.vue。

2.3 添加搜索功能
在AIFriends/frontend/src/components/navbar/NavBar.vue中添加搜索逻辑：

点击搜索按钮后，打开首页，并将搜索文本添加到url的query参数中。
监听route.query.q，并将最新值赋给searchQuery。这样刷新页面后，搜索文本才能自动填充到搜索框内。
在AIFriends/frontend/src/views/homepage/HomepageIndex.vue中将搜索文本添加到请求中，并且当query参数变化时自动重新获取角色列表。

在AIFriends/backend/web/views/homepage/index.py中实现对搜索的支持。

2.4 将前端代码打包到后端
3. 实现好友页面
3.1 创建后端
3.1.1 创建数据库
在AIFriends/backend/web/models/friend.py中创建Friend数据库。

3.1.2 创建views
在AIFriends/backend/web/views/friend/目录下实现：

get_or_create.py：如果有该好友，则返回；如果没有，则创建并返回
remove.py：删除好友
get_list.py：获取好友列表
3.1.3 实现路由
在AIFriends/backend/web/urls.py中添加路由。

3.2 实现前端
3.2.1 创建聊天界面组件
在AIFriends/frontend/src/components/character/chat_field/目录下创建：

ChatField.vue组件：显示聊天界面
input_field/InputField.vue组件：聊天输入框
character_photo_field/CharacterPhotoField.vue组件：虚拟角色头像
将模态框背景图片设置成聊天背景：

const modalStyle = computed(() => {
  if (props.friend) {
    return {
      backgroundImage: `url(${props.friend.character.background_image})`,
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      backgroundRepeat: 'no-repeat',
    }
  } else {
    return {}
  }
})
然后在AIFriends/frontend/src/components/character/Character.vue中实现：

点击角色卡片后，自动打开聊天界面
3.2.2 实现好友列表页面
实现AIFriends/frontend/src/views/friend/FriendIndex.vue。
实现删除好友功能。
阻止卡片内的点击事件向上传播：@click.top。
character= models.ForeignKey(Character, on_delete=models.CASCADE)：当删除character时，会自动将关联的friend删掉。
3.3 将前端代码打包到后端

