<template>
  <div class="hello">
    <div>
      <img id="logo" src="../assets/name.png" alt="logo">
    </div>
    <div id="div-login">
      <el-button type="success" round @click="$router.push('/login/')">点击登陆</el-button>
    </div>
    <img src="../assets/logo.jpg" alt="">
  </div>
</template>

<script>
// document.body.style.backgroundImage = `url($(../assests/bg.jpg))`
export default {
  name: 'HelloWorld',
  data () {
    return {
      roomid: ''
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
div {
    padding-bottom: 20px;
}
.hello {
  background: #eef3f7;
  width:100%;
  height:100%;
  top:0px;
  left:0px;
  z-index:1000;
  text-align: center;
}
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
