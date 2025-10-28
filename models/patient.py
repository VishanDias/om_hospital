from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread']
    _description = 'Hospital Patient'

    name = fields.Char(string="Name", required=True, tracking=True)
    date_of_birth = fields.Date(string="DOB", tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender", tracking=True)

    tag_ids = fields.Many2many('patient.tag', string="Tags")
    product_ids = fields.Many2many('product.product', string="Products")

    is_minor = fields.Boolean(string='Minor')
    guardian = fields.Char(string='Guardian')
    weight = fields.Float(string='Weight')

    # def unlink(self):
    #     for rec in self:
    #         domain = [('patient_id', '=', rec.id)]
    #         appointments = self.env['hospital.appointment'].search(domain)
    #         if appointments:
    #             raise ValidationError(_("You can' delete the patient now." "\nAppointments existing for this patient:  %s" % rec.name))
    #     return super().unlink() #if patient has assigned appointments restrict and show error for user

    @api.ondelete(at_uninstall=False) #ondelete decorator using same as unlink
    def _check_patient_appointments(self):
        for rec in self:
            domain = [('patient_id', '=', rec.id)]
            appointments = self.env['hospital.appointment'].search(domain)
            if appointments:
                raise ValidationError(_("You can' delete the patient now." "\nAppointments existing for this patient:  %s" % rec.name))