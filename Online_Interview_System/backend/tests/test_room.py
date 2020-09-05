from django.test import TestCase, Client
from ..models import *
from django.test.utils import setup_test_environment

class RoomTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        itve = Interviewee.objects.create(
            name = "abcde",
            mobile = "43224252",
            email = "123@567.com",
        )
        itvr = Interviewer.objects.create(
            name = "abcde",
            mobile = "43224252",
            email = "123@567.com",
            password = "123456"
        )
        room = Room.objects.create(
            roomid = 999,
            time = 1,
            tester = itvr,
            interviewee = itve,
            remark = "还行吧"
        )

    def setUp(self):
        pass

    def test_room_add(self):
        client = Client()
        itve = Interviewee.objects.get(pk="123@567.com")
        itvr = Interviewer.objects.get(pk="123@567.com")
        room = Room.objects.get(pk=999)
        response = client.post('/room/add/', {'itve': itve, 'itvr': itvr, 'time': 0})
        json_data = eval(response.content.decode('utf8'))
        self.assertNotEqual(json_data['roomid'], '')
        new_add = Room.objects.get(pk=int(json_data['roomid']))
        self.assertEqual(new_add.roomid, int(json_data['roomid']))

    def test_room_unfinished(self):
        client = Client()
        response = client.get('/room/getun/')
        json_data = eval(response.content.decode('utf8'))
        self.assertEqual(json_data[0]['roomid'], 999)
        self.assertEqual(json_data[0]['time'], 1)
        self.assertEqual(json_data[0]['tester__email'], '123@567.com')
        self.assertEqual(json_data[0]['interviewee__email'], '123@567.com')

    def test_room_getinfo(self):
        client = Client()
        response = client.get('/room/info/999')
        json_data = eval(response.content.decode('utf8'))
        self.assertEqual(json_data[0]['roomid'], 999)
        self.assertEqual(json_data[0]['time'], 1)
        self.assertEqual(json_data[0]['tester'], '123@567.com')
        self.assertEqual(json_data[0]['interviewee'], '123@567.com')
        self.assertEqual(json_data[0]['rname'], 'abcde')
        self.assertEqual(json_data[0]['ename'], 'abcde')

    def test_room_delete(self):
        import json
        client = Client()
        itve = Interviewee.objects.get(pk="123@567.com")
        itvr = Interviewer.objects.get(pk="123@567.com")
        room = Room.objects.get(pk=999)
        room = Room.objects.create(
            roomid = 110,
            time = 2,
            tester = itvr,
            interviewee = itve
        )
        room.refresh_from_db()
        response = client.delete('/room/delete/', {'roomid': 110}, content_type='application/json')
        print('---room-delete')
        print(response.content)
        json_data = json.loads(response.content.decode('utf8'))
        self.assertEqual(json_data['success'], True)
        with self.assertRaises(DoesNotExist, msg='Room matching query does not exist.'):
            old_room = Room.objects.get(pk=110)
        self.assertNotEqual(old_room.roomid, 110)

    def test_room_rate(self):
        import json
        client = Client()
        room = Room.objects.get(pk=999)
        response = client.post('/room/rate/', {'roomid': 999, 'score': 100, 'remark': '整挺好'})
        json_data = json.loads(response.content.decode('utf8'))
        self.assertEqual(json_data['success'], True)
        self.assertEqual(room.score, 100)
        self.assertEqual(room.remark, '整挺好')

    def test_room_review(self):
        client = Client()
        itve = Interviewee.objects.get(pk="123@567.com")
        itvr = Interviewer.objects.get(pk="123@567.com")
        room = Room.objects.get(pk=999)
        Room.objects.create(
            roomid = 110,
            time = 2,
            tester = itvr,
            interviewee = itve,
            score = 90,
            remark = 'nice'
        )
        response = client.get('/room/review')
        json_data = eval(response.content.decode('utf8'))
        self.assertEqual(json_data[1]['roomid'], 110)
        self.assertEqual(json_data[1]['interviewee__name'], "abcde")
        self.assertEqual(json_data[1]['interviewer__name'], "abcde")
        self.assertEqual(json_data[1]['score'], 90)
        self.assertEqual(json_data[1]['time'], 2)
        self.assertEqual(json_data[1]['interviewee__status'], 0)


    def test_room_get_remark(self):
        client = Client()
        response = client.post('/room/decide/', {'roomid': 999})
        json_data = eval(response.content.decode('utf8'))
        self.assertEqual(json_data['remark'], "还行吧")

    def room_decide(self):
        import json
        client = Client()
        itve = Interviewee.objects.get(pk="123@567.com")
        itvr = Interviewer.objects.get(pk="123@567.com")
        room = Room.objects.get(pk=999)
        response = client.post('/room/decide/', {'rooms':[999], 'status':2})
        json_data = json.loads(response.content.decode('utf8'))
        self.assertEqual(json_data['success'], True)
        self.assertEqual(itve.status, 2)
