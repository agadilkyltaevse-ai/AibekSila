from fastapi import FastAPI
from fastapi.responses import HTMLResponse
app = FastAPI(title="Calculator App")
@app.get("/")
def home():
    html_content = """
    <html>
        <head>
            <title>Calculator</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 50px; text-align: center; }
                input, select, button { padding: 10px; margin: 5px; font-size: 16px; }
            </style>
        </head>
        <body>
            <h2>Railway Calculator App</h2>
            <form action="/calculate" method="get">
                <input type="number" name="a" step="any" required placeholder="Number 1">
                <select name="operation">
                    <option value="add">+</option>
                    <option value="subtract">-</option>
                    <option value="multiply">*</option>
                    <option value="divide">/</option>
                </select>
                <input type="number" name="b" step="any" required placeholder="Number 2">
                <br><br>
                <button type="submit">Calculate</button>
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)
@app.get("/calculate")
def calculate(a: float, b: float, operation: str):
    if operation == "add":
        res = a + b
    elif operation == "subtract":
        res = a - b
    elif operation == "multiply":
        res = a * b
    elif operation == "divide":
        if b == 0:
            return HTMLResponse("<h3>Error: Division by zero is not allowed.</h3><a href='/'>Go back</a>")
        res = a / b
    else:
        return {"error": "Invalid operation"}
    return HTMLResponse(f"<h3>Result: {a} {operation} {b} = {res}</h3><br><a href='/'>Calculate again</a>")
