<script setup>
import {ref, watch} from "vue";

const props = defineProps(['photo'])
const myPhoto = ref(props.photo)

watch(() => props.photo, newVal => {
  myPhoto.value = newVal
})
</script>

<template>
  <div class="flex justify-center">

  </div>
</template>

<style scoped>

</style>