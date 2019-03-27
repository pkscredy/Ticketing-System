from django.contrib import admin

from ticket.models import TicketActivity, TicketAttachment, TrackTicket


@admin.register(TicketActivity)
class TicketActivityAdmin(admin.ModelAdmin):
    list_display = ('subject', 'content', 'department', 'category',
                    'status', 'urgent',)
    search_fields = ('department', 'status', 'urgent',)


@admin.register(TrackTicket)
class TrackTicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_uuid', 'from_user', 'to_user',)

    def ticket_uuid(self, obj):
        return obj.ticket.uuid

    search_fields = ('ticket_uuid',)


@admin.register(TicketAttachment)
class TicketAttachmentAdmin(admin.ModelAdmin):
    list_display = ('ticket_uuid',)

    def ticket_uuid(self, obj):
        return obj.ticket.uuid

    search_fields = ('ticket_uuid',)
