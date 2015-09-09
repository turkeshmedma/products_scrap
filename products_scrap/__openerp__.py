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

{
    "name": "Products Scrap",
    "version": "1.0",
    "author": "Medma Infomatix",
    "category": "Warehouse Management",
    "website": "http://www.medma.net",
    "description": """Scrap Products from Locations/Product views directly""",
    "summary": "Scrap Products from Locations/Product views directly",
    "license": "AGPL-3",
    "depends": ["stock"],
    "demo": [],
    "data": [
        'views/stock_view.xml',
        'wizard/scrap_stock_view.xml',
    ],
    "test": [],
    "js": [],
    "css": [],
    "qweb": [],
    "installable": True,
    "auto_install": False,
    "active": True
}


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
