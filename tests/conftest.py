from typing import Generator
import pytest
from src.db import db_connection
from src.db.models import Post, User
from src.db.schemas import Conversation, ConversationMessage


@pytest.fixture(scope='class')
def db_with_test_user(request: pytest.FixtureRequest) -> Generator[None, None, None]:
    try:
        db_connection.create_tables()
        with db_connection.session() as session:
            session.begin()
            test_user = User(tg_user_id=1, tg_username='test_user', tg_chat_id=1)
            conversation = Conversation(messages=[
                ConversationMessage(role='user', content='Hello'),
                ConversationMessage(role='assistant', content='Hello')
            ])
            posts = [
                Post(tg_user_id=1, conversation=conversation.model_dump()),
                Post(tg_user_id=1, conversation=conversation.model_dump())
            ]
            test_user.posts = posts
            session.add(test_user)
            session.commit()
            request.cls.session = session
            yield
    finally:
        db_connection.drop_tables()