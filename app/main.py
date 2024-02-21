from fastapi import FastAPI
from sqladmin import Admin
from app.database import engine
from app.admin.views import NewsAdmin, PeriodAdmin, SystemAdmin, UserAdmin, RoleAdmin,StatusAdmin, OrganizationAdmin, TicketAdmin, MessagesAdmin, AttachmentsAdmin
from app.tikets.router import router as tickets_router
from app.organizations.router import router as orgs_router
from app.users.router import router as auth_router
from app.news.router import router as news_router



app = FastAPI()
admin = Admin(app, engine)

app.include_router(auth_router)
app.include_router(news_router)
app.include_router(tickets_router)
app.include_router(orgs_router)



admin.add_view(NewsAdmin)
admin.add_view(UserAdmin)
admin.add_view(RoleAdmin)
admin.add_view(StatusAdmin)
admin.add_view(SystemAdmin)
admin.add_view(OrganizationAdmin)
admin.add_view(TicketAdmin)
admin.add_view(MessagesAdmin)
admin.add_view(AttachmentsAdmin)
admin.add_view(PeriodAdmin)