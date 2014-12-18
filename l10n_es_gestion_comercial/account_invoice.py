# -*- coding: utf-8 -*-
################################################################
#    License, author and contributors information in:          #
#    __openerp__.py file at the root folder of this module.    #
################################################################

from osv import fields, osv, orm
from tools.translate import _
import logging


class account_invoice(osv.osv):
    _name = "account.invoice"
    _inherit = "account.invoice"

    def _has_received_check(self, cr, uid, ids, field_name=None,
                            field_value=None, arg=None, context=None):
#         logger = logging.getLogger(__name__)
#         logger.debug('>>>>>>> ids: {}'.format(ids))
        res = {}
        invoices = self.browse(cr, uid, ids, context=context)
        
        if not invoices:
            return res
            
        for invoice in invoices:
            received_check = False
            move_line_obj = self.pool.get('account.move.line')
            move_line_ids = move_line_obj.search(
                 cr, uid, ['|',
                           ('invoice', '=', invoice.id),
                           ('move_id.id', '=', invoice.move_id.id)])
            move_lines = move_line_obj.browse(cr, uid, move_line_ids,
                                              context=context)
            if any(move_line.received_check for move_line in move_lines):
                received_check = True
            res[invoice.id] = received_check
        return res

    _columns = {
        'received_check' : fields.function(
            _has_received_check,
            type='boolean',
            obj="account.invoice",
            readonly=False,
            method=True,
#             store=True,
            string='Received check',),
        'received_check_dummy': fields.related(
            'received_check',
            type="boolean",
            readonly=True,
            string='Received check',)
    }

    _defaults = {  
        'received_check': _has_received_check
    }
    
account_invoice()
