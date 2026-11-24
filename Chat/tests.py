from channels.testing import WebsocketCommunicator
from django.test import TestCase, override_settings

from DjangoProject.asgi import application


@override_settings(CHANNEL_LAYERS={"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}})
class ChatTests(TestCase):
    def test_pages(self):
        self.assertEqual(self.client.get("/chat/").status_code, 200)
        self.assertEqual(self.client.get("/chat/my-room/").status_code, 200)
        self.assertEqual(self.client.get("/chat/café/").status_code, 404)  # socket can't serve it

    async def test_message_reaches_everyone_in_room(self):
        a = WebsocketCommunicator(application, "/ws/chat/my-room/")
        b = WebsocketCommunicator(application, "/ws/chat/my-room/")
        self.assertTrue((await a.connect())[0])
        self.assertTrue((await b.connect())[0])
        await a.send_json_to({"message": "hi", "sender": "Ali"})
        expected = {"message": "hi", "sender": "Ali"}
        self.assertEqual(await b.receive_json_from(), expected)
        self.assertEqual(await a.receive_json_from(), expected)
        await a.disconnect()
        await b.disconnect()
