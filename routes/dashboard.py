from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required
from models import Transaction, Category
from database import db
from sqlalchemy import func
import datetime
import calendar
import pandas as pd
from flask import Response

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def index():
    """Rota principal que renderiza a página do dashboard."""
    # Buscar resumo do mês atual para exibir nos cartões
    today = datetime.date.today()
    # Parâmetro para ver Mês ou Ano
    period = request.args.get('period', 'month')
    
    if period == 'year':
        start_date = today.replace(month=1, day=1)
        end_date = today.replace(month=12, day=31)
    else:
        start_date = today.replace(day=1)
        last_day = calendar.monthrange(today.year, today.month)[1]
        end_date = today.replace(day=last_day)
    
    # Calcula totais
    total_income = db.session.query(func.sum(Transaction.amount)).filter(
        Transaction.type == 'income',
        Transaction.date >= start_date,
        Transaction.date <= end_date
    ).scalar() or 0.0
    
    total_expense = db.session.query(func.sum(Transaction.amount)).filter(
        Transaction.type == 'expense',
        Transaction.date >= start_date,
        Transaction.date <= end_date
    ).scalar() or 0.0
    
    balance = total_income - total_expense
    
    # Pegar as últimas 5 transações
    recent_transactions = Transaction.query.order_by(Transaction.created_at.desc()).limit(5).all()
    
    return render_template(
        'index.html', 
        total_income=total_income, 
        total_expense=total_expense,
        balance=balance,
        recent_transactions=recent_transactions,
        period=period
    )

@dashboard_bp.route('/api/chart-data')
@login_required
def chart_data():
    """Rota da API que retorna dados para o Chart.js em formato JSON."""
    today = datetime.date.today()
    period = request.args.get('period', 'month')
    
    if period == 'year':
        start_date = today.replace(month=1, day=1)
        end_date = today.replace(month=12, day=31)
    else:
        start_date = today.replace(day=1)
        last_day = calendar.monthrange(today.year, today.month)[1]
        end_date = today.replace(day=last_day)
    
    # Dados para o gráfico de pizza (Despesas por categoria no período)
    expenses_by_category = db.session.query(
        Category.name, 
        Category.color, 
        func.sum(Transaction.amount).label('total')
    ).join(Transaction, Category.id == Transaction.category_id).filter(
        Transaction.type == 'expense',
        Transaction.date >= start_date,
        Transaction.date <= end_date
    ).group_by(Category.id).all()
    
    pie_labels = [row.name for row in expenses_by_category]
    pie_data = [row.total for row in expenses_by_category]
    pie_colors = [row.color for row in expenses_by_category]
    
    return jsonify({
        "pie_chart": {
            "labels": pie_labels,
            "data": pie_data,
            "colors": pie_colors
        }
    })

@dashboard_bp.route('/api/export/csv')
@login_required
def export_csv():
    """Utiliza Pandas para ler do banco e exportar para CSV, ideal para o Power BI."""
    # Consultando diretamente via read_sql do Pandas com SQLAlchemy engine connection
    query = db.session.query(
        Transaction.id,
        Transaction.description,
        Transaction.amount,
        Transaction.type,
        Transaction.date,
        Transaction.created_at,
        Category.name.label('category')
    ).join(Category, Transaction.category_id == Category.id).statement
    
    df = pd.read_sql(query, db.engine)
    
    # Formatando a data
    if not df.empty:
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M:%S')
        df['amount'] = df['amount'].round(2)
        
    csv_data = df.to_csv(index=False, sep=';', decimal=',')
    
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=financeflow_export.csv"}
    )
