from abc import ABCMeta
from src.db import DbSessionManager
from src.db.models import User, Post
from src.schemas import (
    CreateUserSchema, 
    ResponseUserSchema,
    CreatePostSchema,
    ResponsePostSchema,
    Conversation, 
    ConversationMessage
)
from typing import Iterable, Optional
from sqlalchemy.exc import IntegrityError
from src.env import ENV


db_manager: DbSessionManager = DbSessionManager('sqlite:///' if ENV.test_mode else str(ENV.db))
    

class UserController:
    def find_user(self, id: int) -> Optional[ResponseUserSchema]:
        with db_manager.session() as session:
            user = session.get(User, id)
            if user is None:
                return None
            return ResponseUserSchema.model_validate(user)

    def create_user(self, data: CreateUserSchema) -> ResponseUserSchema:
        with db_manager.session() as session:
            try:
                user = User(**data.model_dump())
                session.add(user)
                session.commit()
                return ResponseUserSchema.model_validate(user)
            except IntegrityError:
                raise ValueError('User already exists')
    

class PostController:
    def create_post(self, data: CreatePostSchema) -> ResponsePostSchema:
        with db_manager.session() as session:
            user = session.get(User, data.tg_user_id)
            if user is None:
                raise ValueError('Invalid user_id')
            post = Post(conversation=data.conversation.model_dump()) 
            post.user = user
            user.posts.append(post)
            session.commit()
            return ResponsePostSchema.model_validate(post)
    
    def get_posts(self, user_id: int) -> Iterable[ResponsePostSchema]:
        with db_manager.session() as session:
            posts = session.query(Post).filter_by(
                tg_user_id=user_id
            ).order_by(Post.timestamp.desc()).all()
            return [ResponsePostSchema.model_validate(post) for post in posts]

    def add_message(self, post_id: int, message: ConversationMessage) -> ResponsePostSchema:
        with db_manager.session() as session:
            post = session.get(Post, post_id)
            if post is None:
                raise ValueError('Invalid post id')
            conversation = Conversation.model_validate(post.conversation)
            conversation.messages.append(message)
            post.conversation = conversation.model_dump()
            session.commit()
            return ResponsePostSchema.model_validate(post)

            