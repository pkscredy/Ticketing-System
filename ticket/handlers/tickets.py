from django.contrib.auth.models import User

from ticket.choices import TicketStatus
from ticket.dbapi import TicketActivityDbio, TrackTicketDbio
from ticket.models import TicketActivity
from ticket.utils import SearchPattern


class TicketAct:
    def create_issue(self, data):
        tkt_data = {
            'subject': data.get('subject'),
            'content': data.get('content'),
            'department': data.get('department'),
            'category': data.get('category'),
            'urgent': data.get('urgent')
        }
        return TicketActivityDbio().create_obj(tkt_data)

    def get_all_tickets(self):
        objs = TicketActivity.objects.all()
        if not objs:
            return {
                'message': 'No tickets are available'
            }
        return objs

    def get_with_state(self, dept=None, cat=None, state=None, urgent=None):
        if dept is not None:
            objs = TicketActivityDbio().filter_objects({'department': dept})
            return self.retrive_data(objs)
        elif cat is not None:
            objs = TicketActivityDbio().filter_objects({'category': cat})
            return self.retrive_data(objs)
        elif state is not None:
            objs = TicketActivityDbio().filter_objects({'status': state})
            return self.retrive_data(objs)
        else:
            objs = TicketActivityDbio().filter_objects({'urgent': urgent})
            return self.retrive_data(objs)

    def retrive_data(self, objs):
        issue_data = []
        for obj in objs:
            data = {
                'subject': obj.subject,
                'content': obj.content,
                'department': obj.department,
                'category': obj.category,
                'status': obj.status,
                'urgent': obj.urgent,
                'ticket_uuid': obj.uuid
            }
            issue_data.append(data)
        return issue_data

    def modify(self, ticket_uuid, data):
        obj = TicketActivityDbio().get_object(
            {
                'uuid': ticket_uuid
            }
        )
        tkt_data = {
            'subject': data.get('subject', obj.subject),
            'content': data.get('content', obj.content),
            'department': data.get('department', obj.department),
            'category': data.get('category', obj.category),
            'urgent': data.get('urgent', obj.urgent)
        }
        return TicketActivityDbio().update_obj(obj, tkt_data)

    def delete_ticket(self, ticket_uuid):
        TicketActivityDbio().get_object(
            {
                'uuid': ticket_uuid
            }
        ).delete()
        return {
            'message': 'ticket deleted'
        }

    def assigne_ticket(self, data):
        from_obj = User.objects.get(id=data['from_id'])
        to_obj = User.objects.get(id=data['to_id'])
        obj = TicketActivityDbio().get_object(
            {
                'uuid': data['ticket_uuid']
            }
        )
        tkt_obj = TicketActivityDbio().update_obj(obj, {
            'status': TicketStatus.ASSIGNED.value
            }
        )
        TrackTicketDbio().create_obj(
            {
                'from_user': from_obj,
                'to_user': to_obj,
                'ticket': tkt_obj
            }
        )
        return {
            'message': 'Ticket has been assigned'
        }

    def retreive_single_ticket(self, ticket_uuid):
        return TicketActivityDbio().get_object(
            {
                'uuid': ticket_uuid
            }
        )

    def new_search_implement(self, param):
        res = SearchPattern().in_choices(param.lower())
        if res is not None:
            for model, cat in res.items():
                return TicketActivityDbio().filter_objects({model: cat})
