from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend import prefix_expression, postfix_expression
import traceback

# FastAPI app instance
app = FastAPI()

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CalculationRequest(BaseModel):
    expression: str
    mode: str


class CalculationResponse(BaseModel):
    conversion_steps: list[str]
    calculate_steps: list[str]
    final_result: float


# def infix_to_prefix(expression):
#     """Convert infix expression to prefix"""
#     conversion_steps = [
#         f"Original Infix Expression: {expression}",
#         "Step 1: Start with an empty stack and empty prefix expression",
#         "Step 2: Scan the infix expression from right to left",
#         "Step 3: Apply conversion rules for operators and parentheses",
#         f"Converted Prefix Expression: {expression}",  # Placeholder
#     ]
#     converted_expression = expression  # Placeholder
#     return {"conversion_steps": conversion_steps, "converted_expression": converted_expression}


# def infix_to_postfix(expression):
#     """Convert infix expression to postfix"""
#     conversion_steps = [
#         f"Original Infix Expression: {expression}",
#         "Step 1: Start with an empty stack and empty postfix expression",
#         "Step 2: Scan the infix expression from left to right",
#         "Step 3: Apply conversion rules for operators and parentheses",
#         f"Converted Postfix Expression: {expression}",  # Placeholder
#     ]
#     converted_expression = expression  # Placeholder
#     return {"conversion_steps": conversion_steps, "converted_expression": converted_expression}


# def prefix_calculate(expression):
#     try:
#         # Detailed error handling
#         if not expression:
#             raise ValueError("Expression cannot be empty")

#         calculation_steps = [
#             f"Prefix Expression: {expression}",
#             "Step 1: Initialize an empty stack",
#             "Step 2: Scan prefix expression from right to left",
#             "Step 3: When an operand is encountered, push to stack",
#             "Step 4: When an operator is encountered, pop operands and apply",
#             "Step 5: Push result back to stack",
#             "Final stack will contain the result",
#         ]
#         result = 42  # Placeholder calculation
#         return {"steps": calculation_steps, "result": result}
#     except Exception as e:
#         print(f"Prefix Calculation Error: {e}")
#         print(traceback.format_exc())
#         raise


# def postfix_calculate(expression):
#     try:
#         # Detailed error handling
#         if not expression:
#             raise ValueError("Expression cannot be empty")

#         calculation_steps = [
#             f"Postfix Expression: {expression}",
#             "Step 1: Initialize an empty stack",
#             "Step 2: Scan postfix expression from left to right",
#             "Step 3: When an operand is encountered, push to stack",
#             "Step 4: When an operator is encountered, pop operands and apply",
#             "Step 5: Push result back to stack",
#             "Final stack will contain the result",
#         ]
#         result = 42  # Placeholder calculation
#         return {"steps": calculation_steps, "result": result}
#     except Exception as e:
#         print(f"Postfix Calculation Error: {e}")
#         print(traceback.format_exc())
#         raise


@app.post("/api/calculate", response_model=CalculationResponse)
async def calculate(request: CalculationRequest):
    try:
        print(f"Received request: {request}")

        expression = request.expression
        mode = request.mode.lower()

        # Conversion step
        if mode == "prefix":
            prefix, conversion_steps = prefix_expression.infix_to_prefix(expression)
            final_result, calculate_steps = prefix_expression.calculate_prefix(prefix)
        elif mode == "postfix":
            postfix, conversion_steps = postfix_expression.infix_to_postfix(expression)
            final_result, calculate_steps = postfix_expression.calculate_postfix(postfix)
        else:
            raise HTTPException(status_code=400, detail="Invalid calculation mode. Use 'prefix' or 'postfix'.")

        return {
            "conversion_steps": conversion_steps,
            "calculate_steps": calculate_steps,
            "final_result": final_result,
        }
    except Exception as e:
        print(f"Calculation Endpoint Error: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}") from e
