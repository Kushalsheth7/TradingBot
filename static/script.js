// Form handling
const orderForm = document.getElementById('orderForm');
const typeSelect = document.getElementById('type');
const priceGroup = document.getElementById('priceGroup');
const stopPriceGroup = document.getElementById('stopPriceGroup');
const stopLimitPriceGroup = document.getElementById('stopLimitPriceGroup');
const submitBtn = document.getElementById('submitBtn');
const btnText = document.querySelector('.btn-text');
const btnLoader = document.querySelector('.btn-loader');
const resultDiv = document.getElementById('result');
const logsDiv = document.getElementById('logs');
const refreshBtn = document.getElementById('refreshLogs');
const statusBadge = document.getElementById('statusBadge');

// Show/hide price fields based on order type
typeSelect.addEventListener('change', function() {
    const orderType = this.value;
    
    priceGroup.style.display = 'none';
    stopPriceGroup.style.display = 'none';
    stopLimitPriceGroup.style.display = 'none';
    
    if (orderType === 'LIMIT') {
        priceGroup.style.display = 'block';
        document.getElementById('price').required = true;
    } else if (orderType === 'STOP_LIMIT') {
        priceGroup.style.display = 'block';
        stopPriceGroup.style.display = 'block';
        document.getElementById('price').required = true;
        document.getElementById('stop_price').required = true;
    } else if (orderType === 'OCO') {
        priceGroup.style.display = 'block';
        stopPriceGroup.style.display = 'block';
        stopLimitPriceGroup.style.display = 'block';
        document.getElementById('price').required = true;
        document.getElementById('stop_price').required = true;
        document.getElementById('stop_limit_price').required = true;
    } else {
        document.getElementById('price').required = false;
        document.getElementById('stop_price').required = false;
        document.getElementById('stop_limit_price').required = false;
    }
});

// Form submission
orderForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    // Update UI
    submitBtn.disabled = true;
    btnText.style.display = 'none';
    btnLoader.style.display = 'inline-block';
    resultDiv.style.display = 'none';
    statusBadge.textContent = 'Processing...';
    statusBadge.style.background = 'hsla(45, 100%, 51%, 0.2)';
    statusBadge.style.color = 'hsl(45, 100%, 51%)';
    statusBadge.style.borderColor = 'hsl(45, 100%, 51%)';
    
    // Collect form data
    const formData = {
        symbol: document.getElementById('symbol').value,
        side: document.getElementById('side').value,
        type: document.getElementById('type').value,
        quantity: document.getElementById('quantity').value,
        price: document.getElementById('price').value || null,
        stop_price: document.getElementById('stop_price').value || null,
        stop_limit_price: document.getElementById('stop_limit_price').value || null
    };
    
    try {
        const response = await fetch('/api/place-order', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            showResult('success', '✓ Order placed successfully!');
            statusBadge.textContent = 'Success';
            statusBadge.style.background = 'hsla(142, 76%, 36%, 0.2)';
            statusBadge.style.color = 'hsl(142, 76%, 36%)';
            statusBadge.style.borderColor = 'hsl(142, 76%, 36%)';
            
            // Refresh logs after a short delay
            setTimeout(loadLogs, 1000);
        } else {
            showResult('error', '✗ ' + (data.error || 'Order failed'));
            statusBadge.textContent = 'Failed';
            statusBadge.style.background = 'hsla(0, 84%, 60%, 0.2)';
            statusBadge.style.color = 'hsl(0, 84%, 60%)';
            statusBadge.style.borderColor = 'hsl(0, 84%, 60%)';
        }
    } catch (error) {
        showResult('error', '✗ Connection error: ' + error.message);
        statusBadge.textContent = 'Error';
        statusBadge.style.background = 'hsla(0, 84%, 60%, 0.2)';
        statusBadge.style.color = 'hsl(0, 84%, 60%)';
        statusBadge.style.borderColor = 'hsl(0, 84%, 60%)';
    } finally {
        // Reset UI
        submitBtn.disabled = false;
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
        
        // Reset status badge after 3 seconds
        setTimeout(() => {
            statusBadge.textContent = 'Ready';
            statusBadge.style.background = 'hsla(142, 76%, 36%, 0.2)';
            statusBadge.style.color = 'hsl(142, 76%, 36%)';
            statusBadge.style.borderColor = 'hsl(142, 76%, 36%)';
        }, 3000);
    }
});

// Show result message
function showResult(type, message) {
    resultDiv.className = 'result-message ' + type;
    resultDiv.textContent = message;
    resultDiv.style.display = 'block';
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        resultDiv.style.display = 'none';
    }, 5000);
}

// Load logs
async function loadLogs() {
    try {
        const response = await fetch('/api/logs');
        const data = await response.json();
        
        if (data.success && data.logs.length > 0) {
            logsDiv.innerHTML = data.logs.map(log => {
                let logClass = 'log-line';
                if (log.includes('ERROR')) logClass += ' error';
                else if (log.includes('WARNING')) logClass += ' warning';
                else if (log.includes('INFO')) logClass += ' info';
                
                return `<div class="${logClass}">${escapeHtml(log)}</div>`;
            }).join('');
        } else {
            logsDiv.innerHTML = '<div class="log-empty">No logs yet. Place an order to get started.</div>';
        }
    } catch (error) {
        console.error('Failed to load logs:', error);
    }
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// Refresh logs button
refreshBtn.addEventListener('click', loadLogs);

// Load logs on page load
loadLogs();

// Auto-refresh logs every 10 seconds
setInterval(loadLogs, 10000);
