import logging
from .clients import get_popular_movies_from_django

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def update_popular_cache(app_state):
    logger.info("Background task: updating popular cache...")
    data = await get_popular_movies_from_django()
    if data:
        app_state.popular_cache = data
        logger.info(f"Cache updated: {len(data)} movies")
    else:
        logger.warning("Failed to get popular movies from Django")
