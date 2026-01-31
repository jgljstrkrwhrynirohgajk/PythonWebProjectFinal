from app import db
from sqlalchemy import text


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    productname = db.Column(db.String(128), nullable=False)
    barcode = db.Column(db.String(128), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(128))
    description = db.Column(db.String(128))


def getAllProduct():
    sql = text("""
    SELECT p.*, c.categoryname FROM product p
    INNER JOIN category c ON p.category_id = c.id
    """)
    result = db.session.execute(sql)
    rows = [dict(row._mapping) for row in result]
    return rows


def getProductbyId(product_id: int):
    sql = text("""
        SELECT p.*, c.categoryname FROM product p
        INNER JOIN category c ON p.category_id = c.id
        where p.id = :product_id
        """)

    result = db.session.execute(
        sql,
        {
            'product_id': int(product_id)
        }
    ).fetchone()
    if result:
        return dict(result._mapping)

    return {"error": "Product not found"}