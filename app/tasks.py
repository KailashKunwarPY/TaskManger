from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from app.models import Task
from app.forms import TaskForm

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/tasks')
@login_required
def task_list():
    priority = request.args.get('priority')
    status = request.args.get('status')
    due_date = request.args.get('due_date')
    
    query = Task.query.filter_by(user_id=current_user.id)
    
    if priority and priority != 'All':
        query = query.filter_by(priority=priority)
    
    if status == 'completed':
        query = query.filter_by(completed=True)
    elif status == 'pending':
        query = query.filter_by(completed=False)
    
    if due_date:
        try:
            due_date = datetime.strptime(due_date, '%Y-%m-%d').date()
            query = query.filter(db.func.date(Task.due_date) == due_date)
        except ValueError:
            pass
    
    tasks = query.order_by(Task.due_date.asc()).all()
    return render_template('tasks/list.html', tasks=tasks)

@tasks_bp.route('/tasks/create', methods=['GET', 'POST'])
@login_required
def create_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data,
            priority=form.priority.data,
            due_date=form.due_date.data,
            user_id=current_user.id
        )
        db.session.add(task)
        db.session.commit()
        flash('Task created successfully!')
        return redirect(url_for('tasks.task_list'))
    return render_template('tasks/create.html', form=form)

@tasks_bp.route('/tasks/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(id):
    task = Task.query.get_or_404(id)
    if task.user_id != current_user.id:
        flash('You can only edit your own tasks!')
        return redirect(url_for('tasks.task_list'))
    
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.priority = form.priority.data
        task.due_date = form.due_date.data
        db.session.commit()
        flash('Task updated successfully!')
        return redirect(url_for('tasks.task_list'))
    return render_template('tasks/edit.html', form=form, task=task)

@tasks_bp.route('/tasks/<int:id>/delete', methods=['POST'])
@login_required
def delete_task(id):
    task = Task.query.get_or_404(id)
    if task.user_id != current_user.id:
        flash('You can only delete your own tasks!')
        return redirect(url_for('tasks.task_list'))
    
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!')
    return redirect(url_for('tasks.task_list'))

@tasks_bp.route('/tasks/<int:id>/toggle', methods=['POST'])
@login_required
def toggle_task(id):
    task = Task.query.get_or_404(id)
    if task.user_id != current_user.id:
        return jsonify({'success': False})
    
    task.completed = not task.completed
    db.session.commit()
    return jsonify({'success': True, 'completed': task.completed})

@tasks_bp.route('/tasks/export')
@login_required
def export_tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    tasks_data = [{
        'title': task.title,
        'description': task.description,
        'priority': task.priority,
        'due_date': task.due_date.isoformat() if task.due_date else None,
        'completed': task.completed,
        'created_at': task.created_at.isoformat()
    } for task in tasks]
    
    return jsonify(tasks_data)

@tasks_bp.route('/tasks/import', methods=['POST'])
@login_required
def import_tasks():
    if not request.is_json:
        return jsonify({'success': False, 'error': 'Invalid data format'}), 400
    
    tasks_data = request.get_json()
    if not isinstance(tasks_data, list):
        return jsonify({'success': False, 'error': 'Data should be an array'}), 400
    
    try:
        for task_data in tasks_data:
            task = Task(
                title=task_data.get('title'),
                description=task_data.get('description'),
                priority=task_data.get('priority', 'Medium'),
                due_date=datetime.fromisoformat(task_data['due_date']) if task_data.get('due_date') else None,
                completed=task_data.get('completed', False),
                user_id=current_user.id
            )
            db.session.add(task)
        db.session.commit()
        return jsonify({'success': True, 'count': len(tasks_data)})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400