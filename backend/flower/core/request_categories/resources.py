from starlette.responses import JSONResponse

from ..utils import jwt_required
from ..models import RequestCategoryModel


@jwt_required(return_user=False)
async def get_categories(request):
    params = request.query_params

    query = RequestCategoryModel.query
    if 'search' in params:
        query = query.where(
            RequestCategoryModel.name.ilike(f'%{params["search"]}%')
        )

    categories = query.gino.all()

    return JSONResponse({
        'categories': [category.jsonify() for category in categories]
    })


routes = [

]
