# from django.http import HttpResponseRedirect
# from django.urls import reverse
from rest_framework.test import APITestCase

from ticket.handlers.tickets import TicketAct
from ticket.models import TicketActivity


class TicketActTest(APITestCase):
    def setUp(self):
        self.tkt = TicketAct()

    def test_create_issue(self):
        data = {
            'subject': 'Hi, this is a test subject',
            'content': 'and this is test content',
            'department': 2,
            'category': 1,
            'urgent': True
            }
        self.tkt.create_issue(data)
        self.assertEqual(TicketActivity.objects.all().count(), 1)

    def test_get_with_state(self):
        data = {
            'subject': 'Hi, this is a test subject',
            'content': 'and this is test content',
            'department': 3,
            'category': 1,
            'urgent': True
            }
        tkt_obj = self.tkt.create_issue(data)
        result = self.tkt.get_with_state(dept=3)
        expected_keys = {
            'subject',
            'content',
            'department',
            'category',
            'urgent',
            'uuid'
        }
        self.assertIsNotNone(result, expected_keys)
        self.assertEqual(result[0]['ticket_uuid'], tkt_obj.uuid)
