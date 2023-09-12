from project.models.model import Model
from project.utils.error import BadRequest, HttpStatus
from typing import Any
from project.utils.paginate import paginated


@paginated
def get_all_models() -> tuple[list[dict[str, Any]], HttpStatus]:
    result = Model.query.all()
    result = [model.to_dict() for model in result]
    if not len(result):
        raise BadRequest('No models')
    return result, HttpStatus.OK


def get_model_by_id(id: int) -> tuple[dict[str, Any], HttpStatus]:
    result = Model.query.filter_by(id=id).first()
    if not result:
        raise BadRequest('No model')
    return result.to_dict(), HttpStatus.OK