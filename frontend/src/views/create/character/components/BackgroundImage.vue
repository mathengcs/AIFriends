<script setup>

import {ref, watch} from "vue";

const props = defineProps(['backgroundImage'])
const myBackgroundImage = ref(props.backgroundImage)

watch(() => props.backgroundImage, (newVal) => {
  myBackgroundImage.value = newVal
})

defineExpose({
  myBackgroundImage,
})
</script>

<template>

</template>

<style scoped>

</style>