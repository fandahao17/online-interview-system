<template>
  <div class="editor-window">
    <editor
      apiKey="hc02du3nr8ugtoouiyovc99dnozuzms34pkgrnckrfpr6mkr"
      plugins="codesample"
      :init="{ height:500 }"
      />
  </div>
</template>

<script>
import Editor from '@tinymce/tinymce-vue'
export default {
  name: 'EditorWindow',
  components: {
    'editor': Editor
  }
}
</script>

<style scoped>

</style>
