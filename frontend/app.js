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

    calculateBtn.textContent = 'Calculating...';
    calculateBtn.disabled = true;

    try {
        const response = await fetch('/api/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ expression, mode }),
        });

        // Log the full response for debugging
        console.log('Response status:', response.status);

        if (!response.ok) {
            const errorText = await response.text();
            console.error('Error response:', errorText);
            throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
        }

        const data = await response.json();

        stepsDiv.innerHTML = '';
        data.steps.forEach((step, index) => {
            const stepDiv = document.createElement('div');
            stepDiv.textContent = `${index + 1}. ${step}`;
            stepsDiv.appendChild(stepDiv);
        });
        finalResultP.textContent = `Final Result: ${data.final_result}`;

        resultsDiv.classList.remove('hidden');
    } catch (error) {
        console.error('Detailed Calculation Error:', error);
        alert(`Calculation failed: ${error.message}`);
    } finally {
        calculateBtn.textContent = 'Calculate';
        calculateBtn.disabled = false;
    }
});
