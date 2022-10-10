import logging

from fastapi import Depends, FastAPI

from fastapi_web_session import RedisStorage, Session, get_session

logging.basicConfig(level=logging.DEBUG)


redis = RedisStorage()
app = FastAPI(dependencies=[Depends(redis)])


@app.get("/get-session")
async def get(session: Session = Depends(get_session)):
    return {"session": f"{repr(session)}"}


@app.get("/set-session")
async def set(session: Session = Depends(get_session)):
    session["email"] = "test@amenezes.net"
    session.follow = "email"
    return {"session": f"{repr(session)}"}


@app.get("/expire-session")
async def get(session: Session = Depends(get_session)):
    session.invalidate()
    return {"session": f"{repr(session)}"}
