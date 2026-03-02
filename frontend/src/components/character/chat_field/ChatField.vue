<script setup>
import {useTemplateRef} from "vue";

const props = defineProps(['friend'])
const modalRef = useTemplateRef('modal-ref')


function showModal() {
  modalRef.value.showModal()
}

defineExpose({
  showModal,
})
</script>

<template>
  <dialog ref="modal-ref" class="modal">
    <div class="modal-box w-90 h-150">
      <button @click="modalRef.close()" class="btn btn-sm btn-circle btn-ghost bg-transparent ">
        ✕
      </button>
    </div>
  </dialog>
</template>

<style scoped>

</style>