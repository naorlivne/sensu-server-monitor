import requests, os, time, smtplib
from email.mime.text import MIMEText

print "starting sensu server monitor"
mail_from = os.environ["MAIL_FROM"]
mail_to = os.environ["MAIL_TO"]
sensu_host = os.environ["SENSU_HOST"]
sensu_port = os.environ["SENSU_PORT"]
check_timeout = int(os.environ["CHECK_TIMEOUT"])
url = "http://" + sensu_host + ":" + str(sensu_port) + "/info"


def email_send(mail_to, mail_from, host):
    print "sending alert mail"
    msg = MIMEText("critical - there is a problem with the sensu server running at " + sensu_host)
    msg['From'] = mail_from
    msg['To'] = mail_to
    msg['Subject'] = "critical - there is a problem with the sensu server running at " + sensu_host
    s = smtplib.SMTP(host)
    try:
        s.sendmail(mail_from, [mail_to], msg.as_string())
        print "alert mail sent"
    except:
        print "alert mail failed to send"
    if check_timeout * 10 > 600:
        time.sleep(check_timeout * 10)
    else:
        time.sleep(600)
    s.quit()
    return

while 1 == 1:

    time.sleep(check_timeout)
    print "checking sensu server status"
    try:
        response = requests.request("GET", url)
    except:
        time.sleep(check_timeout)
        try:
            response = requests.request("GET", url)
        except:
            email_send(mail_to, mail_from, "127.0.0.1")
    redis_status = response.json()["redis"]["connected"]
    transport_status = response.json()["transport"]["connected"]
    transport_keepalives_consumers = response.json()["transport"]["keepalives"]["consumers"]
    transport_results_consumers = response.json()["transport"]["results"]["consumers"]
    if redis_status is not True or transport_status is not True or transport_keepalives_consumers < 1 or transport_results_consumers < 1:
        time.sleep(check_timeout)
        try:
            response = requests.request("GET", url)
        except:
            email_send(mail_to, mail_from, "127.0.0.1")
        if redis_status is not True or transport_status is not True or transport_keepalives_consumers < 1 or transport_results_consumers < 1:
            email_send(mail_to, mail_from, "127.0.0.1")
    else:
        print "sensu server OK"
