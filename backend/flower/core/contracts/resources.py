import asyncio
from datetime import date, datetime
from starlette.routing import Route
from starlette.endpoints import HTTPEndpoint
from starlette.background import BackgroundTask

from ..database import db
from ..models import ContractModel, PermissionAction, ContractStatus
from ..utils import (
    with_transaction, jwt_required, make_response, make_list_response,
    make_error, Permissions, GinoQueryHelper, MediaUtils, NO_CONTENT,
)

permissions = Permissions(app_name='contracts')


class Contracts(HTTPEndpoint):
    @jwt_required
    @permissions.required(action=PermissionAction.GET)
    async def get(self, request):
        data = request.query_params
        contracts_query = ContractModel.query
        total_query = db.select([db.func.count(ContractModel.id)])

        if 'startDate' in data:
            year, month, day = data['startDate'].split('-')[:3]
            contracts_query = contracts_query.where(
                ContractModel.start_date >= date(year, month, day)
            )
            total_query = total_query.where(
                ContractModel.start_date >= date(year, month, day)
            )
        if 'endDate' in data:
            year, month, day = data['endDate'].split('-')[:3]
            contracts_query = contracts_query.where(
                ContractModel.start_date <= date(year, month, day)
            )
            total_query = total_query.where(
                ContractModel.start_date <= date(year, month, day)
            )

        if 'number' in data:
            contracts_query, total_query = GinoQueryHelper.search(
                ContractModel.number,
                data['number'],
                contracts_query,
                total_query
            )

        if 'providerId' in data:
            # TODO replace with equal
            contracts_query = contracts_query.where(
                ContractModel.provider_id == int(data['providerId'])
            )
            total_query = total_query.where(
                ContractModel.provider_id == int(data['providerId'])
            )

        contracts_query = GinoQueryHelper.pagination(
            data, contracts_query
        )

        contracts_query = GinoQueryHelper.order(
            data,
            contracts_query,
            {
                'id': ContractModel.id,
                'startDate': ContractModel.start_date,
                'endDate': ContractModel.end_date,
                'status': ContractModel.status,
                'number': ContractModel.number,
                'providerId': ContractModel.provider_id,
            }
        )

        contracts = await contracts_query.gino.all()

        return make_list_response(
            [contract.jsonify() for contract in contracts],
            total=await total_query.gino.scalar()
        )

    @with_transaction
    @jwt_required
    @permissions.required(action=PermissionAction.CREATE)
    async def post(self, request):

        data = await request.json()

        start_date = self._get_date(data['startDate'])
        end_date = self._get_date(data['endDate'])
        file_base64 = data['file']
        path = await MediaUtils.save_file_base64(file_base64)

        contract = await ContractModel.create(
            number=data['number'],
            start_date=start_date,
            end_date=end_date,
            status=ContractStatus.get_by_date(start_date, end_date),
            path=path,
            provider_id=data['providerId']
        )

        # async def _manage_status(contract_id):
        #     await asyncio.sleep(
        #         (
        #             datetime.combine(start_date, datetime.min.time()) -
        #             datetime.now()
        #         ).seconds
        #     )
        #     _contract = await ContractModel.get(contract_id)
        #     if _contract.status != ContractStatus.CANCELLED:
        #         await _contract.update(
        #             status=ContractStatus.OPERATING
        #         ).apply()
        #     else:
        #         return
        #     await asyncio.sleep(
        #         (
        #             datetime.combine(end_date, datetime.min.time()) -
        #             datetime.now()
        #         ).seconds
        #     )
        #     _contract = await ContractModel.get(contract_id)
        #     if _contract.status != ContractStatus.CANCELLED:
        #         await _contract.update(
        #             status=ContractStatus.DONE
        #         ).apply()
        #
        # if contract.status == ContractStatus.NOT_STARTED:
        #     return make_response(
        #         {'id': contract.id},
        #         background=BackgroundTask(
        #             _manage_status, contract_id=contract.id
        #         )
        #     )
        return make_response({'id': contract.id})

    @staticmethod
    def _get_date(text_date):
        year, month, day = [int(i) for i in text_date.split('-')]
        return date(year, month, day)


class Contract(HTTPEndpoint):
    @jwt_required
    @permissions.required(action=PermissionAction.GET)
    async def get(self, request):
        pass

@jwt_required
async def get_actions(request, user):
    return make_response(await permissions.get_actions(user.role_id))

routes = [
    Route('/', Contracts),
    Route('/{contract_id:int}', Contract),
    Route('/actions', get_actions, methods=['GET']),
]
