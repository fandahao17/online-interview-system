<template>
  <div>
    <el-container>
      <el-header>
        <intvwer-headmenu></intvwer-headmenu>
      </el-header>
      <el-main>
        <el-col :span="12">
          <el-col :span="23">
            <h1>选择空闲时间段</h1>
            <el-form ref="timeForm" :model="timeForm" label-width="140px">
              <el-form-item label="日期">
                <el-date-picker
                  v-model="timeForm.freeDate"
                  type="date"
                  placeholder="选择日期"
                  :picker-options="pickerOptions">
                </el-date-picker>
              </el-form-item>
              <el-form-item label="空闲时间段">
                <el-checkbox-group v-model="checkList">
                  <el-checkbox label="上午"></el-checkbox>
                  <el-checkbox label="下午"></el-checkbox>
                  <el-checkbox label="晚上"></el-checkbox>
                </el-checkbox-group>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="submitFreeTime">提交</el-button>
              </el-form-item>
            </el-form>
          </el-col>
          <el-col :span="1"><div class="vertical-bar"></div></el-col>
        </el-col>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import axios from 'axios'
import IntvwerHeadmenu from '@/intvwerviews/HeadMenu'

export default {
  name: 'IntvwerHome',
  components: {
    IntvwerHeadmenu
  },
  data: function () {
    return {
      freeDate: '',
      freeTime: [],
      checkList: [],
      pickerOptions: {
        disabledDate (time) { // 只能选择 30 天之内的日期
          return (time.getTime() < (Date.now() - 86400000)) || (time.getTime() > (Date.now() + 2592000000))
        }
      },
      timeForm: {
        freeDate: '',
        freeTime: [new Date(), new Date()]
      },
      treeData: [{
        id: 1,
        label: '一级 1',
        children: [{
          id: 4,
          label: '二级 1-1',
          children: [{
            id: 9,
            label: '三级 1-1-1'
          }, {
            id: 10,
            label: '三级 1-1-2'
          }]
        }]
      }, {
        id: 2,
        label: '一级 2',
        children: [{
          id: 5,
          label: '二级 2-1'
        }, {
          id: 6,
          label: '二级 2-2'
        }]
      }, {
        id: 3,
        label: '一级 3',
        children: [{
          id: 7,
          label: '二级 3-1'
        }, {
          id: 8,
          label: '二级 3-2'
        }]
      }]
    }
  }, /*
  created () {
    var identity = localStorage.getItem('identity')
    var token = localStorage.getItem('token')
    var name = localStorage.getItem('name')
    var _this = this
    axios.request({
      url: 'http://127.0.0.1:8000/api/statecheck',
      method: 'POST',
      data: {
        token: token,
        identity: identity,
        name: name
      },
      headers: {
        'Content-Type': 'application/json'
      }
    }).then(function (arg) {
      //  get return results
      if (arg.data.code !== 1000) {
        window.alert(arg.data.msg)
        _this.$router.push('/404')
      }
    }).catch(function (arg) {
      //  Error
      //  window.alert(arg.data.msg)
      _this.$router.push('/404')
    })
  }, */
  computed: {
    treeData1: function () {
      return JSON.parse(JSON.stringify(this.treeData))
    }
  },
  methods: {
    submitFreeTime: function () {
      var thisemail = localStorage.getItem('email')
      var ft1, ft2, ft3
      if (this.checkList.indexOf('上午') !== -1) ft1 = true         //ft1=true表示此上午时间段被选中
      else ft1 = false
      if (this.checkList.indexOf('下午') !== -1) ft2 = true
      else ft2 = false
      if (this.checkList.indexOf('晚上') !== -1) ft3 = true
      else ft3 = false
      axios.request({
        url: '/api/itvr/setfreetime',
        method: 'POST',
        data: {
          email: thisemail,
          free1: ft1,
          free2: ft2,
          free3: ft3
        },
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(function (arg) {
        console.log(arg.data.success)
      })
      console.log('submit free time')
    },
    remove: function (node, data) {
      const parent = node.parent
      const children = parent.data.children || parent.data
      const index = children.findIndex(d => d.id === data.id)
      children.splice(index, 1)
    }
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
    /*background-color: #E9EEF3;*/
    color: #333;
    /*text-align: center;*/
    /*line-height: 160px;*/
  }

  body > .el-container {
    margin-bottom: 40px;
  }

  .bg-purple-dark {
    background: #99a9bf;
  }
  .bg-purple {
    background: #d3dce6;
  }
  .bg-purple-light {
    background: #e5e9f2;
  }

  .custom-tree-node {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 14px;
    padding-right: 8px;
  }

  .el-tree {
    font-size: 40px;
  }

  .vertical-bar {
    width: 5px;
    height: 600px;
    background: lightgray;
    display: inline-block;
    margin-top: 15px;
    vertical-align: top;
  }
</style>
