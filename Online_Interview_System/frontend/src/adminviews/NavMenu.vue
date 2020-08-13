<template>
  <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal"
    @select="handleSelect">
    <el-menu-item index="itve">候选人管理</el-menu-item>
    <el-menu-item index="itvr">面试官管理</el-menu-item>
    <el-menu-item index="hr">HR 管理</el-menu-item>
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
      activeIndex: 'itve'
    }
  },
  methods: {
    handleSelect: function (key, keyPath) {
      console.log(key, keyPath) // key 是 string 类型
      console.log('activeIndex', this.activeIndex)
      this.$eventHub.$emit('menu-change', key)
    }
  }
}
</script>

<style scoped>

</style>
