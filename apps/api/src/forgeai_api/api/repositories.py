from uuid import UUID

from fastapi import APIRouter, Request, status
from pydantic import BaseModel, Field
from sqlalchemy import select

from forgeai_api.api.deps import get_request_runtime
from forgeai_api.models import Repository

router = APIRouter(prefix="/repositories", tags=["repositories"])


class RepositoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    remote_url: str | None = None
    default_branch: str = Field(default="main", min_length=1, max_length=255)


class RepositoryResponse(BaseModel):
    id: UUID
    name: str
    remote_url: str | None
    default_branch: str


class RepositoryListResponse(BaseModel):
    items: list[RepositoryResponse]


@router.post("", response_model=RepositoryResponse, status_code=status.HTTP_201_CREATED)
async def create_repository(payload: RepositoryCreate, request: Request) -> RepositoryResponse:
    runtime = get_request_runtime(request)
    async with runtime.session_factory() as session:
        repository = Repository(**payload.model_dump())
        session.add(repository)
        await session.commit()
        await session.refresh(repository)
    return RepositoryResponse.model_validate(repository, from_attributes=True)


@router.get("", response_model=RepositoryListResponse)
async def list_repositories(request: Request) -> RepositoryListResponse:
    runtime = get_request_runtime(request)
    async with runtime.session_factory() as session:
        result = await session.scalars(select(Repository).order_by(Repository.created_at.desc()))
        repositories = result.all()
    return RepositoryListResponse(
        items=[
            RepositoryResponse.model_validate(repository, from_attributes=True)
            for repository in repositories
        ]
    )
