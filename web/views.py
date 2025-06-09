# web/views.py

import logging

from infrastructure.db_lead_repo import DjangoLeadRepository
from infrastructure.email_notifier import EmailNotifier
from services.lead_creator import LeadCreator

logger = logging.getLogger(__name__)


def create_lead_view(request):
    name = request.POST["name"]
    email = request.POST["email"]

    creator = LeadCreator(
        repo=DjangoLeadRepository(),
        notifier=EmailNotifier()
    )
    creator.create_lead(name, email)
    logger.info("Lead saved")
    return True
