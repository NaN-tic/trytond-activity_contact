# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
try:
    from trytond.modules.activity_contact.tests.test_activity_contact import suite
except ImportError:
    from .test_activity_contact import suite

__all__ = ['suite']
