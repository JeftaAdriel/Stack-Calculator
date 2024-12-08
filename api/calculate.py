from fastapi import FastAPI, HTTPException
# from .routers.prefix import convert_to_prefix, evaluate_prefix
# from .routers.postfix import convert_to_postfix, evaluate_postfix

app = FastAPI()


# @app.post("/calculate")
# async def calculate(expression: str, mode: str):
#     if mode == "prefix":
#         converted = convert_to_prefix(expression)
#         result = evaluate_prefix(converted)
#     elif mode == "postfix":
#         converted = convert_to_postfix(expression)
#         result = evaluate_postfix(converted)
#     else:
#         raise HTTPException(status_code=400, detail="Invalid mode")

    return {"converted": converted, "result": result}
