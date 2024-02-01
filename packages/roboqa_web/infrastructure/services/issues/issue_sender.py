from roboqa_web.application.issues.services.issue_publisher import IssueSender
from roboqa_web.infrastructure.worker.tasks import issue_publish_gh_task


class WorkerIssueSender(IssueSender):

    def issue_registered(self, issue_id: str) -> None:
        issue_publish_gh_task.send(issue_id)
