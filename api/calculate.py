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
