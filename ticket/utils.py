choices = {
    'status': {
        'created': 1,
        'inprogress': 2,
        'assigned': 3,
        'resolved': 4,
        'reopen': 5,
        'closed': 6
    },
    'category': {
        'payment': 1,
        'loan': 2,
        'others': 3
    },
    'department': {
        'it': 1,
        'sales': 2,
        'operation': 3,
        'hr': 4
    }
}


class SearchPattern:
    def __init__(self):
        self.choices = choices

    def in_choices(self, txt):
        res = {}
        for key, value in self.choices.items():
            for val in value:
                if txt in val:
                    res[key] = value[val]
                    return res
