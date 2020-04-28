<template>
  <div class="menu-right">
    <el-button icon="el-icon-search" plain>搜索</el-button>
    <el-button icon="el-icon-plus" type="primary" plain>添加</el-button>
    <el-button icon="el-icon-upload2" type="primary" plain>导入</el-button>
    <el-button icon="el-icon-delete" type="danger" plain>删除</el-button>

    <el-dropdown class="avatar-container">
      <div class="avatar-wrapper">
        <el-avatar icon="el-icon-user-solid" size="medium"></el-avatar>
        <i class="el-icon-caret-bottom"/>
      </div>
      <el-dropdown-menu slot="dropdown">
        <el-dropdown-item>个人中心</el-dropdown-item>
        <el-dropdown-item>选项二</el-dropdown-item>
        <el-dropdown-item divided>退出登录</el-dropdown-item>
      </el-dropdown-menu>
    </el-dropdown>
  </div>
</template>

<script>
export default {
  name: 'RightMenu'
}
</script>

<style scoped>
.el-avatar {
  vertical-align: middle;
}

.menu-right {
  float: right;
  padding-right: 20px;
}

.avatar-container {
  padding-left: 15px;
}
</style>
