# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Materials(models.Model):
    _name = "master.material"
    _description = "Material"

    _material_type_ = [
        ("fabric", "Fabric"),
        ("jeans", "Jeans"),
        ("cotton", "Cotton"),
    ]

    material_name = fields.Char(string="Material Name", required=True)
    material_code = fields.Char(string="Material Code", required=True)
    material_type = fields.Selection(_material_type_, string="Material Type", required=True)
    material_buy_price = fields.Float(string="Buy Price", required=True)
    related_supplier = fields.Many2one("res.partner", string="Supplier", required=True)

    @api.constrains("material_buy_price")
    def constrains_material_buy_price(self):
        if self.filtered(lambda l: l.material_buy_price < 100):
            raise ValidationError(_("Harga tidak boleh kurang dari 100."))
