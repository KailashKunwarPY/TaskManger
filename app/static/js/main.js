document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    
    if (hamburger && navLinks) {
        hamburger.addEventListener('click', function() {
            navLinks.classList.toggle('active');
        });
    }

    // Dark mode toggle
    const darkModeToggle = document.getElementById('dark-mode-toggle');
    const darkModeStylesheet = document.getElementById('dark-mode-stylesheet');
    const darkModeKey = 'darkModeEnabled';
    
    // Check for saved user preference
    const savedMode = localStorage.getItem(darkModeKey);
    if (savedMode === 'true') {
        darkModeStylesheet.disabled = false;
        updateDarkModeIcon(true);
    }
    
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', function() {
            const isDarkMode = darkModeStylesheet.disabled;
            darkModeStylesheet.disabled = !isDarkMode;
            localStorage.setItem(darkModeKey, !isDarkMode);
            updateDarkModeIcon(!isDarkMode);
        });
    }
    
    function updateDarkModeIcon(isDarkMode) {
        const icon = darkModeToggle.querySelector('i');
        if (isDarkMode) {
            icon.classList.remove('fa-moon');
            icon.classList.add('fa-sun');
        } else {
            icon.classList.remove('fa-sun');
            icon.classList.add('fa-moon');
        }
    }

    // Flash messages auto-close
    const flashMessages = document.querySelectorAll('.flash');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 500);
        }, 5000);
    });

    // Initialize Chart.js on dashboard
    if (document.getElementById('tasksChart')) {
        initTasksChart();
    }
});

function initTasksChart() {
    const ctx = document.getElementById('tasksChart').getContext('2d');
    const highPriority = parseInt(document.getElementById('high-priority').textContent);
    const mediumPriority = parseInt(document.getElementById('medium-priority').textContent);
    const lowPriority = parseInt(document.getElementById('low-priority').textContent);
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['High Priority', 'Medium Priority', 'Low Priority'],
            datasets: [{
                data: [highPriority, mediumPriority, lowPriority],
                backgroundColor: [
                    '#ff5252',
                    '#ffc107',
                    '#4caf50'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}