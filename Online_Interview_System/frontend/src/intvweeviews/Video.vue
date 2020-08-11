<template>
  <div class="video-window">
    这是视频的窗口 {{ $route.params.roomid }}
  </div>
</template>

<script>
export default {
  name: 'VideoWindow',
  props: ['roomInfo']
}
</script>

<style scoped>
.video-window {
  height: 200px;
  line-height: 200px;
}
</style>
