from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# from backend.prefix import prefix_calculate  # Import your prefix logic
# from backend.postfix import postfix_calculate  # Import your postfix logic


def prefix_calculate(expression):
    # Perform prefix calculation
    steps = ["Step 1: Convert expression to prefix notation", "Step 2: Evaluate prefix expression"]
    result = 42  # Replace with actual calculation
    return {"steps": steps, "result": result}


def postfix_calculate(expression):
    # Perform postfix calculation
    steps = ["Step 1: Convert expression to postfix notation", "Step 2: Evaluate postfix expression"]
    result = 42  # Replace with actual calculation
    return {"steps": steps, "result": result}


# FastAPI app instance
app = FastAPI()


# Request Body Schema
class CalculationRequest(BaseModel):
    expression: str
    mode: str


# Response Body Schema (optional, for clarity)
class CalculationResponse(BaseModel):
    steps: list[str]
    final_result: float


@app.post("/calculate", response_model=CalculationResponse)
async def calculate(request: CalculationRequest):
    """
    Endpoint to perform stack-based calculations.
    """
    try:
        # Extract input values
        expression = request.expression
        mode = request.mode.lower()

        # Perform calculation based on mode
        if mode == "prefix":
            result = prefix_calculate(expression)
        elif mode == "postfix":
            result = postfix_calculate(expression)
        else:
            raise HTTPException(status_code=400, detail="Invalid calculation mode. Use 'prefix' or 'postfix'.")

        # Prepare response
        return {"steps": result.get("steps", []), "final_result": result.get("result", None)}  # Step-by-step calculations  # Final result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}") from e
