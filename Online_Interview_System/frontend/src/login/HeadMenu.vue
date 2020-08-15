<template>
  <div>
    <div class="tag">首页</div>
    <div class="menu-right">
      <el-menu default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect" router>
        <el-menu-item index="/login">登录</el-menu-item>
        <el-menu-item index="/register">注册</el-menu-item>
        <el-menu-item class="el-icon-user-solid" index="/login"> 未登录</el-menu-item>
      </el-menu>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HeadMenu',
  data: function () {
    return {
      activeIndex: '/login'
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
