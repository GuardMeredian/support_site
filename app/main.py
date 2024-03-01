from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin
from app.database import engine
from app.admin.views import NewsAdmin, SystemAdmin, UserAdmin, RoleAdmin,StatusAdmin, OrganizationAdmin, TicketAdmin, MessagesAdmin, AttachmentsAdmin
from app.tikets.router import router as tickets_router
from app.organizations.router import router as orgs_router
from app.users.router import router as auth_router
from app.news.router import router as news_router
from app.tikets.status.router import router as status_router
from app.tikets.system.router import router as systems_router



app = FastAPI(
    title="Техническая поддержка МИАЦ",
    description="API для управления технической поддержкой МИАЦ",
)

origins=[
    "http://localhost:5173",
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
#admin.add_view(PeriodAdmin)