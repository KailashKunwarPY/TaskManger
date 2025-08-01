from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Task, User

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    total_tasks = Task.query.filter_by(user_id=current_user.id).count()
    completed_tasks = Task.query.filter_by(user_id=current_user.id, completed=True).count()
    pending_tasks = total_tasks - completed_tasks
    
    high_priority = Task.query.filter_by(user_id=current_user.id, priority='High').count()
    medium_priority = Task.query.filter_by(user_id=current_user.id, priority='Medium').count()
    low_priority = Task.query.filter_by(user_id=current_user.id, priority='Low').count()
    
    return render_template('dashboard.html', 
                         total_tasks=total_tasks,
                         completed_tasks=completed_tasks,
                         pending_tasks=pending_tasks,
                         high_priority=high_priority,
                         medium_priority=medium_priority,
                         low_priority=low_priority)

@main_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html')