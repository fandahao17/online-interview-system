<template>
  <div>
    <el-container>
      <el-header>
        <intvwer-headmenu></intvwer-headmenu>
      </el-header>
      <el-main>
        <el-row v-for="rn in rowNum" v-bind:key="rn">
          <el-col :span="8" v-for="i in 3" v-bind:key="i">
            <el-card class="box-card" shadow="hover" @click.native="clickCard(((rn-1) * 3) + i - 1)">
              <div slot="header" class="clearfix">
                <span> {{ cardDataAll[(((rn-1) * 3) + i - 1)]['interviewee__name'] }} </span>
                <el-button style="float: right; padding: 3px 0" type="text">查看</el-button>
              </div>
              <el-col :span="18">
                <div class="text item">
                  <span>roomid: </span>
                  {{ cardDataAll[(((rn-1) * 3) + i - 1)]['roomid'] }}
                </div>
                <div class="text item">
                  <span>email: </span>
                  {{ cardDataAll[(((rn-1) * 3) + i - 1)]['interviewee__email'] }}
                </div>
                <div class="text item">
                  <span>mobile: </span>
                  {{ cardDataAll[(((rn-1) * 3) + i - 1)]['interviewee__mobile'] }}
                </div>
                <div class="text item">
                  <span>time: </span>
                  {{ cardDataAll[(((rn-1) * 3) + i - 1)]['time'] }}
                </div>
              </el-col>
            </el-card>
          </el-col>
        </el-row>
        <!-- 最后一行 -->
        <el-row v-if="lastRow > 0">
          <el-col :span="8" v-for="i in lastRow" v-bind:key="i">
            <el-card class="box-card" shadow="hover" @click.native="clickCard(MeetingNum - lastRow + i - 1)">
              <div slot="header" class="clearfix">
                <span> {{ cardDataAll[MeetingNum - lastRow + i - 1]['interviewee__name'] }} </span>
                <el-button style="float: right; padding: 3px 0" type="text">查看</el-button>
              </div>
              <el-col :span="18">
                <div class="text item">
                  <span>roomid: </span>
                  {{ cardDataAll[MeetingNum - lastRow + i - 1]['roomid'] }}
                </div>
                <div class="text item">
                  <span>email: </span>
                  {{ cardDataAll[MeetingNum - lastRow + i - 1]['interviewee__email'] }}
                </div>
                <div class="text item">
                  <span>mobile: </span>
                  {{ cardDataAll[MeetingNum - lastRow + i - 1]['interviewee__mobile'] }}
                </div>
                <div class="text item">
                  <span>time: </span>
                  {{ cardDataAll[MeetingNum - lastRow + i - 1]['time'] }}
                </div>
              </el-col>
            </el-card>
          </el-col>
        </el-row>
      </el-main>
    </el-container>

    <!-- 点击面试卡片弹出的表单 -->
    <el-dialog title="面试信息" :visible.sync="intvwDialogFormVisible">
      <el-form :model="intvwForm">
        <el-form-item label="姓名" :label-width="formLabelWidth">
          <span>{{ intvwForm.name }}</span>
        </el-form-item>
        <el-form-item label="性别" :label-width="formLabelWidth">
          <span>{{ intvwForm.sex }}</span>
        </el-form-item>
        <el-form-item label="email" :label-width="formLabelWidth">
          <span>{{ intvwForm.email }}</span>
        </el-form-item>
        <el-form-item label="学历" :label-width="formLabelWidth">
          <span>{{ intvwForm.education }}</span>
        </el-form-item>
        <el-form-item label="面试岗位" :label-width="formLabelWidth">
          <span>{{ intvwForm.position }}</span>
        </el-form-item>
        <el-form-item label="简历" :label-width="formLabelWidth">
          <span>{{ intvwForm.resume }}</span>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import IntvwerHeadmenu from '@/intvwerviews/HeadMenu'
import axios from 'axios'

export default {
  name: 'ScheduleView',
  components: {
    IntvwerHeadmenu
  },
  data: function () {
    return {
      // MeetingNum: 11, // 从 API 请求到的 interview 的数量（用meetingnum代替）
      intvwDialogFormVisible: false,
      intvwForm: { // 弹出表单的内容
        name: 'default',
        sex: '男',
        email: 'default@default.com',
        education: '本科',
        position: '开发',
        resume: '简历'
      },
      formLabelWidth: '120px', // 弹出表单的宽度
      cardDataAll: [{}] // 返回的面试信息
    }
  },
  computed: {
    MeetingNum: function () {
      return this.cardDataAll.length
    },
    rowNum: function () { // 除最后一行外有多少行
      return Math.floor(this.MeetingNum / 3)
    },
    lastRow: function () { // 最后一行有多少个元素
      return this.MeetingNum - 3 * this.rowNum
    }
  },
  methods: {
    clickCard: function () {
      this.intvwDialogFormVisible = true
    },
    getMeetingInfo: function (_this) {
      let email = localStorage.getItem('email')
      console.log('emali' + email)
      axios.get('http://106.14.227.202/api/itvr/getitves/' + email + '/', {
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(function (response) {
        console.log(response.data)
        console.log('type:', typeof (response.data))
        _this.cardDataAll = response.data
      }).catch(function (error) {
        console.log('get meeting info error:')
        console.log(error.response)
      })
    }
  },
  mounted: function () {
    this.getMeetingInfo(this)
  }
}
</script>

<style scoped>
  .el-header {
    background-color: #DCDFE6;
    text-align: left;
    line-height: 55px;
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

  .box-card {
    width: 400px;
    height: 225px;
    margin-left: 40px;
    border-radius: 20px;
    border-width: 2px;
  }

  .el-row {
    margin-bottom: 20px;
  }
  .el-col {
    border-radius: 4px;
    height: 100%;
  }
</style>
