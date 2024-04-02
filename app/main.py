from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin
from app.database import engine
from app.admin.views import NewsAdmin, SystemAdmin, UserAdmin, RoleAdmin,StatusAdmin, OrganizationAdmin, TicketAdmin, MessagesAdmin, AttachmentsAdmin
from app.tikets.router import router as tickets_router
from app.organizations.router import router as orgs_router
from app.users.router import router as auth_router
from app.news.router import router as news_router
from app.tikets.status.router import router as status_router
from app.tikets.system.router import router as systems_router



@asynccontextmanager
async def lifespan(app: FastAPI):

    redis = aioredis.from_url("redis://localhost:6379")

    FastAPICache.init(RedisBackend(redis), prefix="cache")

    yield

app = FastAPI(
    title="Техническая поддержка МИАЦ",
    description="API для управления технической поддержкой МИАЦ",
    lifespan=lifespan
)

origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://192.168.1.147:5173",
    "http://172.27.0.5:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET","POST","PUT",],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Authorization"]
)
admin = Admin(app, engine)

app.include_router(auth_router)
app.include_router(news_router)
app.include_router(tickets_router)
app.include_router(orgs_router)
app.include_router(status_router)
app.include_router(systems_router)



admin.add_view(NewsAdmin)
admin.add_view(UserAdmin)
admin.add_view(RoleAdmin)
admin.add_view(StatusAdmin)
admin.add_view(SystemAdmin)
admin.add_view(OrganizationAdmin)
admin.add_view(TicketAdmin)
admin.add_view(MessagesAdmin)
admin.add_view(AttachmentsAdmin)