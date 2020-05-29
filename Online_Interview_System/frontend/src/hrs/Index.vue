<template>
  <div>
    <el-container>
      <el-header><head-menu></head-menu></el-header>
      <el-container>
        <left-side></left-side>
        <div class="vertical-bar"></div>
        <el-main><right-side></right-side></el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import HeadMenu from '@/hrs/HeadMenu'
import LeftSide from '@/hrs/LeftSide'
import RightSide from '@/hrs/RightSide'
export default {
  name: 'HrHome',
  components: {
    HeadMenu,
    LeftSide,
    RightSide
  }
}
</script>

<style scoped>
  .vertical-bar {
    width: 5px;
    height: 700px;
    background: lightgray;
    display: inline-block;
    margin-top: 15px;
    vertical-align: top;
    margin-left: 310px;
  }
  .el-header {
    background-color: #DCDFE6;
    text-align: center;
    line-height: 55px;
  }
  .left-side {
    float: left;
  }
  .el-aside {
    color: #333;
    text-align: center;
    line-height: 200px;
  }
  .el-main {
    color: #333;
    text-align: center;
  }
  body > .el-container {
    margin-bottom: 40px;
  }
</style>
