from app.users.models import User
from app.attachments.models import Attachments
from app.messages.models import Messages
from app.organizations.models import Organization
from app.roles.models import Roles
from app.status.models import Status
from app.tikets.models import Ticket
from app.users.dao import UserDAO
from sqladmin import ModelView
from wtforms import PasswordField, StringField 



class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.login, User.password, User.surname, User.name, User.secname,
                   User.post, User.organization, User.role, User.email, User.contact_tel]
    column_details_exclude_list = [User.created_messages, User.created_tickets,
                                   User.assigned_tickets, User.organization_id, User.role_id]
    form_excluded_columns = ['created_messages', 'created_tickets', 'assigned_tickets']
    form_overrides = dict(password=PasswordField)                               
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-users"



class RoleAdmin(ModelView, model=Roles):
    column_list = [Roles.id, Roles.description]
    form_excluded_columns = ['users']
    name = "Роль"
    name_plural = "Роли"
    icon = "fa-solid fa-user-secret"

class StatusAdmin(ModelView, model=Status):
    column_list = [Status.id, Status.description]
    form_excluded_columns = ['tickets']
    name = "Статус"
    name_plural = "Статусы"
    icon = "fa-solid fa-hourglass-start"

class OrganizationAdmin(ModelView, model=Organization):
    column_list = [Organization.id, Organization.lpucode, Organization.name]
    form_excluded_columns = ['tickets', 'users']
    name = "Организация"
    name_plural = "Организации"
    icon = "fa-solid fa-sitemap"

class TicketAdmin(ModelView, model=Ticket):
    column_list = '__all__'
    name = "Заявка"
    name_plural = "Заявки"
    icon = "fa-solid fa-ticket"

class MessagesAdmin(ModelView, model=Messages):
    column_list = [Messages.creator, Messages.ticket_id, Messages.content, Messages.created_at]
    name = "Сообщение"
    name_plural = "Сообщения"
    icon = "fa-solid fa-commenting"

class AttachmentsAdmin(ModelView, model=Attachments):
    column_list = '__all__'
    #form_overrides = dict(file_data=wtforms.FileField)
    name = "Файл"
    name_plural = "Файлы"
    icon = "fa-solid fa-folder"