# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request, route


class ControllerMaterial(http.Controller):

    def mapping_data_materials(self, materials):
        return [
            {
                'id': material.id, 
                'material_name': material.material_name, 
                'material_code': material.material_code, 
                'material_type': material.material_type, 
                'material_buy_price': material.material_buy_price, 
                'related_supplier': material.related_supplier.id
            } for material in materials
        ]
    
    @http.route('/v1/master/materials/', type='json', auth='public', methods=['GET'])
    def get_materials(self):
        material_ids = request.env['master.material'].sudo().search([])
        if not material_ids: return {'error': 'Data tidak ditemukan'}
        result = self.mapping_data_materials(material_ids)
        return result

    @http.route('/v1/master/materials/type/', type='json', auth='public', methods=['POST'])
    def get_materials_by_type(self):
        param = request.jsonrequest
        material_type = param.get('material_type') 
        domain_data = [('material_type','=',material_type)] if material_type else []
        material_ids = request.env['master.material'].sudo().search(domain_data)
        if not material_ids: return {'error': 'Data tidak ditemukan'}
        result = self.mapping_data_materials(material_ids)
        return result
    
    @route('/v1/master/materials/<int:id_material>', type='json', auth='public', methods=['PUT'])
    def update_material(self, id_material):
        vals = request.jsonrequest
        material_id = request.env['master.material'].sudo().search([('id','=', id_material)])
        if not material_id: return {'error': 'Data tidak ditemukan'}
        material_id.sudo().write(vals)
        return {
            "id": id_material, 
            "message": "Berhasil diupdate!"
        }

    @route('/v1/master/materials', type='json', auth='public', methods=['POST'])
    def create_material(self):
        vals = request.jsonrequest
        material_id = request.env['master.material'].sudo().create(vals)
        return {
            "id": material_id.id, 
            "message": "Berhasil dibuat!"
        }

    @route('/v1/master/materials/<int:id_material>', type='json', auth='public', methods=['DELETE'])
    def delete_material(self, id_material):
        material_id = request.env['master.material'].sudo().search([('id','=', id_material)])
        if not material_id: return {"error": "Data tidak ditemukan"}
        material_id.sudo().unlink()
        return {"message": "Berhasil dihapus!"}
