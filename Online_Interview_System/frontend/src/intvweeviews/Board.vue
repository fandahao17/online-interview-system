<template>
  <div class="board-window">
    <iframe :src="this.privateurl" width="100%" frameborder="0" height="500px" scrolling="no"></iframe>
  </div>
</template>

<script>
export default {
  name: 'BoardWindow',
  data: function () {
    return {
      privateurl: ''
    }
  },
  mounted: function () {
    this.privateurl = 'http://localhost:8001/boards/' + this.$route.params.roomid
  }
}
</script>

<style scoped>

</style>
