<script setup>

import Photo from "@/views/create/character/components/Photo.vue";
import Name from "@/views/create/character/components/Name.vue";
import BackgroundImage from "@/views/create/character/components/BackgroundImage.vue";
import Profile from "@/views/create/character/components/Profile.vue";
</script>

<template>
  <div class="flex justify-center">
    <div class="card w-120 bg-base-200 shadow-sm mt-16">
      <div class="card-body">
        <h3 class="text-lg font-bold my-4">创建角色</h3>
        <photo />
        <Name />
        <Profile />
        <BackgroundImage />
        <div class="flex justify-center">
          <button class="btn btn-neutral w-60 mt-2">创建</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>