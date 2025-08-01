from datetime import datetime
from app import db
from app.models import Task, User, Profile
import json

def seed_database():
    """Seed the database with initial data"""
    try:
        # Create test user if not exists
        if not User.query.filter_by(username='testuser').first():
            user = User(username='testuser', email='test@example.com')
            user.set_password('testpassword')
            db.session.add(user)
            db.session.commit()

            # Create profile
            profile = Profile(
                full_name='Test User',
                bio='This is a test user profile',
                user_id=user.id
            )
            db.session.add(profile)

            # Create sample tasks
            tasks = [
                {
                    'title': 'Complete project',
                    'description': 'Finish the task management application',
                    'priority': 'High',
                    'due_date': datetime(2023, 12, 31),
                    'completed': False,
                    'user_id': user.id
                },
                {
                    'title': 'Buy groceries',
                    'description': 'Milk, eggs, bread, fruits',
                    'priority': 'Medium',
                    'due_date': datetime(2023, 11, 15),
                    'completed': True,
                    'user_id': user.id
                },
                {
                    'title': 'Exercise',
                    'description': '30 minutes of cardio',
                    'priority': 'Low',
                    'due_date': None,
                    'completed': False,
                    'user_id': user.id
                }
            ]

            for task_data in tasks:
                task = Task(**task_data)
                db.session.add(task)
            
            db.session.commit()
            print("Database seeded successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"Error seeding database: {str(e)}")

def backup_database_to_json():
    """Create a JSON backup of the database"""
    try:
        users = User.query.all()
        tasks = Task.query.all()
        profiles = Profile.query.all()
        
        backup_data = {
            'users': [{
                'username': user.username,
                'email': user.email,
                'password_hash': user.password_hash,
                'created_at': user.created_at.isoformat() if user.created_at else None
            } for user in users],
            'profiles': [{
                'full_name': profile.full_name,
                'bio': profile.bio,
                'user_id': profile.user_id
            } for profile in profiles],
            'tasks': [{
                'title': task.title,
                'description': task.description,
                'priority': task.priority,
                'due_date': task.due_date.isoformat() if task.due_date else None,
                'completed': task.completed,
                'created_at': task.created_at.isoformat() if task.created_at else None,
                'user_id': task.user_id
            } for task in tasks]
        }
        
        return backup_data
    except Exception as e:
        print(f"Error creating backup: {str(e)}")
        return None

def restore_database_from_json(json_data):
    """Restore database from JSON backup"""
    try:
        # Clear existing data
        db.session.query(Task).delete()
        db.session.query(Profile).delete()
        db.session.query(User).delete()
        db.session.commit()

        # Restore users
        for user_data in json_data.get('users', []):
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                password_hash=user_data['password_hash'],
                created_at=datetime.fromisoformat(user_data['created_at']) if user_data.get('created_at') else None
            )
            db.session.add(user)
        
        db.session.commit()

        # Restore profiles
        for profile_data in json_data.get('profiles', []):
            profile = Profile(
                full_name=profile_data['full_name'],
                bio=profile_data['bio'],
                user_id=profile_data['user_id']
            )
            db.session.add(profile)
        
        # Restore tasks
        for task_data in json_data.get('tasks', []):
            task = Task(
                title=task_data['title'],
                description=task_data['description'],
                priority=task_data['priority'],
                due_date=datetime.fromisoformat(task_data['due_date']) if task_data.get('due_date') else None,
                completed=task_data['completed'],
                created_at=datetime.fromisoformat(task_data['created_at']) if task_data.get('created_at') else None,
                user_id=task_data['user_id']
            )
            db.session.add(task)
        
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error restoring database: {str(e)}")
        return False