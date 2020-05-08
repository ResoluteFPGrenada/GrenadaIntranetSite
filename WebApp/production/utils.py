import os
import smtplib
from flask import url_for, current_app

def send_log(message, log_type):
    log_path = os.path.join(current_app.root_path, 'static/logs/', log_type + '.log')
    file = open(log_path, 'a')
    file.write(message)
    file.write(os.linesep)
    file.close()

def email_mill_log_reports(data):

    body = """MIME-Version: 1.0
Content-type: text/html
Subject: Mill Log Reports {}
<h3>Mill Logs entered on {}</h3>
<table style="font-size: 120%; border-collapse: collapse; border: 1px solid black;">
    <thead>
        <tr>
            <th style="border: 1px solid black;">Id</th>
            <th style="border: 1px solid black;">User</th>
            <th style="border: 1px solid black;">Date</th>
            <th style="border: 1px solid black;">Time</th>
            <th style="border: 1px solid black;">Supervisor</th>
            <th style="border: 1px solid black;">Event Location</th>
            <th style="border: 1px solid black;">Event Type</th>
            <th style="border: 1px solid black;">Comment</th>
        </tr>
    </thead>
    <tbody>""".format(data['date'], data['date'])
    for log in data['logs']:
        body += """<tr>
                    <td style="border: 1px solid black;">{}</td>
                    <td style="border: 1px solid black;">{}</td>
                    <td style="border: 1px solid black;">{}</td>
                    <td style="border: 1px solid black;">{}</td>
                    <td style="border: 1px solid black;">{}</td>
                    <td style="border: 1px solid black;">{}</td>
                    <td style="border: 1px solid black;">{}</td>
                    <td style="border: 1px solid black;">{}</td>
                    </tr>""".format(log['id'],
                                    log['user'],
                                    log['date'],
                                    log['time'],
                                    log['supervisor'],
                                    log['location'],
                                    log['type'],
                                    log['comment'])

    body += """</tbody></table> """

    Sender = 'MillLog.Reports@resolutefp.com'
    Receiver = 'gremilllogdata@resolutefp.com','jason.hodges@resolutefp.com'
    #Receiver = 'jason.hodges@resolutefp.com'
    s = smtplib.SMTP('smtp.cacc.local')
    s.sendmail(Sender, Receiver, body)
    s.quit()

def send_AE_email(data):
    body = """MIME-Version: 1.0
Content-type: text/html
Subject: Submitted AE Comments
Please review these comments before entering into AE Report
<h3>General:</h3>
    {}

<h3>Safety:</h3> 
    {}

<h3>Environment:</h3>
    {}

<h3>Quality / Paper Loss:</h3>
    {}

<h3>Downtime / Loss Time:</h3>
    {}

<h3>Paper Machine:</h3>
    {}

<h3>TMP:</h3>
    {}

<h3>Utilities:</h3>
    {}

<h3>Woodyard:</h3>
    {}

<h3>Customer Service:</h3>
    {}

<h3>Shipping / Finishing:</h3>
    {}

<h3>Inventory:</h3>
    {}


""".format(data['general'], data['safety'], data['environment'],
           data['quality'], data['downtime'], data['pm'], data['tmp'],
           data['utilities'], data['woodyard'], data['customer_service'],
           data['fs'], data['inventory'])

    Sender = 'AEComments@resolutefp.com'
    Receiver = 'dwight.devall@resolutefp.com'
    s = smtplib.SMTP('smtp.cacc.local')
    s.sendmail(Sender, Receiver, body)
    s.quit()
