<template>
  <div>
    <el-container>
      <el-header><head-menu></head-menu></el-header>
      <el-main>
        <el-row v-for="rn in rowNum" v-bind:key="rn">
          <el-col :span="8" v-for="i in 3" v-bind:key="i">
            <el-card class="box-card" shadow="hover">
              <div slot="header" class="clearfix">
                <span>面试{{ (((rn-1) * 3) + i) }}</span>
                <el-button style="float: right; padding: 3px 0" type="text" round @click="$router.push('/hr/' + roomdata[(((rn-1) * 3) + i)-1].roomid + '/')">进入房间</el-button>
              </div>
              <div v-if='getComplete'>
                {{'候选人邮箱: ' + roomdata[(((rn-1) * 3) + i) - 1].interviewee__email }}<br>
                {{'房间id: ' + roomdata[(((rn-1) * 3) + i)-1].roomid }}<br>
                {{'面试官邮箱: ' + roomdata[(((rn-1) * 3) + i) - 1].tester__email }}<br>
                {{'时间: ' + time[roomdata[(((rn-1) * 3) + i) - 1].time]}}
              </div>
            </el-card>
          </el-col>
        </el-row>
        <!-- 最后一行 -->
        <el-row v-if="lastRow > 0">
          <el-col :span="8" v-for="i in lastRow" v-bind:key="i">
            <el-card class="box-card" shadow="hover">
              <div slot="header" class="clearfix">
                <span>面试{{ intvwNum - lastRow + i }}</span>
                <el-button style="float: right; padding: 3px 0" type="text" round @click="$router.push('/hr/' + roomdata[intvwNum - lastRow + i - 1].roomid + '/')">进入房间</el-button>
              </div>
              <div v-if='getComplete'>
                {{'候选人邮箱: ' + roomdata[intvwNum - lastRow + i - 1].interviewee__email }}<br>
                {{'房间id: ' + roomdata[intvwNum - lastRow + i - 1].roomid }}<br>
                {{'面试官邮箱: ' + roomdata[intvwNum - lastRow + i - 1].tester__email }}<br>
                {{'时间: ' + time[roomdata[intvwNum - lastRow + i - 1].time]}}
              </div>
            </el-card>
          </el-col>
        </el-row>
      </el-main>
    </el-container>
  </div>
</template>

<script>
// note!
// 列表内容应该换成 面试官、面试者、面试时间范围
import HeadMenu from '@/hrs/HeadMenu'
import axios from 'axios'

export default {
  name: 'HrWatch',
  components: {
    HeadMenu
  },
  data: function () {
    return {
      intvwNum: 11, // 从 API 请求到的 interview 的数量
      roomdata: [],
      getComplete: false,
      time: ['早上', '中午', '晚上']
    }
  },
  computed: {
    rowNum: function () { // 除最后一行外有多少行
      return Math.floor(this.intvwNum / 3)
    },
    lastRow: function () { // 最后一行有多少个元素
      return this.intvwNum - 3 * this.rowNum
    }
  },
  methods: {
    getRoominfo: function () {
      let _this = this
      axios.get('http://106.14.227.202/api/room/getun/', {
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(function (response) {
        console.log(response.data)
        console.log('type:', typeof (response.data))
        _this.intvwNum = response.data.length
        _this.roomdata = response.data
        _this.getComplete = true
      }).catch(function (error) {
        console.log('get problems detail error:')
        console.log(error)
      })
    }
  },
  created: function () {
    this.getRoominfo()
  }
}
</script>

<style scoped>
  .el-header {
    background-color: #DCDFE6;
    text-align: center;
    line-height: 55px;
  }

  .el-main {
    color: #333;
  }

  body > .el-container {
    margin-bottom: 40px;
  }

  .box-card {
    width: 400px;
    height: 200px;
    margin-left: 40px;
    border-radius: 20px;
    border-width: 2px;
  }

  .text {
    font-size: 14px;
  }

  .item {
    margin-bottom: 18px;
  }

  .clearfix:before,
  .clearfix:after {
    display: table;
    content: "";
  }
  .clearfix:after {
    clear: both
  }

  .el-row {
    margin-bottom: 20px;
  }

  .el-col {
    border-radius: 4px;
    height: 100%;
  }
</style>
