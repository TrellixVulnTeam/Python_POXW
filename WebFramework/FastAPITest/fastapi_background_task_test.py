#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: fastapi_background_task_test.py
# Author: alfons
# LastChange:  2020/6/29 上午10:37
#=============================================================================
"""
import uvicorn
from typing import Optional
from fastapi import BackgroundTasks, FastAPI, Depends

app = FastAPI()


def write_log(message: str):
    with open("log.txt", mode="a") as log:
        log.write(message)


def get_query(background_tasks: BackgroundTasks, q: Optional[str] = None):
    if q:
        message = f"found query: {q}\n"
        background_tasks.add_task(write_log, message)
    return q


@app.post("/send-notification/{email}")
async def send_notification(email: str,
                            background_tasks: BackgroundTasks,
                            q: str = Depends(get_query)):
    message = f"message to {email}\n"
    background_tasks.add_task(write_log, message)
    return {"message": "Message sent"}


def main():
    uvicorn.run("fastapi_background_task_test:app", host="0.0.0.0", port=8000, workers=1)


if __name__ == '__main__':
    main()
