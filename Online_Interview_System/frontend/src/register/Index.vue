<template>
  <div id="admin-main">
    <el-container>
      <el-header>
          <head-menu></head-menu>
      </el-header>
      <el-container>
          <el-aside width="500px">Online Interview System</el-aside>
          <div class="vertical-bar"></div>
          <el-main>
              <register-in></register-in>
          </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import HeadMenu from '@/register/HeadMenu'
import RegisterIn from '@/register/RegisterIn'
export default {
  name: 'LogRegHome',
  components: {
    HeadMenu,
    RegisterIn
  }
}
</script>

<style scoped>
  body {
    margin: 0;
  }

  .vertical-bar {
    width: 5px;
    height: 700px;
    background: lightgray;
    display: inline-block;
    margin-top: 15px;
    vertical-align: top;
    margin-right: 29px;
    margin-left: 30px;
  }

  .head-menu {
    float: right;
    padding-right: 20px;
  }

  .el-header {
    background-color: #DCDFE6;
    line-height: 55px;
  }

  .el-aside {
    text-align: center;
    line-height: 500px;
    font-size: 40px;
    color: gray;
  }

  .el-main {
    margin-top: 200px;
    margin-left: 300px;
    float: right;
    color: #333;
  }

  body > .el-container {
    margin-bottom: 40px;
  }
</style>
