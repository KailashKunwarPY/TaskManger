import click
from app import db
from app.models import User, Task, Profile
from app.utils import seed_database, backup_database_to_json

def register_cli_commands(app):
    @app.cli.command('seed-db')
    def seed_db():
        """Seed the database with sample data"""
        seed_database()
        click.echo('Database seeded successfully!')

    @app.cli.command('backup-db')
    def backup_db():
        """Create a backup of the database"""
        backup_data = backup_database_to_json()
        if backup_data:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_dir = os.path.join(app.instance_path, 'backups')
            os.makedirs(backup_dir, exist_ok=True)
            backup_file = os.path.join(backup_dir, f'db_backup_{timestamp}.json')
            
            with open(backup_file, 'w') as f:
                json.dump(backup_data, f, indent=2)
            
            click.echo(f'Database backup created at: {backup_file}')
        else:
            click.echo('Failed to create database backup')

    @app.cli.command('reset-db')
    def reset_db():
        """Reset the database"""
        if click.confirm('Are you sure you want to reset the database? This will delete all data.'):
            db.drop_all()
            db.create_all()
            click.echo('Database reset successfully!')