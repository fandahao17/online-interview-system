<template>
  <div id="app">
    <c-dialog
      ref="loginDialog"
      title='请输入你的昵称'
      confirmBtn="开始聊天"
      @confirm="login"
    >
      <input class="nickname" v-model="nickname" type="text" placeholder="请输入你的昵称">
    </c-dialog>

    <div class="web-im" id="web-im">
      <div class="dis-flex">
        <div class="msg-content">
          <div class="header im-title">{{title}}</div>
            <div class="body im-record" id="im-record">
              <div class="li" :class="{user: item.uid == uid}" v-for="item in currentMessage" v-bind:key="item">
                <template v-if="item.type===2">
                  <div class="img">{{item.nickname}}</div>
                  <p class="message-box">{{item.msg}}</p>
                </template>
              </div>
            </div>
        </div>
      </div>
    </div>
    <div class="footer im-input" v-show="inputshow">
      <input type="text" v-model="msg" placeholder="请输入内容">
      <button @click="send">发送</button>
    </div>
  </div>
</template>

<script>
/* eslint-disable */
import Vue from 'vue'
import moment from 'moment'

export default {
  name: 'Text',
  props: ['roomInfo','isHr'],
  components: {
    'c-dialog': Vue.extend(require('@/components/dialog/index.vue').default)
  },
  data(){
    return {
      roomid: '',
      title: '群聊',
      uid: '',
      nickname: '',
      socket: '',
      msg: '',
      messageList: [],
      users: [],
      bridge: [],
      inputshow: true
    }
  },
  mounted() {
    let vm = this;
    let user = localStorage.getItem('WEB_IM_USER');
    let path = vm.$route.path;
    var str = path;
    console.log(vm.roomInfo);
    user = user && JSON.parse(user) || {};
    user.roomid = vm.$route.params.roomid;
    vm.roomid = vm.$route.params.roomid;
    console.log("item.roomid:"+vm.roomid);
    vm.uid = user.uid;
    vm.nickname = user.nickname;
    if(str.indexOf("interviewee") != -1){
      vm.nickname = "候选人";
    }
    else{
      vm.nickname = "面试官";
    }
    vm.conWebSocket();

    document.onkeydown = function (event) {
        var e = event || window.event;
        if (e && e.keyCode == 13) { //回车键的键值为13
            vm.send()
        }
    }
  },
  computed: {
    currentMessage() {
      let vm = this;
      let data = vm.messageList.filter(item=>{
        return (item.bridge.sort().join(',') == vm.bridge.sort().join(','))&&(item.roomid == vm.roomid)
      })
      //if(vm.messageList.length>12){
      //  vm.messageList.shift();
      //}
      return data;
    }
  },
  methods: {
    triggerGroup() {
      this.bridge = [];
      this.title = this.roomid;
    },
    triggerPersonal(item) {
      if(this.uid === item.uid){
        return;
      }
      this.bridge = [this.uid, item.uid];
      this.title = '和' + item.nickname + '聊天';
    },
    send(){
      if(!this.msg||this.isHr==true){
        return
      }
      this.sendMessage(2, this.msg)
    },
    sendMessage(type, msg){
      this.socket.send(JSON.stringify({
        roomid: this.roomid,
        uid: this.uid,
        type: type,
        nickname: this.nickname,
        msg: msg,
        bridge: this.bridge
      }));
      this.msg = '';
    },
    conWebSocket(){
      if (this.isHr == true){
      this.inputshow = false;
      }
      let vm = this;
      if(window.WebSocket){
        vm.socket = new WebSocket('ws://106.14.227.202:8010');
        let socket = vm.socket;

        socket.onopen = function(e){
          console.log("连接服务器成功");
          if(!vm.uid){
            vm.uid = 'web_im_' + moment().valueOf();
            localStorage.setItem('WEB_IM_USER', JSON.stringify({
              uid: vm.uid,
              roomid: vm.roomid,
              nickname: vm.nickname
            }))
          }
          vm.sendMessage(1)
        }
        socket.onclose = function(e){
          console.log("服务器关闭");
        }
        socket.onerror = function(){
          console.log("连接出错");
        }
        // 接收服务器的消息
        socket.onmessage = function(e){
          console.log(vm.messageList);
          let message = JSON.parse(e.data);
          vm.messageList.push(message);
          if(message.users) {
            vm.users = message.users;
          }
        }   
      }
    },
    login(){
      this.$refs.loginDialog.hide()
      this.conWebSocket();
    }
  }
}
</script>

<style lang='stylus' scoped>
  @import './Text.styl';
</style>
