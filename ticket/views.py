from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render

# from ticket.models import TicketActivity
from ticket.constants import TEMPLATE_URL
from ticket.handlers.tickets import TicketAct


class TicketActivityView(APIView):
    def post(self, request):
        data = request.data
        response = TicketAct().create_issue(data)
        return Response(response, status=status.HTTP_201_CREATED)

    def get(self, request):
        response = TicketAct().get_all_tickets()
        return Response(response, status=status.HTTP_200_OK)


class RetreiveTicketView(APIView):
    def get(self, request):
        dept = request.query_params.get('dept')
        cat = request.query_params.get('cat')
        state = request.query_params.get('status')
        urgent = request.query_params.get('urgent')
        response = TicketAct().get_with_state(dept, cat, state, urgent)
        return Response(response, status=status.HTTP_200_OK)


class ModifyTicketView(APIView):
    def put(self, request):
        data = request.data
        ticket_uuid = request.query_params.get('ticket_uuid')
        response = TicketAct().modify(ticket_uuid, data)
        return Response(response, status=status.HTTP_200_OK)

    def delete(self, request):
        ticket_uuid = request.query_params.get('ticket_uuid')
        response = TicketAct().delete_ticket(ticket_uuid)
        return Response(response, status=status.HTTP_200_OK)

    # def get(self, request):
    #     """
    #     this is rendering the ticket data for user
    #     """
    #     objs = TicketActivity.objects.all()
    #     paginator = Paginator(objs, 15)  # Show 15 Reataurents per page
    #     page = request.GET.get('page')
    #     try:
    #         tickets = paginator.page(page)
    #     except PageNotAnInteger:
    #         # If page is not an integer, deliver first page.
    #         tickets = paginator.page(1)
    #     except EmptyPage:
    #         # If page is out of range (e.g. 9999), deliver last page of results
    #         tickets = paginator.page(paginator.num_pages)
    #
    #     return render(request, TEMPLATE_URL, {'tkt_info': tickets})
