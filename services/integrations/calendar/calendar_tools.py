import logging

from core.logger import get_logger

log = get_logger(__name__)

def create_calendar_event(title="Meeting"):
    log.info(f"Creating calendar event: {title}")
    return f"Calendar event created: {title}"
