## backend
主要用来和frontend进行协同合作
### 1.Mysql: 
#### (1)数据库设计
对于数据库的设计module位于`Online_Interview_System/interview/modules.py`下，主要设计了Applicant, Interviewer, Room三个实体。关于之后视频，代码，白板，对话框等面试信息的存储暂时使用Char类型表示，之后根据需求作出相应更改。
#### (2)所使用数据库信息
位于'Online_Interview_System/setting.py'的DATABASE部分，其中罗列了所使用数据库名称，用户名，密码等。之后若是需要在django的admin上进行数据库方面的测试， 可以使用超级管理员账号：cbn, 密码：123456
### 2.Vue: 
#### (1)配置访问Vue
对于访问编译好的vue静态文件，可以使用通过nginx直接访问或通过django路由访问的方式.
- django路由访问
主要通过Django模版配置使知道Vue的`index.html`的位置，通过视图来创建最简单的模版控制器，以及增加路由的方式。之后在访问`http://ip:8080/xxx`时便会直接返回`index.html`。若是涉及到较复杂的静态文件部分(css样式等)，还需做其它处理。(待更)
- nginx直接访问(待更)

### 3.模块整合
#### 1.模块设计的同学
对于视频等Vue模块，可以在`Issue #9`下方列出你们需要的URL路由请求，eg:`http://localhost:8080/xxx`,xxx即为你们需要的模块名。之后在和前端同学整合时会需要。之后可以把你们整合好的模块放在`/home/interview/database/`下，或在Issue上说明你们的模块在那个分支即可。也可以提前写上你们模块需要的交互操作，我们做出提前的设计。
#### 2.前端设计的同学
我们需要及时沟通，作出视图层的设计，并及时对数据库模型进行修改。
#### 3.django整合的同学
需要进一步详细了解django的机制。
#### 4.进一步部署
可能之后会需要关于nginx, uwsgi, celery, mysql, redis, supervisor等(常用的web框架)方面的知识

<I>待更，相关需求可在Issue#9下留言</I>
