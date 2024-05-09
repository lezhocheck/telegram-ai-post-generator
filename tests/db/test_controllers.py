import unittest
import pytest
from src.db.controllers import UserController, PostController
from src.schemas import (
    Conversation,
    CreateUserSchema,
    CreatePostSchema,
    ResponsePostSchema,
    ConversationMessage
)


@pytest.mark.usefixtures('db_with_test_user')
class TestUserController(unittest.TestCase):
    def setUp(self) -> None:
        self._controller = UserController()

    def test_find_user(self) -> None:
        response = self._controller.find_user(1)
        self.assertEqual(response.tg_user_id, 1)
        self.assertEqual(response.tg_username, 'test_user')

    def test_create_user(self) -> None:
        user_data = CreateUserSchema(tg_user_id=2, tg_username='test_user_2', tg_chat_id=2)
        response = self._controller.create_user(user_data)
        self.assertEqual(response.tg_username, 'test_user_2')

    def test_create_existing_user(self) -> None:
        user_data = CreateUserSchema(tg_user_id=1, tg_username='test_user', tg_chat_id=1)
        with self.assertRaises(ValueError):
            self._controller.create_user(user_data)


@pytest.mark.usefixtures('db_with_test_user')
class TestPostController(unittest.TestCase):
    def setUp(self) -> None:
        self._controller = PostController()

    def test_create_post(self) -> None:
        post_data = CreatePostSchema(tg_user_id=1, conversation=Conversation(messages=[
            ConversationMessage(role='system', content='Content')
        ]))
        response = self._controller.create_post(post_data)
        self.assertIsInstance(response, ResponsePostSchema)

    def test_get_posts(self) -> None:
        responses = self._controller.get_posts(1)
        self.assertEqual(len(responses), 3)
        self.assertIsInstance(responses[0], ResponsePostSchema)

    def test_add_message(self):
        message = ConversationMessage(role='system', content='Test message')
        response = self._controller.add_message(1, message)
        self.assertIsInstance(response, ResponsePostSchema)