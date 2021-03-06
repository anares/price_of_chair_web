from flask import Blueprint, render_template, request, json, redirect, url_for

from src.models.stores.store import Store
import src.models.users.decorators as user_decorators

stores_blueprint = Blueprint('stores', __name__)


@stores_blueprint.route('/')
def index():
    stores = Store.all()
    return render_template('stores/store_index.html', stores=stores)


@stores_blueprint.route('/store/<string:store_id>')
def store_page(store_id):
    return render_template('stores/store.html', store=Store.get_by_id(store_id))


@stores_blueprint.route('/edit/<string:store_id>', methods=['GET', 'POST'])
@user_decorators.requires_admin_permissions
def edit_store(store_id):
    store = Store.get_by_id(store_id)
    if request.method == 'POST':
        store.name = request.form['name']
        store.url_prefix = request.form['url_prefix']
        store.tag_name = request.form['tag_name']
        store.query = json.loads(request.form['query'])
        store.save_to_db()
        return redirect(url_for('.index'))

    return render_template('stores/edit_store.html', store=store)


@stores_blueprint.route('/delete/<string:store_id>', methods=['GET'])
@user_decorators.requires_admin_permissions
def delete_store(store_id):
    Store.get_by_id(store_id).delete()
    return redirect(url_for('stores.index'))


@stores_blueprint.route('/new', methods=['GET', 'POST'])
@user_decorators.requires_admin_permissions
def create_store():
    if request.method == 'POST':
        name = request.form['name']
        url_prefix = request.form['url_prefix']
        tag_name = request.form['tag_name']
        query = json.loads(request.form['query'])
        Store(name, url_prefix, tag_name, query).save_to_db()
        return redirect((url_for('stores.index')))
    return render_template('stores/new_store.html')


