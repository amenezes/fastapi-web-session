import json
from typing import Optional

from fastapi import Request, Response

from ._logger import logger
from .constants import DEFAULT_ENCODING, DEFAULT_SESSION_ID
from .session import Session


async def get_session(request: Request, response: Response) -> Session:  # type: ignore
    try:
        request.app.FASTAPI_SESSION_STORAGE
    except AttributeError:
        raise RuntimeError("Register fastapi_session in your app first.")

    storage = request.app.FASTAPI_SESSION_STORAGE
    logger.debug(repr(storage))

    cookie = request.cookies.get(DEFAULT_SESSION_ID)

    if cookie is None:
        logger.debug("Cookie does not exist creating a new Session")
        session = Session()
    else:
        logger.debug("Session already registered, loading data from storage")
        session_data: Optional[bytes] = storage.get(f"{DEFAULT_SESSION_ID}_{cookie}")
        if session_data:
            session_data_decode: dict = json.loads(
                session_data.decode(DEFAULT_ENCODING)
            )
            session = Session(
                identity=cookie,
                data=session_data_decode.get("session"),
                created=session_data_decode.get("created"),
            )
        else:
            logger.debug("Session expired, create a new one")
            session = Session()

    response.set_cookie(
        key=DEFAULT_SESSION_ID, value=f"{session.identity}", httponly=True
    )

    yield session

    if session.changed:
        if session.expired:
            logger.debug("Session expired, deleting from storage...")
            response.delete_cookie(key=DEFAULT_SESSION_ID)
            storage.delete(f"{DEFAULT_SESSION_ID}_{session.identity}", session.follow)
        else:
            logger.debug("Session changed, storing data...")
            storage.set(f"{DEFAULT_SESSION_ID}_{session.identity}", session.data())
