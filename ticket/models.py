from django.contrib.auth.models import User
from django.db import models

from base.fields import ChoicesField
from base.models import AbstractAuditModel
from ticket.choices import Department, TicketCategory, TicketStatus


class TicketActivity(AbstractAuditModel):
    subject = models.CharField(max_length=200, blank=True, null=True)
    content = models.CharField(max_length=2000, blank=True, null=True)
    department = ChoicesField(
                                default=Department.STATUS_NOT_SET,
                                choice_class=Department
                        )
    category = ChoicesField(
                                default=TicketCategory.STATUS_NOT_SET,
                                choice_class=TicketCategory
                        )
    status = ChoicesField(
                                default=TicketStatus.CREATED,
                                choice_class=TicketStatus
                        )
    urgent = models.BooleanField(default=False)

    def __str__(self):
        return '%s ' % (self.subject)


class TrackTicket(AbstractAuditModel):
    ticket = models.ForeignKey(TicketActivity, related_name='ticket_track',
                               blank=True, null=True, on_delete=models.CASCADE)
    from_user = models.OneToOneField(User, related_name='from_user',
                                     on_delete=models.CASCADE, null=True)
    to_user = models.OneToOneField(User, related_name='to_user',
                                   on_delete=models.CASCADE, null=True)


class TicketAttachment(AbstractAuditModel):
    ticket = models.ForeignKey(TicketActivity, related_name='ticket_att',
                               blank=True, null=True, on_delete=models.CASCADE)
    pic = models.ImageField(upload_to='ticket_folder', blank=True, null=True)

    def __str__(self):
        return '%s' % (self.ticket.uuid)
