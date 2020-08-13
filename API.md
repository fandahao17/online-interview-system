# 后端API

## room

### `/api/room/info/<int:roomid>/`

返回对应面试房间的面试时间、面试者等信息

用法：GET /api/room/info/《int:roomid》/
- 返回：
    - 成功：`{ 'roomid': 6位数字（str）, 'time': 时间（0-2）, 'tester': 面试官邮箱, 'interviewee': 候选人邮箱, 'rname': 面试官名字, 'ename': 候选人名字 }`
    - 失败（房间不存在等）：`{ 'roomid': 空字符串 }`

### `/api/room/getun/`

返回所有未确定结果的面试

用法：GET /api/room/getun/
- 返回：`[{ 'roomid': 6位数字（str）, 'time': 时间（0-2）, 'tester': 面试官邮箱, 'interviewee': 候选人邮箱 }, ...]`

### `/api/room/add/`

新建一个面试

用法：POST /api/room/add/
- 请求内容：`{ 'itve': 候选人邮箱(str), 'itvr': 面试官邮箱(str), 'time': 面试时间，范围0-2(int) }`
- 返回内容：`{ 'roomid': 6位数字房间号(str)，若失败则返回空 }`

### `/api/room/delete/`
删除面试。

用法：POST /api/room/delete/
- 请求内容：`{ 'roomid': int }`
- 返回内容：`{ 'success': bool }`

### `/api/room/rate/`
给面试打分。

用法：POST /api/room/rate/
- 请求内容：`{ 'roomid': int, 'score': int (0-100), 'remark': 评语（str）}`
- 返回内容：`{ 'success': bool }`

### `/api/room/review/`
返回面试结果（UI-ALL第28页）。

用法：GET /api/room/review/
- 返回内容：`[{ 'roomid': str, 'interviewee__name': 候选人姓名(str), 'interviewer__name': 面试官姓名(str), 'score': int(0-100), 'time': int(0-2), 'interviewee__status': int(0-2) }, ...]`
- status：0代表未分配，1代表拒绝，2代表录用

### `/api/room/remark`
返回面试评语

用法：POST /api/room/remark/
- 请求内容：`{ 'roomid': int }`
- 返回内容：`{ 'remark': str }`

### `/api/room/decide`
确定是否录用，支持批量修改

用法：POST /api/room/decide/
- 请求内容：`{ 'rooms': [int, int, ...], 'status': int(0-2) }`
- 返回内容：`{ 'success': bool }`

## itve

### `/api/itve/`
修改候选人的信息，若`old_email`域为空字符串，则新建一个候选人。

用法：POST /api/itve/
请求内容：`{ 'name': str, 'mobile': str, 'old_email': str, 'new_email': str }`
返回：`{ 'success': bool }`


### `/api/itve/getun/`
返回所有尚未确定是否录用的候选人，HR可以给这些候选人安排面试。

用法：GET /api/itve/getun/
- 返回：`[{ 'name': str, 'mobile': str, 'email': str }, ...]`

### `/api/itve/getall/`
返回所有候选人。

用法：GET /api/itve/getall/
返回：`[{ 'name': str, 'mobile': str, 'email': str, 'status': int }, ...]`

## itvr

### `/api/itvr/`
修改面试官的信息，若`old_email`域为空字符串，则新建一个面试官。

用法：POST /api/itvr/
请求内容：`{ 'name': str, 'mobile': str, 'password': str, 'old_email': str, 'new_email': str, 'free1': bool, 'free2': bool, 'free3': bool }`
返回：`{ 'success': bool }`


### `/api/itvr/getall/`
返回所有面试官和他们在不同时间段是否空闲。

用法：GET /api/itvr/getall/
- 返回：`[{ 'name': str, 'mobile': str, 'email': str, free1: bool, free2: bool, free3: bool }, ...]`

## HR

### `/api/hr/`
修改HR的信息，若`old_email`域为空字符串，则新建一个HR。

用法：POST /api/itve/
请求内容：`{ 'name': str, 'mobile': str, 'password': str, 'old_email': str, 'new_email': str }`
返回：`{ 'success': bool }`

### `/api/hr/getall/`
返回所有HR

用法：GET /api/itve/getall/
返回：`[{ 'name': str, 'mobile': str, 'email': str }, ...]`