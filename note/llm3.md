```shell
<script setup>
...
import Croppie from 'croppie'
import 'croppie/croppie.css'
...

const croppieRef = useTemplateRef('croppie-ref')
let croppie = null

if (!croppie) {
  croppie = new Croppie(croppieRef.value, {  // 创建croppie对象
    viewport: {width: 200, height: 200, type: 'square'},
    boundary: {width: 300, height: 300},
    enableOrientation: true,
    enforceBoundary: true,
  })
}

croppie.bind({  // 绑定裁剪图片
  url: photo,
})

myPhoto.value = await croppie.result({  // 获取裁剪结果
  type: 'base64',
  size: 'viewport',
})

onBeforeUnmount(() => {  // 释放croppie对象，防止内存泄漏
  croppie?.destroy()
})
</script>

<template>
...
<!-- 定义croppie绑定的标签 -->
<div ref="croppie-ref" class="flex flex-col justify-center my-4"></div>
...
</template>
```