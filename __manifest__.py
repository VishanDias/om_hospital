{
    "name": "Hospital Management System",
    "author": "Sygnus one",
    "license": "LGPL-3",
    "version": "17.0.1.1",
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "data/sequence.xml",
        "views/patient_views.xml",
        # "views/patient_readonly_views.xml",
        "views/appointment_views.xml",
        "views/appointment_line_views.xml",
        "views/patient_tag_views.xml",
        "views/account_move_views.xml",
        "views/appointment_reporting.xml",
        "views/appointment_pdf_report_wizard_view.xml",
        "report/hospital_appointment_report_template.xml",
        "report/hospital_appointment_report_view.xml",
        "views/menu.xml",
    ],
    'installable': True,
    "depends": [
        'mail',
        'product',
        'account'
    ]
}