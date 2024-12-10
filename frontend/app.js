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

// Enhanced Input Validation Function
function validateExpression(expression) {
    // Remove all whitespace
    const cleanedExpression = expression.replace(/\s+/g, '');

    // Regular expression for valid characters (supporting float numbers)
    const validCharRegex = /^[0-9+\-*/()\.^\s]+$/;

    // Check 1: Only allow valid characters
    if (!validCharRegex.test(cleanedExpression)) {
        throw new Error('Invalid characters in expression. Only numbers and +, -, *, /, ^, (), . are allowed.');
    }

    // Check 2: Balanced parentheses
    let parenthesesCount = 0;
    for (let char of cleanedExpression) {
        if (char === '(') parenthesesCount++;
        if (char === ')') parenthesesCount--;

        // Prevent negative count (more closing than opening)
        if (parenthesesCount < 0) {
            throw new Error('Unbalanced parentheses: Too many closing parentheses');
        }
    }

    // Check 3: Parentheses are balanced at the end
    if (parenthesesCount !== 0) {
        throw new Error('Unbalanced parentheses: Not all parentheses are closed');
    }

    // Check 4: Prevent consecutive operators
    const consecutiveOperatorsRegex = /[+\-*/^]{2,}/;
    if (consecutiveOperatorsRegex.test(cleanedExpression)) {
        throw new Error('Invalid expression: Consecutive operators are not allowed');
    }

    // Check 5: Prevent invalid start/end of expression
    const startEndInvalidRegex = /^[+*/^)]|[+\-*/^.(]$/;
    if (startEndInvalidRegex.test(cleanedExpression)) {
        throw new Error('Expression cannot start with an operator (except -) or end with an operator');
    }

    // Check 6: Validate float numbers
    const floatNumberRegex = /(\d+\.\d+|\d+)/g;
    const numbers = cleanedExpression.match(floatNumberRegex) || [];
    const operators = cleanedExpression.match(/[+\-*/^]/g) || [];

    // Check for multiple decimal points in a number
    const multipleDecimalPointsRegex = /\d+\.\d+\.\d+/;
    if (multipleDecimalPointsRegex.test(cleanedExpression)) {
        throw new Error('Invalid number format: Too many decimal points in a number');
    }

    // Check for invalid decimal placements
    const invalidDecimalRegex = /\.\d*\.|[+\-*/^]\.|\.[+\-*/^]/;
    if (invalidDecimalRegex.test(cleanedExpression)) {
        throw new Error('Invalid decimal point placement');
    }

    // Ensure minimum numbers and operators
    if (numbers.length < 2) {
        throw new Error('Expression must contain at least 2 numbers');
    }

    if (operators.length < 1) {
        throw new Error('Expression must contain at least 1 operator');
    }

    // If all checks pass, return the cleaned expression
    return cleanedExpression;
}

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
