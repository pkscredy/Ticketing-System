from base.choices import Choices


class TicketStatus(Choices):
    STATUS_NOT_SET = 0
    CREATED = 1
    INPROGRESS = 2
    ASSIGNED = 3
    RESOLVED = 4
    REOPEN = 5
    CLOSED = 6


class TicketCategory(Choices):
    STATUS_NOT_SET = 0
    PAYMENT = 1
    LOAN = 2
    OTHERS = 3


class Department(Choices):
    STATUS_NOT_SET = 0
    IT = 1
    SALES = 2
    OPERATION = 3
    HR = 4
