<template>
  <div>
    <div class="menu-left">
      <el-menu default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect" router>
        <el-menu-item index="/interviewer">NAME</el-menu-item>
        <el-menu-item index="/interviewer">选择时间</el-menu-item>
        <el-menu-item index="/schedule">查看面试安排</el-menu-item>
      </el-menu>
    </div>
    <el-dropdown class="avatar-container">
      <div>
        <span class="tag">面试官</span>
        <span class="tag">{{ intvwerName }}</span>
        <el-avatar icon="el-icon-user-solid" size="medium"></el-avatar>
        <i class="el-icon-caret-bottom"/>
      </div>
      <el-dropdown-menu slot="dropdown">
        <el-dropdown-item @click.native="logout">退出登录</el-dropdown-item>
      </el-dropdown-menu>
    </el-dropdown>
  </div>
</template>

<script>
export default {
  name: 'IntvwerHeadmenu',
  data: function () {
    return {
      activeIndex: '/interviewer',
      intvwerName: 'xxx'
    }
  },
  methods: {
    handleSelect: function (key, keyPath) {
      console.log(key, keyPath)
    },
    logout: function () {
      console.log('logout')
      localStorage.clear()
      this.$router.push('/')
    }
  },
  created: function () {
    let _this = this
    console.log(localStorage.getItem('identity'))
    if (localStorage.getItem('email') === null) {
      alert('need to login')
      _this.$router.push('/login/')
    } else if (localStorage.getItem('identity').toString() !== '1') {
      alert('permission denied: not a interviewer')
      if (localStorage.getItem('identity').toString() === '2') {
        _this.$router.push('/admin')
      } else if (localStorage.getItem('identity').toString() === '3') {
        _this.$router.push('/hr')
      } else {
        alert('can\'t identify ')
        _this.$router.push('/')
      }
    }
    _this.intvwerName = localStorage.getItem('name')
    console.log(_this.intvwerName)
  }
}
</script>

<style scoped>
  .tag {
    font-size: 20px;
    padding-left: 20px;
    padding-right: 15px;
    padding-bottom: 5px;
  }
  .el-avatar {
    vertical-align: middle;
  }
  .menu-left {
    float: left;
    padding-right: 20px;
    background-color: #DCDFE6;
  }
  .avatar-container {
    float: right;
    padding-right: 30px;
    background-color: #DCDFE6;
  }
  .el-menu-demo {
    background-color: #DCDFE6;
    float: left;
    padding-left: 10px;
  }
</style>
