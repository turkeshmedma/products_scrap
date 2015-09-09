# -*- encoding: utf-8 -*-
###########################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#
#    Copyright (c) 2015 Medma - http://www.medma.net
#    All Rights Reserved.
#    Medma Infomatix (info@medma.net)
#
#    Coded by: Turkesh Patel (turkesh.patel@medma.in)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api, exceptions, _
import openerp.addons.decimal_precision as dp


class StockScrap(models.TransientModel):
    _name = "stock.scrap"
    _description = "Scrap Products"

    product_id = fields.Many2one('product.product', string='Product', required=True, select=True)
    product_qty = fields.Float(string='Quantity', digits=dp.get_precision('Product Unit of Measure'), required=True, default=1)
    product_uom = fields.Many2one('product.uom', related='product_id.uom_id', string='Product Unit of Measure')
    src_location_id = fields.Many2one('stock.location', string='Location', required=True)
    location_id = fields.Many2one('stock.location', string='Location', required=True)
    restrict_lot_id = fields.Many2one('stock.production.lot', string='Lot')
    open_move = fields.Boolean(string='Open Scrap Move', help='Created Scrap Move will be opened else wizard will be closed only', default=True)

    @api.model
    def default_get(self, fields):
        """ Get default values
        """
        Location = self.env['stock.location']
        res = super(StockScrap, self).default_get(fields)

        scrap_location = Location.search([('scrap_location', '=', True)])
        if scrap_location:
            res.update({'location_id': scrap_location[0].id})
        else:
            res.update({'location_id': False})

        if self._context.get('default_src_location_id'):
            res.update({'src_location_id': self._context['active_id']})
        elif self._context.get('default_product_id'):
            product = self.env['product.product'].browse(self._context['active_id'])
            res.update({'product_id': product.id})
            res.update({'product_uom': product.uom_id.id})
        return res

    @api.multi
    def move_scrap(self):
        """ Move the scrap/damaged product into scrap location
        """
        Quant = self.env["stock.quant"]
        Move = self.env['stock.move']
        for move in self:
            if move.product_qty <= 0:
                raise osv.except_osv(_('Warning!'), _('Please provide a positive quantity to scrap.'))
            default_val = {
                'name': 'Scrap: ' + move.product_id.name,
                'product_id': move.product_id.id,
                'location_id': move.src_location_id.id,
                'product_uom_qty': move.product_qty,
                'product_uom': move.product_id.uom_id.id,
                'scrapped': True,
                'location_dest_id': move.location_id.id,
                'restrict_lot_id': move.restrict_lot_id.id,
            }
            scrap_move = Move.create(default_val)

            domain = [('qty', '>', 0)]
            quants = Quant.quants_get_prefered_domain(scrap_move.location_id,
                    scrap_move.product_id, move.product_qty, domain=domain, prefered_domain_list=[],
                    restrict_lot_id=scrap_move.restrict_lot_id and scrap_move.restrict_lot_id.id or False,
                    restrict_partner_id=scrap_move.restrict_partner_id and scrap_move.restrict_partner_id.id or False)
            Quant.quants_reserve(quants, scrap_move)
        scrap_move.action_done()

        if move.open_move:
            view = {
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'stock.move',
                'type': 'ir.actions.act_window',
                'res_id': scrap_move.id,
                'context': self._context
            }
        else:
            view = {'type': 'ir.actions.act_window_close'}

        return view


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
