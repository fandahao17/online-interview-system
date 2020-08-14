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

    <div class="web-im">
      <div class="dis-flex">
        <div class="msg-content">
          <div class="header im-title">{{title}}</div>
            <div class="content im-record">
              <div class="li" :class="{user: item.uid == uid}" v-for="item in currentMessage" v-bind:key="item">
                <template v-if="item.type===1">
                  <p class="join-tips">{{item.msg}}</p>
                </template>
                <template v-else>
                  <div class="img">{{item.nickname}}</div>
                  <p class="message-box">{{item.msg}}</p>
                </template>
              </div>
            </div>
            <div class="footer im-input">
              <input type="text" v-model="msg" placeholder="请输入内容">
              <button @click="send">发送</button>
            </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
/* eslint-disable */
import Vue from 'vue'
import moment from 'moment'

export default {
  name: 'Text',
  props: ['roomInfo'],
  components: {
    'c-dialog': Vue.extend(require('@/components/dialog/index.vue').default)
  },
  data(){
    return {
      title: '群聊',
      uid: '',
      nickname: '',
      socket: '',
      msg: '',
      messageList: [],
      users: [],
      bridge: []
    }
  },
  mounted() {
    let vm = this;
    let user = localStorage.getItem('WEB_IM_USER');
    console.log(vm.roomInfo);
    user = user && JSON.parse(user) || {};
    vm.uid = user.uid;
    vm.nickname = user.nickname;
    vm.nickname = "测试员" + Math.floor(Math.random()*1000);
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
        return item.bridge.sort().join(',') == vm.bridge.sort().join(',')
      })
      if(vm.messageList.length>12){
        vm.messageList.shift();
      }
      return data;
    }
  },
  methods: {
    triggerGroup() {
      this.bridge = [];
      this.title = '群聊';
    },
    triggerPersonal(item) {
      if(this.uid === item.uid){
        return;
      }
      this.bridge = [this.uid, item.uid];
      this.title = '和' + item.nickname + '聊天';
    },
    send(){
      if(!this.msg){
        return
      }
      this.sendMessage(2, this.msg)
    },
    sendMessage(type, msg){
      this.socket.send(JSON.stringify({
        uid: this.uid,
        type: type,
        nickname: this.nickname,
        msg: msg,
        bridge: this.bridge
      }));
      this.msg = '';
    },
    conWebSocket(){
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
