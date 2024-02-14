from fastapi import FastAPI
from sqladmin import Admin
from app.database import engine
from app.admin.views import UserAdmin, RoleAdmin,StatusAdmin, OrganizationAdmin, TicketAdmin, MessagesAdmin, AttachmentsAdmin
from app.tikets.router import router as tickets_router


app = FastAPI()
admin = Admin(app, engine)

app.include_router(tickets_router)

admin.add_view(UserAdmin)
admin.add_view(RoleAdmin)
admin.add_view(StatusAdmin)
admin.add_view(OrganizationAdmin)
admin.add_view(TicketAdmin)
admin.add_view(MessagesAdmin)
admin.add_view(AttachmentsAdmin)