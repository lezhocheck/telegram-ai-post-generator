from src.inference import openai_client
from src.schemas import ConversationMessage, Conversation, IsImageRequiredSchema
from src.env import ENV
import logging


class GptInferenceApi:
    def __init__(self) -> None:
        with open(ENV.prompts.gpt_post_text_path) as file:
            self._post_text_prompt = file.read()
        with open(ENV.prompts.gpt_image_required_path) as file:
            self._image_required_prompt = file.read()

    async def generate_post_text(self, conversation: Conversation) -> str:
        prompt = conversation.model_copy(deep=True)
        prompt.messages.insert(0, ConversationMessage(
            role='system',
            content=self._post_text_prompt
        ))
        prompt = prompt.model_dump()
        completion = await openai_client.chat.completions.create(
            model=ENV.gpt_inference_model,
            n=1,
            messages=prompt['messages']
        )
        return completion.choices[0].message.content
    
    async def is_image_asked(self, conversation: Conversation) -> IsImageRequiredSchema:
        user_messages = [i for i in conversation.messages if i['role'] == 'user']
        if not len(user_messages):
            raise ValueError('No user messages')
        user_messages.insert(0, {'role': 'system', 'content': self._image_required_prompt})
        completion = await openai_client.chat.completions.create(
            model=ENV.gpt_inference_model,
            n=1,
            messages=user_messages
        )
        answer = completion.choices[0].message.content
        try:
            return IsImageRequiredSchema.model_validate_json(answer)
        except Exception as e:
            logging.error(f'Model estimation is not correct.\n' 
                f'Received an exception {e} on anwer {answer}.'
            )
            return IsImageRequiredSchema(
                image_required=False,
                prompt_for_text_to_image_model=None
            )

