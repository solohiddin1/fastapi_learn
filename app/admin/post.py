from sqladmin import ModelView
from app.db.models.post import Post

class PostAdmin(ModelView, model=Post):
    column_list = ['id', 'title']