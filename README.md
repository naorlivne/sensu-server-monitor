## sensu server monitor

simple container that monitors sensu /info API and emails in case it fails twice in a row, designed to answer the age old questions of who watches the watchers?. 

set  the following envvars when running the container:

1. `MAIL_FROM` = the from mail address
2. `MAIL_TO` = the email address to send alerts to
3. `SENSU_HOST` = the sensu host fqdn\ip
4. `SENSU_PORT` = the sensu host port
5. `CHECK_TIMEOUT` = time to wait check attempts

after sending an alert email the container will wait 10 times the CHECK_TIMEOUT or 10 minutes (the bigger of the two) before checking again and re-alerting if needed.