import json

from starlette.routing import Route
from starlette.endpoints import HTTPEndpoint


from ..database import db
from ..models import ProviderModel
from .models import ProviderStatusTypes
from ..utils import (
    make_error, with_transaction, jwt_required, Permissions, GinoQueryHelper,
    make_list_response, make_response, NO_CONTENT
)
from .utils import (
    is_name_unique,
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

        if 'id' in query_params:
            ids = json.loads(query_params['id'])
            current_query, total_query = GinoQueryHelper.in_(
                providers_query,
                total_query,
                ProviderModel.id,
                ids
            )

        if 'name' in query_params:
            providers_query, total_query = GinoQueryHelper.search(
                ProviderModel.name,
                query_params["name"],
                providers_query,
                total_query
            )

        providers_query = GinoQueryHelper.pagination(
            query_params, providers_query
        )
        providers_query = GinoQueryHelper.order(
            query_params,
            providers_query, {
                'id': ProviderModel.id,
                'name': ProviderModel.name,
                'status': ProviderModel.status,
            }
        )

        total = await total_query.gino.scalar()
        providers = await providers_query.gino.all()

        return make_list_response(
            [provider.jsonify() for provider in providers],
            total
        )

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
        return make_response({'id': new_provider.id})


class Provider(HTTPEndpoint):
    @staticmethod
    @jwt_required
    @permissions.required(action=permissions.actions.GET)
    async def get(request):
        provider_id = request.path_params['provider_id']
        provider = await ProviderModel.get(provider_id)
        if provider:
            return make_response(provider.jsonify(for_card=True))
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
        return NO_CONTENT


@jwt_required
async def get_actions(request, user):
    return make_response(await permissions.get_actions(user.role_id))

routes = [
    Route('/', Providers),
    Route('/actions', get_actions, methods=['GET']),
    Route('/{provider_id:int}', Provider),
]
