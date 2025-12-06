from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from app import supabase
from datetime import datetime

main_bp = Blueprint('main', __name__, template_folder='templates')

def get_user_id():
    return session.get('user')

@main_bp.route('/')
def index():
    user_id = get_user_id()
    if not user_id:
        return redirect(url_for('auth.login'))
    
    # Filters
    category = request.args.get('category')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    search = request.args.get('search')
    
    query = supabase.table('expenses').select('*').eq('user_id', user_id).order('date', desc=True)
    
    if category:
        query = query.eq('category', category)
    if start_date:
        query = query.gte('date', start_date)
    if end_date:
        query = query.lte('date', end_date)
    if search:
        # Supabase ilike for search
        query = query.ilike('description', f'%{search}%')
        
    try:
        response = query.execute()
        expenses = response.data
    except Exception as e:
        flash(f"Error fetching expenses: {e}", 'danger')
        expenses = []
        
    return render_template('index.html', expenses=expenses)

@main_bp.route('/add', methods=['GET', 'POST'])
def add_expense():
    user_id = get_user_id()
    if not user_id:
        return redirect(url_for('auth.login'))
        
    if request.method == 'POST':
        amount = request.form.get('amount')
        category = request.form.get('category')
        description = request.form.get('description')
        date = request.form.get('date')
        
        try:
            supabase.table('expenses').insert({
                'user_id': user_id,
                'amount': float(amount),
                'category': category,
                'description': description,
                'date': date
            }).execute()
            flash('Expense added successfully!', 'success')
            return redirect(url_for('main.index'))
        except Exception as e:
            flash(f"Error adding expense: {e}", 'danger')
            
    return render_template('expense_form.html', title="Add Expense")

@main_bp.route('/edit/<uuid:id>', methods=['GET', 'POST'])
def edit_expense(id):
    user_id = get_user_id()
    if not user_id:
        return redirect(url_for('auth.login'))
        
    if request.method == 'POST':
        amount = request.form.get('amount')
        category = request.form.get('category')
        description = request.form.get('description')
        date = request.form.get('date')
        
        try:
            supabase.table('expenses').update({
                'amount': float(amount),
                'category': category,
                'description': description,
                'date': date
            }).eq('id', str(id)).eq('user_id', user_id).execute()
            flash('Expense updated successfully!', 'success')
            return redirect(url_for('main.index'))
        except Exception as e:
            flash(f"Error updating expense: {e}", 'danger')
            
    # Get existing expense
    try:
        response = supabase.table('expenses').select('*').eq('id', str(id)).eq('user_id', user_id).single().execute()
        expense = response.data
    except Exception as e:
        flash(f"Error fetching expense: {e}", 'danger')
        return redirect(url_for('main.index'))
        
    return render_template('expense_form.html', title="Edit Expense", expense=expense)

@main_bp.route('/delete/<uuid:id>', methods=['POST'])
def delete_expense(id):
    user_id = get_user_id()
    if not user_id:
        return redirect(url_for('auth.login'))
        
    try:
        supabase.table('expenses').delete().eq('id', str(id)).eq('user_id', user_id).execute()
        flash('Expense deleted successfully!', 'success')
    except Exception as e:
        flash(f"Error deleting expense: {e}", 'danger')
        
    return redirect(url_for('main.index'))

@main_bp.route('/summary')
def summary():
    user_id = get_user_id()
    if not user_id:
        return redirect(url_for('auth.login'))
        
    # Simple summary: Total by category
    # Note: Supabase JS client has better aggregation, python client might need raw sql or processing in python
    # For simplicity, let's fetch all and process in python for now (not efficient for large data but okay for MVP)
    
    try:
        response = supabase.table('expenses').select('*').eq('user_id', user_id).execute()
        expenses = response.data
        
        category_totals = {}
        for expense in expenses:
            cat = expense['category']
            amount = expense['amount']
            category_totals[cat] = category_totals.get(cat, 0) + amount
            
        return render_template('summary.html', category_totals=category_totals)
        
    except Exception as e:
        flash(f"Error fetching summary: {e}", 'danger')
        return redirect(url_for('main.index'))
