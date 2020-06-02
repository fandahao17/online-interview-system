<template>
  <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal"
    @select="handleSelect">
    <el-menu-item index="1">候选人管理</el-menu-item>
    <el-menu-item index="2">面试官管理</el-menu-item>
    <el-menu-item index="3">HR 管理</el-menu-item>
    <right-menu></right-menu>
  </el-menu>
</template>

<script>
import RightMenu from '@/adminviews/RightMenu'

export default {
  name: 'NavMenu',
  components: {
    RightMenu
  },
  data: function () {
    return {
      activeIndex: '1'
    }
  },
  methods: {
    handleSelect: function (key, keyPath) {
      console.log(key, keyPath)
    }
  }
}
</script>

<style scoped>

</style>
