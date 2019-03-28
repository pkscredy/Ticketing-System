from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ticket.constants import RAISE_TICKET_TEMPLATE, All_TICKET_TEMPLATE
from ticket.handlers.tickets import TicketAct


class TicketActivityView(APIView):

    def get(self, request):
        if len(request.query_params) is not 0:
            param = request.query_params.get('search')
            objs = TicketAct().new_search_implement(param)
            return render(request, 'searchpage.html', {'tkt_info': objs})
        objs = TicketAct().get_all_tickets()
        if 'message' in objs:
            return render(request, 'no_ticket.html')

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


class TicketHtmlView(APIView):
    def get(self, request):
        return render(request, RAISE_TICKET_TEMPLATE)

    def post(self, request):
        data = request.data
        tkt_obj = TicketAct().create_issue(data)
        messages.success(request, 'The Ticket has been Created')
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

    def get(self, request, ticket_uuid):
        obj = TicketAct().retreive_single_ticket(ticket_uuid)
        return render(request, 'view_ticket.html', {'info': obj})

    def post(self, request, ticket_uuid):
        data = request.data
        if data.get('_method') == 'PUT':
            return self.put(request, ticket_uuid)
        return self.delete(request, ticket_uuid)

    def put(self, request, ticket_uuid):
        data = request.data
        obj = TicketAct().modify(ticket_uuid, data)
        messages.success(request, 'The Ticket has been Updated')
        return render(request, 'view_ticket.html', {'info': obj})

    def delete(self, request, ticket_uuid):
        TicketAct().delete_ticket(ticket_uuid)
        arg_num = reverse('get_tickets')
        messages.success(request, 'The Ticket has been Deleted')
        return HttpResponseRedirect(arg_num)


class AssignedTicketView(APIView):
    def post(self, request):
        data = request.data
        response = TicketAct().assigne_ticket(data)
        return Response(response, status=status.HTTP_200_OK)
