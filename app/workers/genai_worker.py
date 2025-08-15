import logging
import json
import asyncio

from app.core.celery_conf import celery_app


# Logger
logger = logging.getLogger(__name__)


@celery_app.task(
    acks_late=True,
    #auto_retry_for=(Exception,),
    #default_retry_delay=60,
)
def genai_chatbot(
    collection_id: str,
    query: str,
    user_id: int,
):
    """
    Main task to notify when a process has failed
    """
    try:
        print(f"Processing query: {query} for collection_id: {collection_id} by user_id: {user_id}")
        asyncio.run(send_message(
            collection_id=collection_id,
            user_id=user_id,
        ))

    except Exception as e:
        logger.exception(f"Error processing query: {query} for collection_id: {collection_id} by user_id: {user_id}")
        return {"status": "error", "message": str(e)}
    

async def send_message(
    collection_id: str,
    user_id: int,
):
    
    return {"status": "success", "message": "Message sent successfully"}


# Run the async function

    
