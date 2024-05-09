from pydantic import BaseModel, BeforeValidator
from typing import Optional, Annotated


class IsImageRequiredSchema(BaseModel):
    image_required: Annotated[bool, BeforeValidator(lambda x: bool(x))]
    prompt_for_text_to_image_model: Optional[str]