<template>
  <div>
    <el-row>
      <el-col :span="20" :offset="3">
        <div class="title">面试官</div>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="5" :offset="5">
        <el-checkbox v-model="checked1">有空闲时间</el-checkbox>
      </el-col>
      <el-col :span="5" :offset="5">
        <el-checkbox v-model="checked2">无空闲时间</el-checkbox>
      </el-col>
    </el-row>
    <el-row v-for="num in itveNum" v-bind:key="num">
      <el-col :span="18" :offset="6">
        <el-card class="box-card" shadow="hover">
          <div class="icon"><el-avatar :size="50" :src="circleUrl"></el-avatar></div>
          <div class="item">Name: {{ cardDataAll[num-1]['name'] }}</div>
          <div class="item">Email: {{ cardDataAll[num-1]['email'] }}</div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'RightSide',
  data: function () {
    return {
      circleUrl: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
      checked1: false,
      checked2: false,
      cardDataAll: [{}]
    }
  },
  computed: {
    itveNum: function () {
      return this.cardDataAll.length
    }
  },
  mounted: function () {
    let _this = this
    axios.get('http://106.14.227.202/api/itvr/getall/', {
      headers: {
        'Content-Type': 'application/json'
      }
    }).then(function (response) {
      console.log(response.data)
      console.log('type:', typeof (response.data))
      _this.cardDataAll = response.data
      // _this.checked = Array(_this.cardDataAll.length).fill(false)
    }).catch(function (error) {
      console.log('get itvr info error:')
      console.log(error.response)
    })
  }
}
</script>

<style scoped>
  .el-row {
    margin-bottom: 25px;
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
