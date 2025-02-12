from odoo.tests import HttpCase
import requests
import json


class TestMaterial(HttpCase):

    def setUp(self):
        super(TestMaterial, self).setUp()
        self.base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        self.supplier = self.env['res.partner'].create({
            'name': 'Test Supplier A'
        })

        self.material = self.env['master.material'].create({
            'material_name': 'Test Material Cotton',
            'material_code': 'CC-007',
            'material_type': 'cotton',
            'material_buy_price': 100.0,
            'related_supplier': self.supplier.id
        })

        self.material2 = self.env['master.material'].create({
            'material_name': 'Test Material Jeans',
            'material_code': 'JJ-005',
            'material_type': 'jeans',
            'material_buy_price': 120.0,
            'related_supplier': self.supplier.id
        })

        self.material3 = self.env['master.material'].create({
            'material_name': 'Test Material Fabric',
            'material_code': 'JJ-005',
            'material_type': 'fabric',
            'material_buy_price': 150.0,
            'related_supplier': self.supplier.id
        })


    def test_01_get_materials(self):
        """Test GET /v1/master/materials/"""
        try:
            headers = {"Content-Type": "application/json"}
            data =json.dumps({})
            response = requests.get(f'{self.base_url}/v1/master/materials/', data=data, headers=headers)
        except Exception as e:
            self.fail(f"Request failed: {e}")

        if response:
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIsInstance(data.get('result', []), list)
            self.assertTrue(any(material['id'] == self.material.id for material in data['result']))
            print("----- Test 01 - Get all materials :", self.material.id, data)

    
    def test_02_get_materials_by_type(self):
        """Test POST /v1/master/materials/type"""
        try:
            headers = {"Content-Type": "application/json"}
            data = json.dumps({"material_type": "cotton"})
            response = requests.post(f'{self.base_url}/v1/master/materials/type', data=data, headers=headers)
        except Exception as e:
            self.fail(f"Request failed: {e}")

        if response:
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIsInstance(data.get('result', []), list)
            self.assertTrue(any(material['id'] == self.material.id for material in data['result']))
            print("\n----- Test 02 - Get materials type `cotton` : ", data)


    def test_03_update_material(self):
        """Test PUT /v1/master/materials/<id>"""
        try:
            headers = {"Content-Type": "application/json"}
            data = json.dumps({"material_buy_price": 250})
            response = requests.put(f'{self.base_url}/v1/master/materials/{self.material.id}', data=data, headers=headers)
        except Exception as e:
            self.fail(f"Request failed: {e}")

        if response:
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn("result", data)
            self.assertIn("message", data["result"])
            self.assertEqual(data["result"]["message"], "Berhasil diupdate!")

            self.material.refresh()
            self.assertEqual(self.material.material_buy_price, 250.0)

        print(f"\n----- Test 03 - Update material harga normal (> 100) : {data}")


    def test_04_update_material(self):
        """Test PUT /v1/master/materials/<id>"""
        msg = ""
        old_price = self.material2.material_buy_price
        try:
            headers = {"Content-Type": "application/json"}
            data = json.dumps({"material_buy_price": 80})
            response = requests.put(f'{self.base_url}/v1/master/materials/{self.material2.id}', data=data, headers=headers)
        except Exception as e:
            self.fail(f"Request failed: {e}")

        if response:
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn("error", data)
            self.assertIn("data", data["error"])
            self.assertIn("message", data["error"]["data"])
            self.assertEqual(data["error"]["data"]["message"], "Harga tidak boleh kurang dari 100.")

            self.material2.refresh()
            self.assertEqual(self.material2.material_buy_price, old_price)
            msg = data["error"]["data"]["message"]

        print(f"\n----- Test 04- Update material harga < 100 : {msg}")


    def test_05_create_material(self):
        """Test POST /v1/master/materials"""
        try:
            headers = {"Content-Type": "application/json"}
            data = json.dumps({
                "material_name": "Test Material Jeans 2",
                "material_code": "NM456",
                "material_type": "fabric",
                "material_buy_price": 200.0,
                "related_supplier": self.supplier.id
            })
            response = requests.post(f'{self.base_url}/v1/master/materials/', data=data, headers=headers)
        except Exception as e:
            self.fail(f"Request failed: {e}")

        if response:
            data = response.json()
            self.assertIn("result", data)
            self.assertIn("message", data["result"])
            self.assertEqual(data["result"]["message"], "Berhasil dibuat!")
            print("\n----- Test 05 - Create new materials : ", data)


    def test_06_delete_material(self):
        """Test DELETE /v1/master/materials/<id>"""
        res_id = self.material.id
        response = False
        
        try:
            headers = {"Content-Type": "application/json"}
            data = json.dumps({})
            response = requests.delete(f'{self.base_url}/v1/master/materials/{res_id}', data=data, headers=headers)
        except Exception as e:
            self.fail(f"Request failed: {e}")

        if response:
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn("result", data)
            self.assertIn("message", data["result"])
            self.assertEqual(data["result"]["message"], "Berhasil dihapus!")
            deleted_material = self.env['master.material'].search([('id', '=', res_id)])
            self.assertFalse(deleted_material)
            print(f"\n\n----- Test 06 - Delete material with id {res_id}: {data}")

