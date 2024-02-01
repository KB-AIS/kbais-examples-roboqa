from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, APIRouter
from pydantic import Field, BaseModel
from starlette import status

from roboqa_web.application.core.usecase import UseCase
from roboqa_web.application.usecases.issue_register import IssueRegisterCommand
from roboqa_web.infrastructure.web.container import ContainerApi

issues_router = APIRouter(prefix="/api/v1/issues")


class IssueRegisterReq(BaseModel):
    title: str
    author_name: Optional[str] = Field(default=None, alias="authorName")
    is_issue: Optional[bool] = Field(default=None, alias="isIssue")
    content: Optional[str] = Field(default=None)


@issues_router.post('/', status_code=status.HTTP_201_CREATED)
@inject
async def handle_issue_register(
    req: IssueRegisterReq,
    use_case: UseCase[IssueRegisterCommand, str] = Depends(Provide[ContainerApi.issue_register_uc]),
):
    issue_id = await use_case.execute(IssueRegisterCommand(
        title=req.title,
        author_name=req.author_name,
        is_issue=req.is_issue,
        content=req.content
    ))

    return {
        "issue_id": issue_id
    }
