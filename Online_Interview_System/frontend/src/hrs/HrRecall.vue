<template>
  <div>
    <el-container>
      <el-header><head-menu></head-menu></el-header>
      <el-main>
        <div>
          <el-button type="primary" plain size="medium" @click="clickHire">录用</el-button>
          <el-button type="primary" plain size="medium" @click="clickReject">拒绝</el-button>
          <el-button type="primary" plain size="medium" @click="clickReset">重置</el-button>
        </div>
        <el-table
          v-if="isDataRecevie"
          :data="posterData"
          style="width: 100%"
          @selection-change="handleSelectionChange">
          <el-table-column
            type="selection"
            width="55">
          </el-table-column>
          <el-table-column
            prop="interviewee__name"
            label="候选人"
            width="180">
          </el-table-column>
          <el-table-column
            prop="tester__name"
            label="面试官"
            width="180">
          </el-table-column>
          <el-table-column
            prop="score"
            label="评分"
            width="180">
          </el-table-column>
          <el-table-column
            prop="time"
            label="时间"
            width="180">
          </el-table-column>
          <el-table-column
            prop="interviewee__status"
            label="状态"
            width="180">
          </el-table-column>
          <el-table-column
            label="观看面试回放">
            <template slot-scope="scope">
              <el-button @click="clickVideoList(scope.row)">选择观看视频</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-main>
    </el-container>
    <el-dialog title="选择视频" :visible.sync="videoListVisible">
      <div v-for= "(item , i) in videolist" v-bind:key="i">
        <el-button @click="watchVideo(item)">{{item}}</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import HeadMenu from '@/hrs/HeadMenu'
import axios from 'axios'

export default {
  name: 'HrRecall',
  components: {
    HeadMenu
  },
  data: function () {
    return {
      multipleSelection: [],
      recevieData: '',
      isDataRecevie: false,
      status: ['未分配', '拒绝', '录用'],
      time: ['早上', '中午', '晚上'],
      postData: {
        rooms: [],
        status: ''
      },
      videoListVisible: false,
      videolist: []
    }
  },
  computed: {
    posterData: function () {
      return this.recevieData
    }
  },
  methods: {
    handleSelectionChange: function (val) {
      this.multipleSelection = val
      console.log('multipleSelection = ', this.multipleSelection)
    },
    processDecide: function (Decide) {
      this.postData.rooms = []
      this.postData.status = ''
      for (let item in this.multipleSelection) {
        this.postData.rooms.push(this.multipleSelection[item].roomid)
      }
      this.postData.status = Decide
    },
    clickVideoList: function (row) {
      let _this = this
      console.log(row.roomid)
      _this.videoListVisible = true
      axios.get('http://106.14.227.202/api/room/videolist/' + row.roomid + '/', {
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(function (response) {
        console.log(response.data)
        _this.videolist = response.data.videolist
      }).catch(function (error) {
        console.log(error)
      })
    },
    watchVideo: function (videoname) {
      console.log(videoname)
    },
    clickHire: function () {
      console.log('clickHire')
      this.processDecide(2)
      console.log(this.postData)
      axios.post('http://106.14.227.202/api/room/decide/', this.postData, {
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(function (response) {
        this.VideoList = response.data.videolist
      }).catch(function (error) {
        console.log(error)
      })
      this.getReview()
    },
    clickReject: function () {
      console.log('clickReject')
      this.processDecide(1)
      console.log(this.postData)
      axios.post('http://106.14.227.202/api/room/decide/', this.postData, {
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(function (response) {
        console.log(response.data)
      }).catch(function (error) {
        console.log(error)
      })
      this.getReview()
    },
    clickReset: function () {
      console.log('clickReject')
      this.processDecide(0)
      console.log(this.postData)
      axios.post('http://106.14.227.202/api/room/decide/', this.postData, {
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(function (response) {
        console.log(response.data)
      }).catch(function (error) {
        console.log(error)
      })
      this.getReview()
    },
    clickNextRound: function () {
      console.log('clickNextRound')
    },
    getReview: function () {
      let _this = this
      _this.isDataRecevie = false
      axios.get('http://106.14.227.202/api/room/review/', {
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(function (response) {
        console.log(response.data)
        _this.recevieData = response.data
        _this.processData()
        _this.isDataRecevie = true
      }).catch(function (error) {
        console.log(error)
      })
    },
    processData: function () {
      let _this = this
      for (let item in _this.recevieData) {
        _this.recevieData[item].time = _this.time[_this.recevieData[item].time]
        _this.recevieData[item].interviewee__status = _this.status[_this.recevieData[item].interviewee__status]
      }
    }
  },
  created: function () {
    this.getReview()
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
</style>
