from dramatiq import Broker

from roboqa_web.application.issues.services.issue_publisher import IssueSender
from roboqa_web.runners.worker.runner import issue_publish_gh_task


class WorkerIssueSender(IssueSender):

    def __init__(self, broker: Broker):
        self._broker = broker

    def registered(self, issue_id: str) -> None:
        issue_publish_gh_task.send(issue_id)
