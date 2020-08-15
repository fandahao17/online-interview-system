<template>
  <section>
    <div class="container is-fluid dashboard">
      <div class="columns">
        <div class="column is-half code-editor">
          <el-card>
              <el-button @click="onSubmit">提交</el-button>
              <el-button @click="onClear">清空</el-button>
              {{this.resultMsg}}
          </el-card>
          <editor
            v-model="code"
            :options="cmOptions"
            @input="onCmCodeChange"
          />
          <div class="toolbar">
            <div class="columns">
              <div class="column">
                <multiselect
                  v-model="language"
                  class="languages"
                  :options="languages"
                  :show-labels="false"
                  placeholder="Select a language"
                  @input="setLanguageMode"
                ></multiselect>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import Multiselect from 'vue-multiselect'
import { codemirror } from 'vue-codemirror'
// import base style
import 'codemirror/lib/codemirror.css'
// import language js
import 'codemirror/mode/javascript/javascript.js'
import 'codemirror/mode/python/python.js'
import 'codemirror/mode/clike/clike.js'
// import theme style
import 'codemirror/theme/monokai.css'
export default {
  name: 'EditorWindow',
  components: {
    'editor': codemirror,
    Multiselect
  },
  data () {
    return {
      code: '',
      language: '',
      languages: ['javascript', 'python', 'c', 'cplus'],
      cmOptions: {
        tabSize: 4,
        mode: 'text/javascript',
        theme: 'monokai',
        lineNumbers: true,
        line: true
      },
      languageModes: {
        python: 'x-python',
        javascript: 'javascript',
        c: 'x-csrc',
        cplus: 'x-c++src'
      },
      resultMsg: ''
    }
  },
  computed: {
    codemirror () {
      return this.$refs.cmEditor.codemirror
    }
  },
  mounted () {
    //  recevie server data
    this.$socket.emit('client_enter', { id: this.$route.params.roomid })
  },
  methods: {
    onCmCodeChange (newCode) {
      //  when change, send changed code to the server here
      //  maybe needed to send all codes or part
      console.log('this is new code', newCode)
      //  todo:where add roomid
      //  send to server
      this.$socket.emit('client_update', {id: this.$route.params.roomid, code: newCode})
      this.code = newCode
    },
    setLanguageMode () {
      this.cmOptions.mode = `text/${this.languageModes[this.language]}`
    },
    onSubmit () {
      console.log('submit')
      console.log(this.code)
      console.log(this.language)
      this.$socket.emit('code_run', {id: this.$route.params.roomid, code: this.code, language: this.language})
    },
    onClear () {
      this.code = ''
      this.resultMsg = ''
    }
  },
  sockets: {
    connect () {
      console.log('socket connected')
    },
    server_update (data) {
      console.log('change code')
      this.code = data.code
    },
    server_result (data) {
      this.resultMsg = data.msg
    }
  }
}
</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style scoped>
/* TODO: refactor it into scss (need to learn :D) */
.dashboard {
  padding: 0;
}
.dashboard .columns {
  width: 100%;
  margin: 0;
}
.dashboard .columns .code-editor,
.dashboard .columns .drawing-board {
  padding: 0;
  border: 3px solid #1f364d;
  background: #001528;
}
.vue-codemirror {
  height: 50vh;
  border-radius: 4px;
}
.vue-codemirror >>> .CodeMirror {
  height: 100% !important;
}
.vue-codemirror >>> .cm-s-monokai.CodeMirror,
.vue-codemirror >>> .cm-s-monokai .CodeMirror-gutters {
  background: #001528 !important;
}
.toolbar {
  margin: 0;
  width: 100%;
  height: 64px;
  padding: 10px 0;
  border-top: 1px solid #1f364d;
}
.toolbar .column {
  padding: 0;
  margin-left: 15px;
}
.toolbar .room-title,
.toolbar .room-title:focus {
  background: #0e2439;
  color: #fff;
  border: none;
  border-bottom: 1px solid #1f364d;
  border-radius: 4px;
  outline: none;
}
.languages {
  color: #fff;
}
.languages >>> .multiselect__tags,
.languages >>> .multiselect__tags .multiselect__single,
.languages >>> .multiselect__tags .multiselect__input,
.languages >>> .multiselect__content-wrapper {
  background: #0e2439;
  text-transform: capitalize;
}
.languages >>> .multiselect__tags,
.languages >>> .multiselect__content-wrapper {
  border: none;
}
.languages >>> .multiselect__option {
  text-transform: capitalize;
}
</style>
 <!--// <template>
//   <div class="editor-window">
//       <editor
//       v-model="code"
//       :options="cmOptions"
//       @input="onCmCodeChange"
//       />
//     <b-card show-footer>
//       <editor
//       v-model="code"
//       :options="cmOptions"
//       @input="onCmCodeChange"
//       />
//       <b-form-select :plain="true" size="sm" name="selectedMode" v-model="selectedMode" @change.native="onModeChange($event)">
//         <option value="text/javascript">javascript</option>
//         <option value="sql">SQL</option>
//         <option value="verilog">Verilog</option>
//       </b-form-select>
//     </b-card>
//   </div>
// </template>

// <script>
// import 'codemirror/addon/merge/merge.js'
// import 'codemirror/addon/merge/merge.css'
// import { codemirror } from 'vue-codemirror'
// import 'codemirror/lib/codemirror.css'
// import 'codemirror/mode/javascript/javascript.js'
// import 'codemirror/mode/sql/sql'
// import 'codemirror/mode/verilog/verilog'
// export default {
//   name: 'EditorWindow',
//   data () {
//     return {
//       code: 'const a = 10',
//       cmOptions: {
//         tabSize: 4,
//         mode: 'text/javascript',
//         lineNumbers: true,
//         line: true
//       },
//       selectedMode: 'text/javascript'
//     }
//   },
//   methods: {
//     onModeChange (e) {
//       this.editorOption.mode = e.target.value
//     },
//     onCmCodeChange (newCode) {
//       //  when change, send changed code to the server here
//       //  maybe needed to send all codes or part
//       console.log('this is new code', newCode)
//       //  todo:where add roomid
//       //  send to server
//       this.$socket.emit('client_update', {code: newCode})
//       this.code = newCode
//     }
//   },
//   components: {
//     'editor': codemirror
//   },
//   sockets: {
//     connect () {
//       console.log('socket connected')
//     },
//     server_update (data) {
//       console.log('change code')
//       this.code = data.code
//     }
//   },
//   mounted () {
//     //  recevie server data
//     this.$socket.emit('client_enter', {})
//   }
// }
// </script>

// <style scoped>

// </style> -->
