from WebApp.production.utils import email_mill_log_reports
from WebApp.api.sqlite_tool import sqlite_api
from datetime import datetime, timedelta


if __name__== "__main__":

    today = datetime.today().strftime('%Y-%m-%d')
    yesterday = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
    db = "./app/WebApp/databases/logs.db"
    sql = """ SELECT * FROM MillLogs WHERE date BETWEEN '{}' and '{}' """.format(yesterday,
                                                                                 today)
    logs = sqlite_api(db, sql, 'read')

    for log in logs:
        log['log'] = log['comment'].replace('&', '&amp')
        log['comment'] = log['comment'].replace('<', '&lt')
        log['comment'] = log['comment'].replace('>', '&gt')
        log['comment'] = log['comment'].replace('”', '&quot')
        log['comment'] = log['comment'].replace('“', '&quot')
        log['comment'] = log['comment'].replace("'", '&apos')
        log['comment'] = log['comment'].replace("’", '&apos')
        log['comment'] = log['comment'].replace('—', '-')
        log['comment'] = log['comment'].replace('–', '-')
        log['comment'] = log['comment'].replace('…', '...')

    data = {
            'date' : yesterday,
            'logs' : logs
        }

    email_mill_log_reports(data)
