<template>
  <div class="left-top">
    <el-row>
      <el-col :span="20" :offset="10">
        <div class="title">候选人</div>
      </el-col>
    </el-row>
    <el-row :gutter="100">
      <el-col :span="5" :offset="3">
        <el-checkbox v-model="checked1">已安排</el-checkbox>
      </el-col>
      <el-col :span="5" :offset="3">
        <el-checkbox v-model="checked2">未安排</el-checkbox>
      </el-col>
      <el-col :span="5" :offset="3">
        <el-button type="text" class="but">发送邮件</el-button>
      </el-col>
    </el-row>

    <el-row v-for="num in itveNum" v-bind:key="num">
      <el-col :span="18" :offset="9">
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
  name: 'LeftSide',
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
    // 获取所有候选人信息
    axios.get('http://106.14.227.202/api/itve/getall/', {
      headers: {
        'Content-Type': 'application/json'
      }
    }).then(function (response) {
      console.log(response.data)
      console.log('type:', typeof (response.data))
      _this.cardDataAll = response.data
      // _this.checked = Array(_this.cardDataAll.length).fill(false)
    }).catch(function (error) {
      console.log('get itve info error:')
      console.log(error.response)
    })
  }
}
</script>

<style scoped>
.left-top {
  text-align: center;
}

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
  margin-top: 15px;
  margin-right: 5px;
  font-size: 30px;
  line-height: 50px;
  text-align: center;
}

.box-card {
  font-size: 16px;
  width: 400px;
  height: 100px;
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
