from uuid import UUID

from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel, Field
from sqlalchemy import select

from forgeai_api.api.deps import get_request_runtime
from forgeai_api.models import Job, Repository, Run

router = APIRouter(prefix="/runs", tags=["runs"])


class RunCreate(BaseModel):
    repository_id: UUID
    request: str = Field(min_length=1)


class RunResponse(BaseModel):
    id: UUID
    repository_id: UUID
    status: str
    request: str


class RunListResponse(BaseModel):
    items: list[RunResponse]


@router.post("", response_model=RunResponse, status_code=status.HTTP_201_CREATED)
async def create_run(payload: RunCreate, request: Request) -> RunResponse:
    runtime = get_request_runtime(request)
    async with runtime.session_factory() as session:
        repository = await session.get(Repository, payload.repository_id)
        if repository is None:
            raise HTTPException(status_code=404, detail="repository not found")

        run = Run(repository_id=payload.repository_id, request=payload.request)
        run.jobs.append(Job(job_type="run", status="queued"))
        session.add(run)
        await session.flush()
        job = run.jobs[0]
        await session.commit()

    await runtime.redis.rpush("forgeai:jobs", str(job.id))
    return RunResponse.model_validate(run, from_attributes=True)


@router.get("", response_model=RunListResponse)
async def list_runs(request: Request) -> RunListResponse:
    runtime = get_request_runtime(request)
    async with runtime.session_factory() as session:
        result = await session.scalars(select(Run).order_by(Run.created_at.desc()))
        runs = result.all()
    return RunListResponse(
        items=[RunResponse.model_validate(run, from_attributes=True) for run in runs]
    )


@router.get("/{run_id}", response_model=RunResponse)
async def get_run(run_id: UUID, request: Request) -> RunResponse:
    runtime = get_request_runtime(request)
    async with runtime.session_factory() as session:
        run = await session.get(Run, run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="run not found")
    return RunResponse.model_validate(run, from_attributes=True)
