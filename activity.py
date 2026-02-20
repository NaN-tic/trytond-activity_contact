# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import ModelSQL, ModelView, fields, sequence_ordered
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval
from trytond.transaction import Transaction

__all__ = ['ActivityParty', 'Activity']


class ActivityParty(sequence_ordered(), ModelView, ModelSQL, metaclass=PoolMeta):
    'Activity'
    __name__ = "activity.activity-party.party"

    activity = fields.Many2One('activity.activity', 'Activity',
        required=True, ondelete='CASCADE')
    party = fields.Many2One('party.party', 'Party',
            domain=[('id', 'in', Eval('allowed_contacts', [])),],
        context={
                'company': Eval('company', -1),
            },
        depends=['allowed_contacts', 'company'],
        required=True)
    allowed_contacts = fields.Function(fields.Many2Many('party.party',
            None, None, 'Allowed Contacts',
            context={
                'company': Eval('company', -1),
            },
            depends=['company']),
        'on_change_with_allowed_contacts')
    company = fields.Many2One('company.company', "Company", required=True)

    @classmethod
    def __setup__(cls):
        super().__setup__()
        cls.__access__.add('activity')

    @fields.depends('_parent_activity.id', '_parent_activity.party', 'activity',
                     'company','party')
    def on_change_with_allowed_contacts(self, name=None):
        pool = Pool()
        Employee = pool.get('company.employee')
        res = []
        if self.activity:
            res = [e.party.id for e in Employee.search(
                ['company', '=', self.activity.company.id])]
            if self.activity.party:
                res.extend(r.to.id for r in self.activity.party.relations)
        return res

    @classmethod
    def default_company(cls):
        return Transaction().context.get('company')

class Activity(metaclass=PoolMeta):
    'Activity'
    __name__ = "activity.activity"

    contacts = fields.One2Many('activity.activity-party.party', 'activity', 'Contacts',)
