from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fastapi_zero.routers import auth, users

app = FastAPI()
app.include_router(users.routers)
app.include_router(auth.routers)


@app.get('/', status_code=HTTPStatus.OK, response_class=HTMLResponse)
def inicio():
    return """
        <html>
            <head></head>
            <body>
                <h1>Ola mundo!</h1>
            </body>
        </html>
"""
