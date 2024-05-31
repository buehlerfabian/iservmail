import asyncio
import email
from aiosmtpd.controller import Controller
from iservconnection import IservConnection


class IservHandler:

    async def handle_DATA(self, server, session, envelope):
        msg = email.message_from_bytes(envelope.content)

        with IservConnection() as con:
            success = con.send_mail(
                receiver=envelope.rcpt_tos,
                subject=msg['Subject'],
                body=msg.get_payload(decode=True).decode()
            )
            if not success:
                return '550 Mail could not be sent'
        return '250 Message accepted for delivery'


def run():
    loop = asyncio.get_event_loop()
    handler = IservHandler()
    controller = Controller(handler, hostname='127.0.0.1', port=1025)
    controller.start()

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        controller.stop()


if __name__ == '__main__':
    run()
