<template>
  <div id="admin-main">
    <el-container>
      <el-header>
        <nav-menu></nav-menu>
      </el-header>
      <el-main>
        <app-main></app-main>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import NavMenu from '@/adminviews/NavMenu'
import AppMain from '@/adminviews/AppMain'

export default {
  name: 'AdminHome',
  components: {
    NavMenu,
    AppMain
  }
}
</script>

<style>
body {
  margin: 0;
}

.el-header {
  background-color: #B3C0D1;
  color: #333;
  line-height: 60px;
  padding: 0;
}

.el-aside {
  background-color: #D3DCE6;
  color: #333;
  text-align: center;
  line-height: 200px;
}

.el-main {
  color: #333;
}

body > .el-container {
  margin-bottom: 40px;
}
</style>
