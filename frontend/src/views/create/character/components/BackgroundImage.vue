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
  <fieldset class="fieldset">
    <label for="" class="label text-base"></label>
  </fieldset>
</template>

<style scoped>

</style>