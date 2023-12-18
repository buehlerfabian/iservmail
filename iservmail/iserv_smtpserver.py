import smtpd
import asyncore
import email
from iservconnection import IservConnection


class IservSMTPServer(smtpd.SMTPServer):

    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        msg = email.message_from_bytes(data)

        with IservConnection() as con:
            success = con.send_mail(
                receiver=rcpttos,
                subject=msg['Subject'],
                body=msg.get_payload(decode=True).decode()
            )
            if not success:
                return '550 Mail could not be sent'


def run():
    IservSMTPServer(('127.0.0.1', 1025), None)
    asyncore.loop()


if __name__ == '__main__':
    run()
