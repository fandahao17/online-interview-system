# 后端API

## `/api/room/info/<int:roomid>/`

返回对应面试房间的面试时间、面试者等信息

用法：GET /api/room/info/《int:roomid》/
- 返回：
    - 成功：`{ 'roomid': 6位数字（str）, 'time': 时间（0-2）, 'tester': 面试官邮箱, 'interviewee': 候选人邮箱, 'rname': 面试官名字, 'ename': 候选人名字 }`
    - 失败（房间不存在等）：`{ 'roomid': 空字符串 }`

## `/api/room/getun/`

返回所有未确定结果的面试

用法：GET /api/room/getun/
- 返回：`[{ 'roomid': 6位数字（str）, 'time': 时间（0-2）, 'tester': 面试官邮箱, 'interviewee': 候选人邮箱 }, ...]`

## `/api/room/add/`

新建一个面试

用法：POST /api/room/add/
- 请求内容：`{ 'itve': 候选人邮箱(str), 'itvr': 面试官邮箱(str), 'time': 面试时间，范围0-2(int) }`
- 返回内容：`{ 'roomid': 6位数字房间号(str)，若失败则返回空 }`

## `/api/itvr/getall/`
返回所有面试官和他们在不同时间段是否空闲。

用法：GET /api/itvr/getall/
- 返回：`[{ 'name': str, 'mobile': str, 'email': str, free1: bool, free2: bool, free3: bool }, ...]`

## `/api/itve/getun/`
返回所有尚未确定是否录用的候选人，HR可以给这些候选人安排面试。

用法：GET /api/itve/getun/
- 返回：`[{ 'name': str, 'mobile': str, 'email': str }, ...]`