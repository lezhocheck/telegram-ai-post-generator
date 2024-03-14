from pydantic import BaseModel, validator
from typing import Optional, Any


class IsImageRequiredSchema(BaseModel):
    image_required: bool
    prompt_for_text_to_image_model: Optional[str]

    @validator('image_required', pre=True, always=True)
    def parse_bool(cls, value: Any) -> bool:
        if not isinstance(value, str):
            return bool(value) if value != '' else False
        return value