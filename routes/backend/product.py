from fileinput import filename

from app import app, render_template, db
import requests
from flask import request, redirect, abort, url_for, flash

from model.product import Product
from model.category import getCategoryList
from model.product import getAllProduct, getProductbyId
from flask_wtf import FlaskForm
from pathlib import Path

from werkzeug.utils import secure_filename
import uuid
import os

import config
from upload_service import save_image

@app.route('/admin/product')
def product():
    module = 'product'
    form = FlaskForm()
    products = getAllProduct()
    return render_template('backend/product/index.html', module=module, products=products, form=form)


@app.route('/admin/product/details')
def product_details():
    module = 'product'
    form = FlaskForm()
    pro_id = request.args.get('pro_id',0)
    product = getProductbyId(pro_id)
    return render_template('backend/product/view.html', module=module, product=product, form=form)


@app.route('/admin/product/form')
def form_product():
    module = 'product'
    form = FlaskForm()
    action = request.args.get('action','add')
    if action not in ['add','edit']:
        return abort(404)

    pro_id = request.args.get('pro_id',0)
    status = 'add' if action == 'add' else 'edit'
    product = None
    if status == 'edit':
        product = getProductbyId(pro_id)

    category = getCategoryList()
    return render_template('backend/product/form.html', module=module, status=status, pro_id=pro_id, product=product, category=category, form=form)


@app.route('/admin/product/delete/<int:pro_id>', methods=['POST'])
def delete_product(pro_id):
    product = Product.query.get_or_404(pro_id)
    old_image = request.form.get('old_image')

    try:
        db.session.delete(product)

        old_img = (Path('./static/uploads/' + old_image)).is_file()
        old_img_resized = (Path('./static/uploads/resized_' + old_image)).is_file()
        old_img_thumb = (Path('./static/uploads/thumb_' + old_image)).is_file()

        if old_img:
            (Path('./static/uploads/' + old_image)).unlink()
        if old_img_resized:
            (Path('./static/uploads/' + f"resized_{old_image}")).unlink()
        if old_img_thumb:
            (Path('./static/uploads/' + f"thumb_{old_image}")).unlink()

        db.session.commit()

        flash('Product deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting product.', 'error')
        app.logger.error(f'Error deleting product {pro_id}: {str(e)}')

    return redirect(url_for('product'))

@app.route('/admin/product/save', methods=['POST'])
def save_product():
    status = request.form.get('status')   # add | edit
    pro_id = request.form.get('pro_id')
    old_image = request.form.get('old_image')

    product_name = request.form.get('product_name')
    barcode = request.form.get('barcode')
    category = request.form.get('category')
    cost = request.form.get('cost')
    price = request.form.get('price')
    description = request.form.get('description')

    images = None
    file = request.files['image_path']
    filename = secure_filename(file.filename)
    images = save_image(
        file,
        app.config['UPLOAD_FOLDER'],
        app.config['ALLOWED_EXTENSIONS']
    )

    if not product_name or not price:
        flash("Product name and price are required", "error")
        return redirect(url_for('form_product', action=status, pro_id=pro_id))

    try:
        if status == 'add':
            product = Product(
                productname=product_name,
                barcode=barcode,
                category_id=category,
                cost=cost,
                price=price,
                description=description,
                image=filename
            )
            db.session.add(product)

        if status == 'edit':

            product = Product.query.get_or_404(pro_id)
            product.productname = product_name
            product.barcode = barcode
            product.category_id = category
            product.cost = cost
            product.price = price
            product.description = description
            if file:
                product.image = filename
                old_img = (Path('./static/uploads/' + old_image)).is_file()
                old_img_resized = (Path('./static/uploads/resized_' + old_image)).is_file()
                old_img_thumb = (Path('./static/uploads/thumb_' + old_image)).is_file()

                if old_img:
                    (Path('./static/uploads/' + old_image)).unlink()
                if old_img_resized:
                    (Path('./static/uploads/' + f"resized_{old_image}")).unlink()
                if old_img_thumb:
                    (Path('./static/uploads/' + f"thumb_{old_image}")).unlink()

        db.session.commit()
        flash("Product saved successfully!", "success")

    except Exception as e:
        db.session.rollback()
        app.logger.error(str(e))
        flash("Error saving product", "error")

    return redirect(url_for('product'))
