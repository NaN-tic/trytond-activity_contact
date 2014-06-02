# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import ModelSQL, fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval

__all__ = ['ActivityParty', 'Activity']
__metaclass__ = PoolMeta


class ActivityParty(ModelSQL):
    'Activity'
    __name__ = "activity.activity-party.party"

    activity = fields.Many2One('activity.activity', 'Activity',
        required=True, select=True, ondelete='CASCADE')
    party = fields.Many2One('party.party', 'Party', required=True, select=True)


class Activity:
    'Activity'
    __name__ = "activity.activity"

    allowed_contacts = fields.Function(fields.Many2Many('party.party',
            None, None, 'Allowed Contacts'),
        'on_change_with_allowed_contacts')
    contacts = fields.Many2Many('activity.activity-party.party', 'activity',
        'party', 'Contacts',
        domain=[
            ('id', 'in', Eval('allowed_contacts', [])),
            ],
        depends=['allowed_contacts'])

    @fields.depends('party')
    def on_change_with_allowed_contacts(self, name=None):
        pool = Pool()
        Employee = pool.get('company.employee')
        res = [e.party.id for e in Employee.search([])]
        if not self.party:
            return res
        res.extend(r.to.id for r in self.party.relations)
        return res
