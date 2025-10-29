from odoo import models, fields, api
import base64
from io import BytesIO
from openpyxl import Workbook


class AppointmentReportWizard(models.TransientModel):
    _name = 'appointment.report.wizard'
    _description = 'Appointment Report Wizard'

    date_from = fields.Date(string='From Date')
    date_to = fields.Date(string='To Date')

    # Computed field to show appointments based on date range
    appointment_ids = fields.Many2many(
        'hospital.appointment',
        string='Appointments',
        compute='_compute_appointment_ids'
    )

    @api.depends('date_from', 'date_to')
    def _compute_appointment_ids(self):
        for wizard in self:
            domain = []
            if wizard.date_from:
                domain.append(('date_appointment', '>=', wizard.date_from))
            if wizard.date_to:
                domain.append(('date_appointment', '<=', wizard.date_to))

            appointments = self.env['hospital.appointment'].search(domain)
            # wizard.appointment_ids = [(6, 0, appointments.ids)]
            wizard.appointment_ids = appointments

    def action_export_excel(self):
        # Get appointments based on date range
        domain = []
        if self.date_from:
            domain.append(('date_appointment', '>=', self.date_from))
        if self.date_to:
            domain.append(('date_appointment', '<=', self.date_to))

        appointments = self.env['hospital.appointment'].search(domain)

        # Create Excel workbook
        wb = Workbook()
        ws = wb.active
        ws.title = 'Appointments Report'

        # Add headers
        headers = ['Reference', 'Patient', 'Appointment Date', 'Total Quantity']
        ws.append(headers)

        # Add data
        for appointment in appointments:
            ws.append([
                appointment.reference or '',
                appointment.patient_id.name or '',
                str(appointment.date_appointment or ''),
                str(appointment.total_qty or '')
            ])

        # Save to BytesIO stream
        stream = BytesIO()
        wb.save(stream)
        stream.seek(0)
        data = base64.b64encode(stream.read())

        # Create attachment
        export_file = self.env['ir.attachment'].create({
            'name': f'appointments_report_{fields.Date.today()}.xlsx',
            'type': 'binary',
            'datas': data,
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'res_model': self._name,
            'res_id': self.id,
        })

        # Return download action
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{export_file.id}?download=true',
            'target': 'self',
        }