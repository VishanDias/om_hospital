from odoo import models, fields, api
from odoo.exceptions import UserError


class AppointmentPDFReportWizard(models.TransientModel):
    _name = 'appointment.pdf.report.wizard'
    _description = 'Appointment PDF Wizard'

    patient_id = fields.Many2one('hospital.patient', string='Patient')

    appointment_ids = fields.Many2many(
        'hospital.appointment',
        string='Appointments',
        compute='_compute_appointment_ids'
    )

    @api.depends('patient_id')
    def _compute_appointment_ids(self):
        for wizard in self:
            domain = []
            if wizard.patient_id:
                domain.append(('patient_id', '=', wizard.patient_id.id))

            appointments = self.env['hospital.appointment'].search(domain)

            wizard.appointment_ids = [(6, 0, appointments.ids)]

    def action_appointment_pdf_wizard_report(self):
        """Print appointment report for filtered data"""
        if not self.appointment_ids:
            raise UserError("No appointments found for the selected patient!")

        # Return the report action for the filtered appointments
        return self.env.ref('om_hospital.action_report_hospital_appointment').report_action(self.appointment_ids)