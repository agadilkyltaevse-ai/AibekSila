from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from typing import Optional

app = FastAPI(title="Calculator App")

@app.get("/")
def home(a: Optional[float] = None, b: Optional[float] = None, operation: Optional[str] = None):
    result_html = ""
    if a is not None and b is not None and operation is not None:
        if operation == "add":
            res = a + b
        elif operation == "subtract":
            res = a - b
        elif operation == "multiply":
            res = a * b
        elif operation == "divide":
            if b == 0:
                res = "Error: Division by zero"
            else:
                res = a / b
        else:
            res = "Invalid operation"
            
        if isinstance(res, str) and res.startswith("Error"):
            result_html = f"<h3 style='color:red;'>{res}</h3>"
        else:
            result_html = f"<h3>Result: {a} {operation} {b} = {res}</h3>"

    html_content = f"""
    <html>
        <head>
            <title>Calculator</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 50px; text-align: center; }}
                input, select, button {{ padding: 10px; margin: 5px; font-size: 16px; }}
            </style>
        </head>
        <body>
            <h2>Railway Calculator App</h2>
            <form action="/" method="get">
                <input type="number" name="a" step="any" required placeholder="Number 1" value="{a if a is not None else ''}">
                <select name="operation">
                    <option value="add" {'selected' if operation=='add' else ''}>+</option>
                    <option value="subtract" {'selected' if operation=='subtract' else ''}>-</option>
                    <option value="multiply" {'selected' if operation=='multiply' else ''}>*</option>
                    <option value="divide" {'selected' if operation=='divide' else ''}>/</option>
                </select>
                <input type="number" name="b" step="any" required placeholder="Number 2" value="{b if b is not None else ''}">
                <br><br>
                <button type="submit">Calculate</button>
            </form>
            <hr>
            {result_html}
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)
