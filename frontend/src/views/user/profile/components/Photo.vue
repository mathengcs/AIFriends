<script setup>
import {ref, useTemplateRef, watch} from "vue";
import CameraIcon from "@/views/user/profile/components/icons/CameraIcon.vue";

const props = defineProps(['photo'])
const myPhoto = ref(props.photo)



watch(() => props.photo, newVal => {
  myPhoto.value = newVal
})

const fileInputRef = useTemplateRef('file-input-ref')
const modalRef = useTemplateRef('modal-ref')

async function openModal() {
  modalRef.value.showModal()

}

function onFileChange(e) {
  const file = e.target.files[0]
  e.target.value = ''
  if (!file) return

  const reader = new FileReader()
  reader.onload = () => {
    openModel(reader.result)
  }
  reader.readAsDataURL(file)
}

</script>

<template>
  <div class="flex justify-center">
    <div class="avatar" relative="">
      <div class="w-28 rounded-full">
        <img :src="myPhoto" alt="" >
      </div>
      <div @click="fileInputRef.click()" class="absolute left-0 top-0 w-28 h-28 flex justify-center items-center bg-black/20 rounded-full cursor-pointer">
        <CameraIcon />
      </div>
    </div>
  </div>
  <input ref="file-input-ref" type="file" accept="image/*" class="hidden">

  <dialog ref="modal-ref" class="modal">
    <div class="modal-box">

    </div>
  </dialog>
</template>

<style scoped>

</style>