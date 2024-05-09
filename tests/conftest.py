from typing import Generator
import pytest
from src.db.controllers import db_manager
from src.db.models import Post, User
from src.schemas import Conversation, ConversationMessage


@pytest.fixture(scope='class')
def db_with_test_user(request: pytest.FixtureRequest) -> Generator[None, None, None]:
    try:
        db_manager.create_tables()
        with db_manager.session() as session:
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
        db_manager.drop_tables()