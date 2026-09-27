from flask import Blueprint, jsonify, request
from models import Category
from database import db

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/api/categories', methods=['GET'])
def get_categories():
    """API para buscar categorias. Retorna JSON para o frontend."""
    # Pode filtrar por tipo se passar na URL (ex: /api/categories?type=expense)
    cat_type = request.args.get('type')
    
    query = Category.query
    if cat_type in ['income', 'expense']:
        query = query.filter(Category.type == cat_type)
        
    categories = query.all()
    
    # Usa o método to_dict que criamos no models.py para converter o objeto Python em dicionário
    return jsonify([cat.to_dict() for cat in categories])
