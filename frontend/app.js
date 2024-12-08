// DOM Elements
const expressionInput = document.getElementById('expression');
const postfixBtn = document.getElementById('postfix-btn');
const prefixBtn = document.getElementById('prefix-btn');
const calculateBtn = document.getElementById('calculate-btn');
const resultsDiv = document.getElementById('results');
const stepsDiv = document.getElementById('steps');
const finalResultP = document.getElementById('final-result');

// State
let mode = 'postfix'; // Default mode

// Toggle mode between postfix and prefix
postfixBtn.addEventListener('click', () => {
    mode = 'postfix';
    postfixBtn.classList.add('active');
    prefixBtn.classList.remove('active');
});

prefixBtn.addEventListener('click', () => {
    mode = 'prefix';
    prefixBtn.classList.add('active');
    postfixBtn.classList.remove('active');
});

// Handle Calculate Button Click
calculateBtn.addEventListener('click', async () => {
    const expression = expressionInput.value.trim();

    if (!expression) {
        alert('Please enter a mathematical expression');
        return;
    }

    // Display loading state
    calculateBtn.textContent = 'Calculating...';
    calculateBtn.disabled = true;

    try {
        // API Request
        const response = await fetch('/api/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ expression, mode }),
        });

        const data = await response.json();

        // Display Results
        stepsDiv.innerHTML = '';
        data.steps.forEach((step, index) => {
            const stepDiv = document.createElement('div');
            stepDiv.textContent = `${index + 1}. ${step}`;
            stepsDiv.appendChild(stepDiv);
        });
        finalResultP.textContent = `Final Result: ${data.final_result}`;

        resultsDiv.classList.remove('hidden');
    } catch (error) {
        console.error('Calculation error:', error);
        alert('Failed to calculate. Please try again.');
    } finally {
        // Reset button state
        calculateBtn.textContent = 'Calculate';
        calculateBtn.disabled = false;
    }
});
