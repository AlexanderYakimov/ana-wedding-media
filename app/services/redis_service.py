import redis
from redis.exceptions import RedisError
import os

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', '')

def get_files_by_tag(redis_host: str = REDIS_HOST, redis_port: int = REDIS_PORT, tag: str = "") -> list:
    """
    Returns a set of files associated with a specific tag.

    :param redis_host: Redis server hostname (default: environment variable REDIS_HOST or 'localhost').
    :param redis_port: Redis server port (default: environment variable REDIS_PORT or 6379).
    :param tag: Tag for searching files.
    :returns: A set of file names associated with the tag.
    :raises RedisError: If an error occurs while accessing Redis.
    :raises ValueError: If tag is not provided.
    """
    if not tag:
        raise ValueError("Tag parameter cannot be empty.")

    try:
        redis_client = redis.StrictRedis(
            host=redis_host,
            port=redis_port,
            password=REDIS_PASSWORD if REDIS_PASSWORD else None,
            decode_responses=True)
        files = list(redis_client.smembers(tag))
        if not files:
            print(f"No files found for tag: {tag}")
        
        return files
    except RedisError as e:
        print(f"Error accessing Redis: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise
