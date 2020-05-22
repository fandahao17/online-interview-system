<template>
  <div>
    <div class="tag">首页</div>
    <div class="menu-right">
      <el-menu default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect2">
        <el-menu-item index="1">登陆</el-menu-item>
        <el-menu-item index="2">注册</el-menu-item>
        <el-menu-item class="el-icon-user-solid" index="3"> 未登陆</el-menu-item>
      </el-menu>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HeadMenu',
  data: function () {
    return {
      activeIndex: '1'
    }
  },
  methods: {
    handleSelect1: function (key, keyPath) {
      console.log(key, keyPath)
    },
    handleSelect2: function (key, keyPath) {
      console.log(key, keyPath)
    }
  }
}
</script>

<style scoped>
  .tag {
    float: left;
    padding-left: 20px;
    color: gray;
  }
  .el-menu {
    background-color: #DCDFE6;
  }
  .menu-right {
    float: right;
    padding-right: 20px;
  }
  .menu-left {
    float: left;
    padding-right: 20px;
  }
</style>
