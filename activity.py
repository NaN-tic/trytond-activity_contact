# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import ModelSQL, fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval

__all__ = ['ActivityParty', 'Activity']


class ActivityParty(ModelSQL, metaclass=PoolMeta):
    'Activity'
    __name__ = "activity.activity-party.party"

    activity = fields.Many2One('activity.activity', 'Activity',
        required=True, ondelete='CASCADE')
    party = fields.Many2One('party.party', 'Party', required=True)


class Activity(metaclass=PoolMeta):
    'Activity'
    __name__ = "activity.activity"

    allowed_contacts = fields.Function(fields.Many2Many('party.party',
            None, None, 'Allowed Contacts',
            context={
                'company': Eval('company'),
            },
            depends=['company']),
        'on_change_with_allowed_contacts')
    contacts = fields.Many2Many('activity.activity-party.party', 'activity',
        'party', 'Contacts', domain=[
            ('id', 'in', Eval('allowed_contacts', [])),
            ],
        context={
            'company': Eval('company'),
            },
        depends=['allowed_contacts', 'company'])

    @fields.depends('party', methods=['on_change_with_party'])
    def on_change_with_allowed_contacts(self, name=None):
        pool = Pool()
        Employee = pool.get('company.employee')

        res = [e.party.id for e in Employee.search([])]
        self.party = self.on_change_with_party()
        if not self.party or self.party.id < 0:
            return res
        res.extend(r.to.id for r in self.party.relations)
        return res
