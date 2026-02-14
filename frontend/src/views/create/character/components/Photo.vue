<script setup>

import {ref, useTemplateRef, watch} from "vue";
import CameraIcon from "@/views/user/profile/components/icons/CameraIcon.vue";

const props = defineProps(['photo'])
const myPhoto = ref(props.photo)

watch(() => props.photo, (newVal) => {
  myPhoto.value = newVal
})

const fileInputRef = useTemplateRef('file-input-ref')
const modalRef = useTemplateRef('modal-ref')
async function openModal(photo) {
  modalRef.value.showModal()
}

function onFileChange(e) {
  const file = e.target.files[0]
  e.target.value = ''
  if (!file) return

  const reader = new FileReader()

  reader.onload = () => {
    openModal(reader.result)
  }
  reader.readAsDataURL(file)

}

defineExpose({
  myPhoto,
})
</script>

<template>
  <div class="flex justify-center">
    <div class="avatar relative">
      <div v-if="myPhoto" class="w-28 rounded-full">
        <img :src="myPhoto" alt="">
      </div>
      <div v-else class="w-28 h-28 rounded-full bg-base-300"></div>
      <div @click="fileInputRef.click()"
           class="w-28 h-28 rounded-full bg-black/20 absolute left-0 top-0 flex justify-center items-center cursor-pointer">
        <CameraIcon/>
      </div>
    </div>
    <input ref="file-input-ref" type="file" class="hidden" accept="image/*" @change="onFileChange">
    <dialog ref="modal-ref" class="modal">
      <div class="modal-box transition-none">
        <button class="btn btn-ghost btn-sm btn-circle absolute">✕</button>
      </div>
    </dialog>
  </div>
</template>

<style scoped>

</style>