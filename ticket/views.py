from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render

# from ticket.models import TicketActivity
from ticket.constants import All_TICKET_TEMPLATE, RAISE_TICKET_TEMPLATE
from ticket.handlers.tickets import TicketAct


class TicketActivityView(APIView):
    def post(self, request):
        # import ipdb; ipdb.set_trace()
        data = request.data
        tkt_obj = TicketAct().create_issue(data)
        return render(request, RAISE_TICKET_TEMPLATE, {'tkt_info': tkt_obj})
        # return Response(response, status=status.HTTP_201_CREATED)

    def get(self, request):
        objs = TicketAct().get_all_tickets()

        paginator = Paginator(objs, 15)  # Show 15 ticket per page
        page = request.GET.get('page')
        try:
            tickets = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            tickets = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results
            tickets = paginator.page(paginator.num_pages)

        return render(request, All_TICKET_TEMPLATE, {'tkt_info': tickets})

        # return Response(response, status=status.HTTP_200_OK)


class TicketHtmlView(APIView):
    def get(self, request):
        return render(request, RAISE_TICKET_TEMPLATE)

    def post(self, request):
        data = request.data
        tkt_obj = TicketAct().create_issue(data)
        return render(request, RAISE_TICKET_TEMPLATE, {'tkt_info': tkt_obj})


class RetreiveTicketView(APIView):
    def get(self, request):
        dept = request.query_params.get('dept')
        cat = request.query_params.get('cat')
        state = request.query_params.get('status')
        urgent = request.query_params.get('urgent')
        response = TicketAct().get_with_state(dept, cat, state, urgent)
        return Response(response, status=status.HTTP_200_OK)


class ModifyTicketView(APIView):

    def put(self, request, ticket_uuid):
        data = request.data
        # ticket_uuid = request.query_params.get('ticket_uuid')
        response = TicketAct().modify(ticket_uuid, data)
        return Response(response, status=status.HTTP_200_OK)

    def delete(self, request):
        ticket_uuid = request.query_params.get('ticket_uuid')
        response = TicketAct().delete_ticket(ticket_uuid)
        return Response(response, status=status.HTTP_200_OK)


class AssignedTicketView(APIView):
    def post(self, request):
        data = request.data
        response = TicketAct().assigne_ticket(data)
        return Response(response, status=status.HTTP_200_OK)
