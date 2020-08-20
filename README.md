## TODO
1. 面试房间(`/frontend/src/intvweeviews/*`)
- 面试房间的 url 生成未完成。需要为每个房间生成唯一的 url，无需登录，只要候选人从邮箱中点击链接进入即可。
- ~~面试房间录像并保存的功能未实现~~
- 面试结束后需要弹出评价窗口，未完成(UI-ALL.pdf 18-23页)
- 题目的展示窗口未完成(UI-ALL.pdf 18-23页)

2. 登录部分(`/frontend/src/login/*`)
- 现在的登录使用 token，在页面跳转之后就会失效，需要寻找在页面跳转之后仍能保存登录者身份的方法。

3. HR 页面(`/frontend/src/hrs/*`)
- 管理面试部分(UI-ALL.pdf 1-8页)：前端页面和发送请求部分均未完成（刘硕在写）
- 观看面试部分(UI-ALL.pdf 9-10页)：发送请求部分未完成
- 回溯面试部分(UI-ALL.pdf 27-30页)：发送请求部分未完成

4. 面试官页面(`/frontend/src/intvwerviews/*`)
- 时间选择和查看面试安排(UI-ALL.pdf 14-18页)：发送请求部分未完成（需要在 登录部分 完成之后进行，因为面试官的界面中需要知道是哪一个面试官在选择时间和查看面试）

5. admin 界面(`/frontend/src/adminviews/*`)（曹宇昂在写）
- 候选人、面试官、HR 信息的修改
- 候选人、面试官、HR 的添加和删除
- 将面试官和候选人分配给 HR


## backend+frontend
整合前后端(Django+Vue)
### 1.Mysql: 
#### (1)数据库设计
对于数据库的设计module位于`Online_Interview_System/interview/modules.py`下，主要设计了Hr(面试安排管理), Interviewer(面试管)，Super(超级管理员)三个实体及相应的Token对应model。关于之后视频，代码，白板，对话框等面试信息的存储暂时只对空闲时间作出设置，其余未作出设置。
#### (2)所使用数据库信息
位于'Online_Interview_System/setting.py'的DATABASE部分，其中罗列了所使用数据库名称，用户名，密码等。之后若是需要在django的admin上进行数据库方面的测试， 可以登陆`http://106.14.227.202:8000/admin/`，使用超级管理员账号：admin, 密码：superuser。
### 2.Vue & django: 
- frontend：使用`Element-ui`完成, 服务运行于`http://106.14.227.202`
- backend：使用`Django rest framework`实现, 服务运行于`http://106.14.227.202/api/`
- 前后端交互：
	- backend: 主要使用`Django rest framework`中的`@api_view(['POST'])`
	- frontend: 主要使用`axios`

### 3.接口部分
- 白板：将整合好的组件添加到`Online_Interview_System/frontend/src/intvweeviews/Board.vue`内
- 编辑器：将整合好的组件添加到`Online_Interview_System/frontend/src/intvweeviews/Editor.vue`内
- 文字聊天：将整合好的组件添加到`Online_Interview_System/frontend/src/intvweeviews/Text.vue`内
- 视屏：将整合好的组建添加到`Online_Interview_System/frontend/src/intvweeviews/Video.vue`内
### 4.api接口
详细接口请见[api.md](API.md)。

- `http://106.14.227.202/api/login`: 用户登陆api
- `http://106.14.227.202/api/register`: 用户注册api
- `http://106.14.227.202/api/statecheck`: 用户token前端验证api
- `http://106.14.227.202/api/room/info/<int:roomid>/`: 获取面试房间的相关信息

### 5.api使用方法
- login-api: 参考`LogIn.vue`实现
- register-api: 参考`RegisterIn.vue`实现
- statecheck-api(前端使用localStorage存储token，其它设计暂未实现): (1)第一次登录的时候，前端调后端的登陆接口，发送用户名和密码; (2)后端收到请求，验证用户名和密码，验证成功，就给前端返回一个token; (3)前端拿到token，将token存储到localStorage和vuex中，并跳转路由页面; (4)前端每次跳转路由，就判断 localStroage 中有无 token ，没有就跳转到登录页面，有则跳转到对应路由页面; (5)每次调后端接口，都要在请求头中加token; (6)后端判断请求头中有无token，有token，就拿到token并验证token，验证成功就返回数据，验证失败（例如：token过期）就返回401，请求头中没有token也返回401; (7)如果前端拿到状态码为401，就清除token信息并跳转到登录页面

### 6.面试房间获取roomid等信息的方式
面试房间的 url 为`http://106.14.227.202/#/interviewee/<roomid>/`，例如 `http://106.14.227.202/#/interviewee/673841/`，其中最后一部分房间号需要手动输入，请在后端的 admin 界面（见上面的1(2)）中查看现有的房间号。

如果只需要获取房间号，则可以在子组件中可以通过变量 `this.$route.params.roomid` 获取房间号。

如果除房间号外还需要获取该房间的详细信息，如被面试者姓名、面试官姓名等等，父组件 `Online_Interview_System/frontend/src/intvweeviews/Index.vue` 中的变量 `roomInfo` 存储了该房间的详细信息，需要在子组件中使用 `props` 来将该变量从父组件传至子组件。关于 `props` 的使用在 `Online_Interview_System/frontend/src/intvweeviews/Video.vue` 中有示例。

**Note：其它api还未设计，有需求可以及时交流更新**
### 7.项目运行方式
直接在`http://106.14.227.202`查看。




<I>Update time: 2020.8.11</I>
<I>待更，相关 `api/database` 需求可在Issue#9下留言</I>
