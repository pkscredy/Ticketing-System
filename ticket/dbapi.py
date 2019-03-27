from base.dbapi import AbstractBaseDbIO

from ticket.models import TicketActivity, TicketAttachment, TrackTicket


class TicketActivityDbio(AbstractBaseDbIO):

    @property
    def model(self):
        return TicketActivity


class TicketAttachmentDbio(AbstractBaseDbIO):

    @property
    def model(self):
        return TicketAttachment


class TrackTicketDbio(AbstractBaseDbIO):

    @property
    def model(self):
        return TrackTicket
