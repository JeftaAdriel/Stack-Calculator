from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import traceback

# from backend.prefix import prefix_calculate  # Import your prefix logic
# from backend.postfix import postfix_calculate  # Import your postfix logic


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
    steps: list[str]
    final_result: float


def prefix_calculate(expression):
    try:
        # Detailed error handling
        if not expression:
            raise ValueError("Expression cannot be empty")

        steps = [f"Received prefix expression: {expression}", "Step 1: Convert expression to prefix notation", "Step 2: Evaluate prefix expression"]
        result = 42  # Placeholder
        return {"steps": steps, "result": result}
    except Exception as e:
        print(f"Prefix Calculation Error: {e}")
        print(traceback.format_exc())
        raise


def postfix_calculate(expression):
    try:
        # Detailed error handling
        if not expression:
            raise ValueError("Expression cannot be empty")

        steps = [
            f"Received postfix expression: {expression}",
            "Step 1: Convert expression to postfix notation",
            "Step 2: Evaluate postfix expression",
        ]
        result = 42  # Placeholder
        return {"steps": steps, "result": result}
    except Exception as e:
        print(f"Postfix Calculation Error: {e}")
        print(traceback.format_exc())
        raise


@app.post("/api/calculate", response_model=CalculationResponse)
async def calculate(request: CalculationRequest):
    try:
        print(f"Received request: {request}")

        expression = request.expression
        mode = request.mode.lower()

        if mode == "prefix":
            result = prefix_calculate(expression)
        elif mode == "postfix":
            result = postfix_calculate(expression)
        else:
            raise HTTPException(status_code=400, detail="Invalid calculation mode. Use 'prefix' or 'postfix'.")

        return {"steps": result.get("steps", []), "final_result": result.get("result", None)}
    except Exception as e:
        print(f"Calculation Endpoint Error: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
