<template>
  <div>
      <div class="title">注册界面</div>
      <el-row>
          <el-col :span="12">
              <el-select v-model="value" size="200px" clearable placeholder="请选择注册身份">
                <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"></el-option>
              </el-select>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
              <el-input v-model="input1" prefix-icon="el-icon-user" placeholder="姓名" clearable ></el-input>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
              <el-input v-model="input2" prefix-icon="el-icon-phone-outline" placeholder="电话" clearable ></el-input>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
              <el-input v-model="input3" prefix-icon="el-icon-message" placeholder="邮箱" clearable ></el-input>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
              <el-input v-model="input4" prefix-icon="el-icon-key" placeholder="请输入密码" show-password clearable></el-input>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="6">
              <el-button type="primary" round>注册</el-button>
          </el-col>
          <el-col :span="6">
            <el-button type="danger" round>取消</el-button>
        </el-col>
        </el-row>
  </div>
</template>
<script>
export default {
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
      }],
      value: '',
      input1: '',
      input2: '',
      input3: '',
      input4: '',
      imageUrl: ''
    }
  },
  methods: {
    handleAvatarSuccess (res, file) {
      this.imageUrl = URL.createObjectURL(file.raw)
    },
    beforeAvatarUpload (file) {
      const isJPG = file.type === 'image/jpeg'
      const isLt2M = file.size / 1024 / 1024 < 2
      if (!isJPG) {
        this.$message.error('上传头像图片只能是 JPG 格式!')
      }
      if (!isLt2M) {
        this.$message.error('上传头像图片大小不能超过 2MB!')
      }
      return isJPG && isLt2M
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
.head {
  font-size: 15px;
  color: gray;
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
