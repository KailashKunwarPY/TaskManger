document.addEventListener('DOMContentLoaded', function() {
    // Task completion toggle
    document.querySelectorAll('.task-btn.complete').forEach(button => {
        button.addEventListener('click', async function(e) {
            e.preventDefault();
            const taskId = this.dataset.taskId;
            const taskCard = this.closest('.task-card');
            
            try {
                const response = await fetch(`/tasks/${taskId}/toggle`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });
                
                const data = await response.json();
                if (data.success) {
                    taskCard.classList.toggle('completed');
                    this.textContent = data.completed ? 'Undo' : 'Complete';
                    
                    // Show a temporary notification
                    showNotification(
                        data.completed ? 'Task marked as complete!' : 'Task marked as incomplete!',
                        data.completed ? 'success' : 'info'
                    );
                }
            } catch (error) {
                console.error('Error:', error);
                showNotification('Failed to update task status', 'error');
            }
        });
    });
    
    // Task deletion confirmation
    document.querySelectorAll('.task-btn.delete').forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this task?')) {
                e.preventDefault();
            }
        });
    });
    
    // Export tasks
    const exportBtn = document.getElementById('export-tasks');
    if (exportBtn) {
        exportBtn.addEventListener('click', async function() {
            try {
                const response = await fetch('/tasks/export');
                const data = await response.json();
                
                // Create a download link
                const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `tasks-${new Date().toISOString().split('T')[0]}.json`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
                
                showNotification('Tasks exported successfully!', 'success');
            } catch (error) {
                console.error('Error:', error);
                showNotification('Failed to export tasks', 'error');
            }
        });
    }
    
    // Import tasks
    const importBtn = document.getElementById('import-tasks');
    const fileInput = document.getElementById('task-import-file');
    if (importBtn && fileInput) {
        importBtn.addEventListener('click', function() {
            fileInput.click();
        });
        
        fileInput.addEventListener('change', async function() {
            if (this.files.length === 0) return;
            
            const file = this.files[0];
            if (file.type !== 'application/json') {
                showNotification('Please select a JSON file', 'error');
                return;
            }
            
            try {
                const fileContent = await file.text();
                const tasksData = JSON.parse(fileContent);
                
                if (!Array.isArray(tasksData)) {
                    showNotification('Invalid file format', 'error');
                    return;
                }
                
                const response = await fetch('/tasks/import', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: fileContent
                });
                
                const data = await response.json();
                if (data.success) {
                    showNotification(`Successfully imported ${data.count} tasks!`, 'success');
                    setTimeout(() => window.location.reload(), 1500);
                } else {
                    showNotification(data.error || 'Failed to import tasks', 'error');
                }
            } catch (error) {
                console.error('Error:', error);
                showNotification('Failed to import tasks', 'error');
            }
            
            // Reset file input
            this.value = '';
        });
    }
    
    // Filter form submission
    const filterForm = document.getElementById('task-filters');
    if (filterForm) {
        filterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            const params = new URLSearchParams();
            
            for (const [key, value] of formData.entries()) {
                if (value) params.append(key, value);
            }
            
            window.location.search = params.toString();
        });
        
        // Reset filters
        const resetBtn = document.getElementById('reset-filters');
        if (resetBtn) {
            resetBtn.addEventListener('click', function() {
                window.location.search = '';
            });
        }
    }
    
    // Helper function to show notifications
    function showNotification(message, type) {
        const notification = document.createElement('div');
        notification.className = `flash flash-${type}`;
        notification.textContent = message;
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.opacity = '0';
            setTimeout(() => notification.remove(), 500);
        }, 3000);
    }
    
    // Check for due tasks and show reminders
    checkDueTasks();
});

async function checkDueTasks() {
    try {
        const response = await fetch('/tasks/export');
        const tasks = await response.json();
        
        const today = new Date().toISOString().split('T')[0];
        const dueTasks = tasks.filter(task => 
            task.due_date && 
            task.due_date.startsWith(today) && 
            !task.completed
        );
        
        if (dueTasks.length > 0) {
            const taskTitles = dueTasks.map(task => task.title).join(', ');
            console.log(`Reminder: You have ${dueTasks.length} tasks due today: ${taskTitles}`);
            
            // You could replace this with a more visible notification system
            if (Notification.permission === 'granted') {
                new Notification(`You have ${dueTasks.length} tasks due today`, {
                    body: taskTitles
                });
            } else if (Notification.permission !== 'denied') {
                Notification.requestPermission().then(permission => {
                    if (permission === 'granted') {
                        new Notification(`You have ${dueTasks.length} tasks due today`, {
                            body: taskTitles
                        });
                    }
                });
            }
        }
    } catch (error) {
        console.error('Error checking due tasks:', error);
    }
}