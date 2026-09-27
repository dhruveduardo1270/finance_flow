from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import Transaction, Category
from database import db
from datetime import datetime

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/transactions')
@login_required
def list_transactions():
    """Rota para listar todas as transações, com filtros opcionais."""
    # Pega os parâmetros da URL (ex: ?type=expense&month=9)
    filter_type = request.args.get('type')
    
    # Inicia a query base
    query = Transaction.query.order_by(Transaction.date.desc())
    
    # Aplica filtros se existirem
    if filter_type in ['income', 'expense']:
        query = query.filter(Transaction.type == filter_type)
        
    transactions = query.all()
    return render_template('transactions.html', transactions=transactions)

@transactions_bp.route('/transactions/add', methods=['GET', 'POST'])
@login_required
def add_transaction():
    """Rota para adicionar uma nova transação. Lida tanto com o formulário (GET) quanto com o envio (POST)."""
    if request.method == 'POST':
        # Recebe os dados do formulário
        description = request.form.get('description')
        amount = float(request.form.get('amount').replace(',', '.'))
        trans_type = request.form.get('type')
        category_id = int(request.form.get('category_id'))
        date_str = request.form.get('date')
        notes = request.form.get('notes')
        
        # Converte a string de data para objeto Date
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # Cria o objeto de transação
        new_transaction = Transaction(
            description=description,
            amount=amount,
            type=trans_type,
            category_id=category_id,
            date=date_obj,
            notes=notes
        )
        
        # Salva no banco de dados
        db.session.add(new_transaction)
        db.session.commit()
        
        # Flash é uma forma de mandar mensagens temporárias para a próxima página
        # O Jinja2 vai exibir essa mensagem depois
        # Requer app.secret_key configurado, mas vamos adicionar lá depois
        # flash('Transação adicionada com sucesso!', 'success')
        return redirect(url_for('dashboard.index'))
        
    # Se for GET, apenas renderiza o formulário e envia as categorias disponíveis
    categories = Category.query.all()
    return render_template('add_transaction.html', categories=categories)

@transactions_bp.route('/transactions/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_transaction(id):
    """Rota para editar uma transação existente."""
    transaction = Transaction.query.get_or_404(id)
    
    if request.method == 'POST':
        transaction.description = request.form.get('description')
        transaction.amount = float(request.form.get('amount').replace(',', '.'))
        transaction.type = request.form.get('type')
        transaction.category_id = int(request.form.get('category_id'))
        
        date_str = request.form.get('date')
        transaction.date = datetime.strptime(date_str, '%Y-%m-%d').date()
        transaction.notes = request.form.get('notes')
        
        db.session.commit()
        return redirect(url_for('transactions.list_transactions'))
        
    categories = Category.query.all()
    return render_template('edit_transaction.html', transaction=transaction, categories=categories)

@transactions_bp.route('/transactions/delete/<int:id>', methods=['POST'])
@login_required
def delete_transaction(id):
    """Rota para deletar uma transação."""
    transaction = Transaction.query.get_or_404(id)
    db.session.delete(transaction)
    db.session.commit()
    return redirect(url_for('transactions.list_transactions'))
