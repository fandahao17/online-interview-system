<template>
  <div>
    <el-row>
      <el-col :span="20" offset="3">
        <div class="title">面试官</div>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="5" offset="5">
        <el-checkbox v-model="checked1">有空闲时间</el-checkbox>
      </el-col>
      <el-col :span="5" offset="5">
        <el-checkbox v-model="checked2">无空闲时间</el-checkbox>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="18" offset="6">
        <el-card class="box-card" shadow="hover">
          <div class="icon"><el-avatar :size="50" :src="circleUrl"></el-avatar></div>
          <div class="item">Name:{{ name1 }}</div>
          <div class="item">Email:{{email1}}</div>
        </el-card>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="18" offset="6">
        <el-card class="box-card" shadow="hover">
          <div class="icon"><el-avatar :size="50" :src="circleUrl"></el-avatar></div>
          <div class="item">Name:{{ name2 }}</div>
          <div class="item">Email:{{email2}}</div>
        </el-card>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="18" offset="6">
        <el-card class="box-card" shadow="hover">
          <div class="icon"><el-avatar :size="50" :src="circleUrl"></el-avatar></div>
          <div class="item">Name:{{ name3 }}</div>
          <div class="item">Email:{{email3}}</div>
        </el-card>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="18" offset="6">
        <el-card class="box-card" shadow="hover">
          <div class="icon"><el-avatar :size="50" :src="circleUrl"></el-avatar></div>
          <div class="item">Name:{{ name4 }}</div>
          <div class="item">Email:{{email4}}</div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: 'RightSide',
  data () {
    return {
      name1: '面试官1',
      email1: 'fir@ustc.edu.cn',
      name2: '面试官2',
      email2: 'sec@ustc.edu.cn',
      name3: '面试官3',
      email3: 'thi@ustc.edu.cn',
      name4: '面试官4',
      email4: 'for@ustc.edu.cn',
      circleUrl: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
      checked1: false,
      checked2: false
    }
  }
}
</script>

<style scoped>
  .el-row {
    margin-bottom: 25px;
    &:last-child {
      margin-bottom: 0;
    }
  }
  .el-col {
    border-radius: 4px;
  }
  .icon {
    float: left;
  }
  .but {
    padding-top: 0;
  }
  .item {
    margin-bottom: 13px;
  }
  .title {
    margin-top: 0px;
    margin-right: 5px;
    font-size: 30px;
    line-height: 50px;
    text-align: center;
  }
  .box-card {
    font-size: 16px;
    width: 400px;
    height: 100px;
    margin-left: 0px;
    border-radius: 20px;
    border-width: 2px;
  }
  .grid-content {
    border-radius: 4px;
    min-height: 26px;
  }
  .row-bg {
    padding: 10px 0;
    background-color: #f9fafc;
  }
</style>
