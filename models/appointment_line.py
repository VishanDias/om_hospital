from odoo import api, fields, models

class HospitalAppointmentLine(models.Model):
    _name = 'hospital.appointment.line'
    _description = 'Hospital Appointment Line'

    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')
    product_id = fields.Many2one('product.product', string='Product')
    qty = fields.Float(string='Quantity')