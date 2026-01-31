from app import db
from sqlalchemy import text


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    categoryname = db.Column(db.String(128), unique=True, nullable=False)

def getCategoryList():
    sql = text("SELECT * FROM category")
    result = db.session.execute(sql)
    rows = [dict(row._mapping) for row in result]
    return rows