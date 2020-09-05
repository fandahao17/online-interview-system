<template>
  <div>
    <div class="menu-left">
      <el-menu default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect" router>
        <el-menu-item index="/hr">NAME</el-menu-item>
        <el-menu-item index="/hr">分配面试</el-menu-item>
        <el-menu-item index="/watch">观看面试</el-menu-item>
        <el-menu-item index="/recall">回溯面试</el-menu-item>
      </el-menu>
    </div>
    <el-dropdown class="avatar-container">
      <div>
        <span class="tag">Hr</span>
        <span class="tag">{{ hrname }}</span>
        <el-avatar icon="el-icon-user-solid" size="medium"></el-avatar>
        <i class="el-icon-caret-bottom"/>
      </div>
      <el-dropdown-menu slot="dropdown">
        <el-dropdown-item>个人中心</el-dropdown-item>
        <el-dropdown-item>选项二</el-dropdown-item>
        <el-dropdown-item divided @click.native="logout">退出登录</el-dropdown-item>
      </el-dropdown-menu>
    </el-dropdown>
  </div>
</template>

<script>
export default {
  name: 'HeadMenu',
  data: function () {
    return {
      activeIndex: '/hr',
      hrname: 'xxx'
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
    if (localStorage.getItem('email') === null) {
      alert('need to login')
      _this.$router.push('/login/')
    } else if (localStorage.getItem('identity') != '3') {
      alert('permission denied: not a hr')
      if (localStorage.getItem('identity') == '2') {
        _this.$router.push('/admin')
      } else if (localStorage.getItem('identity') == '1') {
        _this.$router.push('/interviewer')
      } else {
        alert('can\'t identify ')
        _this.$router.push('/')
      }
    }
    _this.hrname = localStorage.getItem('name')
    console.log(_this.hrname)
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
