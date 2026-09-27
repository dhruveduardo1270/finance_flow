from flask import Flask, redirect, url_for
import os
from database import db
from flask_login import LoginManager
from routes.dashboard import dashboard_bp
from routes.transactions import transactions_bp
from routes.categories import categories_bp
from routes.auth import auth_bp
from models import User

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'uma_chave_secreta_muito_segura_aqui'
    
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'financeflow.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    # Configurar Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Por favor, faça login para acessar esta página."
    login_manager.login_message_category = "danger"
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(transactions_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(auth_bp)
    
    with app.app_context():
        db.create_all()
        seed_data()
        
    return app

def seed_data():
    from models import Category, User
    
    # Criar um usuário padrão se não existir
    if not User.query.first():
        admin = User(username='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Usuário padrão criado: admin / admin123")

    if not Category.query.first():
        default_categories = [
            Category(name="Salário", color="#4CAF50", type="income"),
            Category(name="Freelance", color="#8BC34A", type="income"),
            Category(name="Alimentação", color="#F44336", type="expense"),
            Category(name="Transporte", color="#FF9800", type="expense"),
            Category(name="Moradia", color="#795548", type="expense"),
            Category(name="Saúde", color="#E91E63", type="expense"),
            Category(name="Lazer", color="#9C27B0", type="expense")
        ]
        db.session.bulk_save_objects(default_categories)
        db.session.commit()
        print("Banco de dados populado com categorias padrão!")

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
