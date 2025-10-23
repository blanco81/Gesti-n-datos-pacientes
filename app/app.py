import reflex as rx
from app.pages.index import index
from app.api import router as fastapi_router

app = rx.App(theme=rx.theme(appearance="light"))
app.add_page(index)
app.api = fastapi_router