from odoo import api, fields, models
import base64
from io import BytesIO
from openpyxl import Workbook

class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _inherit = ['mail.thread']
    _description = 'Hospital Appointment'
    _rec_names_search = ['reference', 'patient_id']
    _rec_name = 'patient_id'

    reference = fields.Char(string="Reference", default="New")
    patient_id = fields.Many2one('hospital.patient', stirng="Patient", on_delete="cascade") #on_delete="cascade" use for enable cascade, on_delete="restrict" use for restrict the delete
    date_of_birth = fields.Date(related='patient_id.date_of_birth')
    appointment_line_ids = fields.One2many('hospital.appointment.line', 'appointment_id', string='Lines')
    date_appointment = fields.Date(string="Date")
    note = fields.Text(string="Note")
    state = fields.Selection(
        [('draft', 'Draft'), ('confirmed', 'Confirmed'), ('ongoing', 'Ongoing'), ('done', 'Done'), ('cancel', 'Cancelled')],
        default='draft', tracking=True
    )
    total_qty = fields.Float(compute='_compute_total_qty', string='Total Quantity', store=True
                             )

    @api.model_create_multi
    def create(self, vals_list):
        print("odoo mates", vals_list)
        for vals in vals_list:
            if not vals.get('reference') or vals['reference'] == 'New':
                vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
        return super().create(vals_list)


    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"[{rec.reference}] {rec.patient_id.name}"

    @api.depends('appointment_line_ids', 'appointment_line_ids.qty')
    def _compute_total_qty(self):
        for rec in self:
            total_qty = 0
            print(sum(rec.appointment_line_ids.mapped('qty'))) # this aloso correct
            for line in rec.appointment_line_ids:
                print("Line value", line.qty)
                total_qty = total_qty + line.qty
            rec.total_qty = total_qty

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirmed'

    def action_ongoing(self):
        for rec in self:
            rec.state = 'ongoing'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    def action_export_excel(self):
        appointments = self or self.env['hospital.appointment'].search([])

        wb = Workbook()
        ws = wb.active
        ws.title = 'Appointments'

        headers = ['Reference', 'Patient', 'Data']
        ws.append(headers)

        for rec in appointments:
            ws.append([
                rec.reference or '',
                rec.patient_id.name or '',
                str(rec.date_appointment or ''),
            ])

        stream = BytesIO()
        wb.save(stream)
        stream.seek(0)
        data = base64.b64encode(stream.read())

        export_file = self.env['ir.attachment'].create({
            'name': 'appointments.xlsx',
            'type': 'binary',
            'datas': data,
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        })

        return {
            'type': 'ir.actions.act_url',
            'url': f"/web/content/{export_file.id}?download=true",
            'target': 'new',
        }