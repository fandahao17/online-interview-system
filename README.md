## backend+frontend
整合前后端(Django+Vue)
### 1.Mysql: 
#### (1)数据库设计
对于数据库的设计module位于`Online_Interview_System/interview/modules.py`下，主要设计了Hr(面试安排管理), Interviewer(面试管)，Super(超级管理员)三个实体及相应的Token对应model。关于之后视频，代码，白板，对话框等面试信息的存储暂时只对空闲时间作出设置，其余未作出设置。
#### (2)所使用数据库信息
位于'Online_Interview_System/setting.py'的DATABASE部分，其中罗列了所使用数据库名称，用户名，密码等。之后若是需要在django的admin上进行数据库方面的测试， 可以使用超级管理员账号：cbn, 密码：123456
### 2.Vue & django: 
- frontend：使用`Element-ui`完成, 服务运行于`http://127.0.0.1:8080`
- backend：使用`Django rest framework`实现, 服务运行于`http://127.0.0.1:8000`
- 前后端交互：
	- backend: 主要使用`Django rest framework`中的`@api_view(['POST'])`
	- frontend: 主要使用`axios`

### 3.接口部分
- 白板：将整合好的组件添加到`Online_Interview_System/frontend/src/intvweeviews/Board.vue`内
- 编辑器：将整合好的组件添加到`Online_Interview_System/frontend/src/intvweeviews/Editor.vue`内
- 文字聊天：将整合好的组件添加到`Online_Interview_System/frontend/src/intvweeviews/Text.vue`内
- 视屏：将整合好的组建添加到`Online_Interview_System/frontend/src/intvweeviews/Video.vue`内
### 4.api接口
- `http://127.0.0.1:8000/api/login`: 用户登陆api
- `http://127.0.0.1:8000/api/register`: 用户注册api

**Note：其它api还未设计，有需求可以及时交流更新**
### 5.项目运行方式
分别运行如下指令，之后项目效果在vue界面查看：
- django：python manage.py runserver (端口8000）
- vue：npm run dev（端口8080）




<I>Update time: 2020.6.2</I>
<I>待更，相关 `api/database` 需求可在Issue#9下留言</I>
