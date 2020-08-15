<template>
  <div>
      <div class="title">登录界面</div>
      <el-row>
          <el-col :span="12">
              <el-select v-model="value" size="200px" clearable placeholder="请选择登录身份">
                <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"></el-option>
              </el-select>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
              <el-input v-model="input1" prefix-icon="el-icon-user" placeholder="Name" clearable ></el-input>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
              <el-input v-model="input2" prefix-icon="el-icon-key" placeholder="请输入密码" show-password clearable></el-input>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="6">
              <el-button type="primary" @click.native="onLogin" round>登录</el-button>
          </el-col>
          <el-col :span="6">
            <el-button type="danger" round>取消</el-button>
        </el-col>
        </el-row>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'LogIn',
  data () {
    return {
      options: [{
        value: '身份1',
        label: '面试官'
      }, {
        value: '身份2',
        label: '超级管理员'
      }, {
        value: '身份3',
        label: 'HR'
      }
      ],
      value: '',
      input1: '',
      input2: ''
    }
  },
  methods: {
    onLogin () {
      var _this = this
      axios.request({
        url: 'http://127.0.0.1:8000/api/login',
        method: 'POST',
        data: {
          name: _this.input1,
          password: _this.input2,
          identity: Number(_this.value.charAt(_this.value.length - 1))
        },
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(function (arg) {
        //  get return results
        if (arg.data.code === 1000) {
          window.alert(arg.data.msg)
          localStorage.setItem('identity', Number(_this.value.charAt(_this.value.length - 1)))
          localStorage.setItem('token', arg.data.token)
          localStorage.setItem('name', _this.input1)
          if (arg.data.type === '1') {
            _this.$router.push('/interviewer')
          } else if (arg.data.type === '2') {
            _this.$router.push('/admin')
          } else if (arg.data.type === '3') {
            _this.$router.push('/hr')
          }
        } else {
          window.alert(arg.data.msg)
        }
      })
      //  .catch(function (arg) {
      //  Error
      //  console.log(arg.data.msg)
      //  })
    }
  }
}
</script>
<style scoped>
.text {
  font-size: 34px;
  text-align: center;
  font-family: Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
}
.title {
  font-size: 45px;
  color: gray;
  margin-right: 250px;
  margin-bottom: 30px;
}
.el-row {
  color: gray;
  margin-bottom: 20px;
}
.el-col {
  border-radius: 4px;
}
.grid-content {
  border-radius: 4px;
  min-height: 36px;
}
.row-bg {
  padding: 10px 0;
  background-color: #f9fafc;
}
</style>
