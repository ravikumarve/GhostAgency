// BRUTALIST JS - Ghost Agency Dashboard
// Minimal JavaScript for brutalist functionality

// Status indicator updates
function updateAgentStatus() {
    fetch('/api/agent-status')
        .then(response => response.json())
        .then(data => {
            document.querySelector('[data-agent-count]').textContent = data.total;
            document.querySelector('[data-online-count]').textContent = data.online;
            document.querySelector('[data-offline-count]').textContent = data.offline;
        })
        .catch(error => console.error('Status update failed:', error));
}

// Auto-refresh status every 30 seconds
setInterval(updateAgentStatus, 30000);

// Button hover effects (enhance brutalist feel)
document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(btn => {
        btn.addEventListener('mouseenter', () => {
            btn.style.transform = 'translate(-2px, -2px)';
        });
        btn.addEventListener('mouseleave', () => {
            btn.style.transform = 'translate(0, 0)';
        });
    });
});

// Simple form validation
function validateForm(form) {
    const inputs = form.querySelectorAll('.form-input');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.style.borderColor = '#FF0000';
            isValid = false;
        } else {
            input.style.borderColor = '#000000';
        }
    });
    
    return isValid;
}

// Toggle dark mode (brutalist alternative)
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
}

// Check for saved dark mode preference
if (localStorage.getItem('darkMode') === 'true') {
    document.body.classList.add('dark-mode');
}