from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from app import supabase

auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        try:
            res = supabase.auth.sign_up({
                "email": email,
                "password": password,
            })
            flash('Registration successful! Please check your email to confirm.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash(str(e), 'danger')
            
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        try:
            res = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password,
            })
            session['user'] = res.user.id
            session['access_token'] = res.session.access_token
            flash('Login successful!', 'success')
            return redirect(url_for('main.index'))
        except Exception as e:
            flash(str(e), 'danger')
            
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    try:
        supabase.auth.sign_out()
    except:
        pass
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
