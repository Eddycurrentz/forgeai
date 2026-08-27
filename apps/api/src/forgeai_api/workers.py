from uuid import UUID

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from forgeai_api.models import Job, Run

JOB_QUEUE = "forgeai:jobs"


async def process_next_job(
    session_factory: async_sessionmaker[AsyncSession], redis: Redis
) -> bool:
    raw_message = await redis.lpop(JOB_QUEUE)
    if not isinstance(raw_message, (str, bytes)):
        return False

    message = raw_message.decode() if isinstance(raw_message, bytes) else raw_message
    job_id = UUID(message)
    async with session_factory() as session:
        job = await session.get(Job, job_id)
        if job is None or job.status != "queued":
            return False
        run = await session.get(Run, job.run_id)
        if run is None or run.status != "queued":
            return False

        job.status = "running"
        job.attempts += 1
        run.status = "running"
        await session.commit()

        try:
            job.status = "succeeded"
            run.status = "succeeded"
            await session.commit()
        except Exception as error:
            job.status = "failed"
            job.error = str(error)
            run.status = "failed"
            await session.commit()
            return False

    return True
