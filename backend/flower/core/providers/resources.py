from starlette.routing import Route
from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse, Response


from ..database import db
from ..models import ProviderModel
from .models import ProviderStatusTypes
from ..utils import (
    make_error, with_transaction, jwt_required, Permissions
)
from .utils import (
    is_name_unique, get_column_for_order,
)

permissions = Permissions(app_name='providers')


class Providers(HTTPEndpoint):
    @staticmethod
    @jwt_required
    @permissions.required(action=permissions.actions.GET)
    async def get(request):
        providers_query = ProviderModel.query
        total_query = db.select([db.func.count(ProviderModel.id)])

        query_params = request.query_params

        if 'name' in query_params:
            providers_query = providers_query.where(
                ProviderModel.name.ilike(f'%{query_params["name"]}%')
            )
            total_query = total_query.where(
                ProviderModel.name.ilike(f'%{query_params["name"]}%')
            )

        if 'page' in query_params and 'perPage' in query_params:
            page = int(query_params['page']) - 1
            per_page = int(query_params['perPage'])
            providers_query = providers_query.limit(
                                        per_page
                                    ).offset(page * per_page)

        if 'order' in query_params and 'field' in query_params:
            providers_query = providers_query.order_by(
                get_column_for_order(
                    query_params['field'],
                    query_params['order'] == 'ASC'
                )
            )

        total = await total_query.gino.scalar()
        providers = await providers_query.gino.all()

        return JSONResponse({
            'items': [provider.jsonify() for provider in providers],
            'total': total,
        })

    @with_transaction
    @jwt_required
    @permissions.required(action=permissions.actions.CREATE)
    async def post(self, request):
        data = await request.json()
        if not await is_name_unique(data['name']):
            return make_error('Provider already exists', status_code=400)

        if 'email' not in data and 'phone' not in data:
            return make_error('No contacts for provider', status_code=400)

        new_provider = await ProviderModel.create(
            name=data['name'],
            email=data['email'] if 'email' in data else None,
            phone=data['phone'] if 'phone' in data else None,
            status=ProviderStatusTypes.NEW,
            data=data['data'],
            address=data['address'],
        )
        return JSONResponse({'id': new_provider.id})


class Provider(HTTPEndpoint):
    @staticmethod
    @jwt_required
    @permissions.required(action=permissions.actions.GET)
    async def get(request):
        provider_id = request.path_params['provider_id']
        provider = await ProviderModel.get(provider_id)
        if provider:
            return JSONResponse(provider.jsonify(for_card=True))
        return make_error(description='Provider not found', status_code=404)

    @with_transaction
    @jwt_required
    @permissions.required(
        action=permissions.actions.UPDATE,
        additional_actions=[permissions.actions.UPDATE_STATUS],
        return_actions=True
    )
    async def patch(self, request, actions):
        data = await request.json()
        provider_id = request.path_params['provider_id']
        provider = await ProviderModel.get(provider_id)
        if not provider:
            return make_error(
                f'Provider with id {provider_id} not found', status_code=404
            )

        values = {
            'data': data['data'] if 'data' in data else None,
        }
        if 'update' in actions:
            values['name'] = data['name'] if 'name' in data else None
            values['phone'] = data['phone'] if 'phone' in data else None
            values['email'] = data['email'] if 'email' in data else None
            values['address'] = data['address'] if 'address' in data else None
        if 'update_status' in actions:
            values['status'] = (
                data['status'].upper() if 'status' in data else None
            )

        values = dict(filter(lambda item: item[1] is not None, values.items()))

        await provider.update(**values).apply()
        return Response('', status_code=204)


@jwt_required
async def get_actions(request, user):
    return JSONResponse(await permissions.get_actions(user.role_id))

routes = [
    Route('/', Providers),
    Route('/actions', get_actions, methods=['GET']),
    Route('/{provider_id:int}', Provider),
]
