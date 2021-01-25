import gino.dialects.asyncpg

from datetime import date, datetime, timedelta
from sqlalchemy.sql import true, false, case, cast
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .models import ContractStatus, ContractModel


async def change_contact_statuses():
    contact_statuses = gino.dialects.asyncpg.AsyncEnum(
        'NOT_STARTED', 'OPERATING', 'CANCELLED', 'DONE', name='contractstatus'
    )
    print(f'[{datetime.now()}] Start updating statuses')
    update_case = {
        false(): cast('OPERATING', contact_statuses),
        true(): cast('DONE', contact_statuses),
    }

    status = await ContractModel.update.values({
        ContractModel.status: case(
            update_case,
            value=ContractModel.end_date < date.today()
        )
    }).where(
        (ContractModel.start_date <= date.today())
        & (ContractModel.status == ContractStatus.NOT_STARTED)
        | (ContractModel.end_date < date.today())
        & (ContractModel.status == ContractStatus.OPERATING)
    ).gino.status()
    print(f'[{datetime.now()}] End updating statuses. Result: {status[0]}')


async def startup_event():
    scheduler = AsyncIOScheduler()
    # run every day
    scheduler.add_job(
        change_contact_statuses, CronTrigger(day='*', hour=0, minute=0)
    )

    # run after startup
    current_datetime = datetime.now() + timedelta(seconds=5)

    scheduler.add_job(
        change_contact_statuses, CronTrigger(
            year=current_datetime.year,
            month=current_datetime.month,
            day=current_datetime.day,
            hour=current_datetime.hour,
            minute=current_datetime.minute,
            second=current_datetime.second
        )
    )

    scheduler.start()
