<script setup>
defineProps(["userProfile"])
</script>

<template>
<div v-if="userProfile" class="flex items-center mt-12 gap-8">
  <div class="avatar">
    <div class="w-44 rounded-full">
      <img :src="userProfile.photo" alt="">
    </div>
  </div>
  <div>
    <div class="text">{{ userProfile.username }}</div>
    <div>AIFriends号: {{ userProfile.user_id }}</div>
    <div></div>
  </div>
</div>
</template>

<style scoped>

</style>