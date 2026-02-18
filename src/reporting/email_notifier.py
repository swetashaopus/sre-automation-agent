class EmailNotifier:
    def __init__(self, smtp_server, smtp_port, username, password, from_email, to_emails):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.from_email = from_email
        self.to_emails = to_emails

    def send_email(self, subject, body):
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        msg = MIMEMultipart()
        msg['From'] = self.from_email
        msg['To'] = ", ".join(self.to_emails)
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'html'))

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.sendmail(self.from_email, self.to_emails, msg.as_string())
        except Exception as e:
            print(f"Failed to send email: {e}")

    def notify_incident(self, incident_report):
        subject = f"Incident Report: {incident_report['title']}"
        body = incident_report['body']
        self.send_email(subject, body)

    def notify_health(self, health_report):
        subject = "Health Report"
        body = health_report['body']
        self.send_email(subject, body)