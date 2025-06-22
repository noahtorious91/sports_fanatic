document.addEventListener('DOMContentLoaded', function() {
    console.log('Page loaded, setting up transaction select listener');
    
    const transactionSelect = document.getElementById('id_transaction');
    const lineItemsGroup = document.getElementById('line-items-group');
    const lineItemsContainer = document.getElementById('line-items-container');
    const submitBtn = document.getElementById('submit-btn');
    
    console.log('Transaction select element:', transactionSelect);
    
    if (transactionSelect) {
        transactionSelect.addEventListener('change', function() {
            const transactionId = this.value;
            console.log('Transaction selected:', transactionId);
            
            if (transactionId) {
                console.log('Fetching line items for transaction:', transactionId);
                // Fetch line items for the selected transaction
                fetch(`/api/transaction-line-items/${transactionId}/`)
                    .then(response => {
                        console.log('Response received:', response);
                        if (!response.ok) {
                            throw new Error(`HTTP error! status: ${response.status}`);
                        }
                        return response.json();
                    })
                    .then(data => {
                        console.log('Data received:', data);
                        lineItemsContainer.innerHTML = '';
                        
                        if (data.line_items && data.line_items.length > 0) {
                            console.log('Found', data.line_items.length, 'line items');
                            data.line_items.forEach(item => {
                                const div = document.createElement('div');
                                div.className = 'line-item-checkbox';
                                div.innerHTML = `
                                    <label>
                                        <input type="checkbox" name="line_items" value="${item.id}">
                                        LineItem #${item.id} - ${item.product_name} (Qty: ${item.quantity}) - $${item.price}
                                    </label>
                                `;
                                lineItemsContainer.appendChild(div);
                            });
                            
                            lineItemsGroup.style.display = 'block';
                            submitBtn.disabled = false;
                        } else {
                            console.log('No line items found');
                            lineItemsContainer.innerHTML = '<p>No line items found for this transaction.</p>';
                            lineItemsGroup.style.display = 'block';
                            submitBtn.disabled = true;
                        }
                    })
                    .catch(error => {
                        console.error('Error fetching line items:', error);
                        lineItemsContainer.innerHTML = '<p>Error loading line items.</p>';
                        lineItemsGroup.style.display = 'block';
                        submitBtn.disabled = true;
                    });
            } else {
                console.log('No transaction selected');
                lineItemsGroup.style.display = 'none';
                submitBtn.disabled = true;
            }
        });
    } else {
        console.error('Transaction select element not found');
    }
});