from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from typing import Optional

app = FastAPI(title="Calculator App")

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CALC</title>
    <link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=Bebas+Neue&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

        :root {{
            --bg: #0a0a0a;
            --surface: #111111;
            --surface2: #1a1a1a;
            --border: #2a2a2a;
            --accent: #e8ff47;
            --accent2: #ff6b35;
            --text: #f0f0f0;
            --muted: #555;
            --error: #ff4444;
        }}

        body {{
            background: var(--bg);
            color: var(--text);
            font-family: 'DM Mono', monospace;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow-y: auto;
            padding: 20px 0;
        }}

        /* Background grid */
        body::before {{
            content: '';
            position: fixed;
            inset: 0;
            background-image:
                linear-gradient(var(--border) 1px, transparent 1px),
                linear-gradient(90deg, var(--border) 1px, transparent 1px);
            background-size: 60px 60px;
            opacity: 0.4;
            z-index: 0;
        }}

        /* Glow blob */
        body::after {{
            content: '';
            position: fixed;
            top: -20%;
            left: 30%;
            width: 500px;
            height: 500px;
            background: radial-gradient(circle, rgba(232,255,71,0.06) 0%, transparent 70%);
            border-radius: 50%;
            z-index: 0;
            animation: float 8s ease-in-out infinite;
        }}

        @keyframes float {{
            0%, 100% {{ transform: translate(0, 0); }}
            50% {{ transform: translate(-30px, 30px); }}
        }}

        .wrapper {{
            position: relative;
            z-index: 1;
            width: 100%;
            max-width: 480px;
            padding: 20px;
        }}

        /* Header */
        .header {{
            display: flex;
            align-items: baseline;
            gap: 12px;
            margin-bottom: 40px;
        }}

        .header h1 {{
            font-family: 'Bebas Neue', sans-serif;
            font-size: 72px;
            letter-spacing: 4px;
            color: var(--accent);
            line-height: 1;
        }}

        .header .tag {{
            font-size: 11px;
            letter-spacing: 3px;
            color: var(--muted);
            text-transform: uppercase;
            border: 1px solid var(--border);
            padding: 4px 8px;
            border-radius: 2px;
        }}

        /* Calculator card */
        .card {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 4px;
            padding: 32px;
            position: relative;
        }}

        .card::before {{
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 2px;
            background: linear-gradient(90deg, var(--accent), var(--accent2), transparent);
        }}

        /* Display */
        .display {{
            background: var(--bg);
            border: 1px solid var(--border);
            border-radius: 3px;
            padding: 20px 24px;
            margin-bottom: 28px;
            min-height: 80px;
            position: relative;
            overflow: hidden;
        }}

        .display::after {{
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: repeating-linear-gradient(
                0deg,
                transparent,
                transparent 2px,
                rgba(255,255,255,0.01) 2px,
                rgba(255,255,255,0.01) 4px
            );
            pointer-events: none;
        }}

        .display-label {{
            font-size: 10px;
            letter-spacing: 3px;
            color: var(--muted);
            text-transform: uppercase;
            margin-bottom: 8px;
        }}

        .display-value {{
            font-size: 32px;
            font-weight: 300;
            color: var(--text);
            letter-spacing: -1px;
            transition: all 0.3s ease;
        }}

        .display-value.result {{
            color: var(--accent);
        }}

        .display-value.error {{
            color: var(--error);
            font-size: 18px;
        }}

        /* Input grid */
        .input-row {{
            display: grid;
            grid-template-columns: 1fr auto 1fr;
            gap: 10px;
            align-items: center;
            margin-bottom: 24px;
        }}

        .field-group {{
            display: flex;
            flex-direction: column;
            gap: 6px;
        }}

        label {{
            font-size: 10px;
            letter-spacing: 3px;
            color: var(--muted);
            text-transform: uppercase;
        }}

        input[type="number"] {{
            background: var(--surface2);
            border: 1px solid var(--border);
            color: var(--text);
            font-family: 'DM Mono', monospace;
            font-size: 18px;
            padding: 14px 16px;
            border-radius: 3px;
            width: 100%;
            outline: none;
            transition: border-color 0.2s, background 0.2s;
            -moz-appearance: textfield;
        }}

        input[type="number"]::-webkit-outer-spin-button,
        input[type="number"]::-webkit-inner-spin-button {{
            -webkit-appearance: none;
        }}

        input[type="number"]:focus {{
            border-color: var(--accent);
            background: #161616;
        }}

        /* Op selector */
        .op-selector {{
            display: flex;
            flex-direction: column;
            gap: 4px;
            padding-top: 20px;
        }}

        .op-btn {{
            width: 44px;
            height: 44px;
            background: var(--surface2);
            border: 1px solid var(--border);
            color: var(--muted);
            font-family: 'DM Mono', monospace;
            font-size: 18px;
            cursor: pointer;
            border-radius: 3px;
            transition: all 0.15s ease;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .op-btn:hover {{
            border-color: var(--accent);
            color: var(--accent);
            background: rgba(232,255,71,0.05);
        }}

        .op-btn.active {{
            background: var(--accent);
            border-color: var(--accent);
            color: var(--bg);
            font-weight: 500;
        }}

        /* Hidden select for form submission */
        #operation {{
            display: none;
        }}

        /* Submit */
        .submit-btn {{
            width: 100%;
            padding: 16px;
            background: var(--accent);
            border: none;
            color: var(--bg);
            font-family: 'Bebas Neue', sans-serif;
            font-size: 22px;
            letter-spacing: 4px;
            cursor: pointer;
            border-radius: 3px;
            transition: all 0.2s ease;
            position: relative;
            overflow: hidden;
        }}

        .submit-btn::before {{
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(135deg, transparent 40%, rgba(255,255,255,0.1) 50%, transparent 60%);
            transform: translateX(-100%);
            transition: transform 0.4s ease;
        }}

        .submit-btn:hover::before {{
            transform: translateX(100%);
        }}

        .submit-btn:hover {{
            background: #d4eb2e;
            transform: translateY(-1px);
            box-shadow: 0 8px 30px rgba(232,255,71,0.3);
        }}

        .submit-btn:active {{
            transform: translateY(0);
        }}

        /* History */
        .history {{
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid var(--border);
        }}

        .history-label {{
            font-size: 10px;
            letter-spacing: 3px;
            color: var(--muted);
            text-transform: uppercase;
            margin-bottom: 10px;
        }}

        .history-list {{
            display: flex;
            flex-direction: column;
            gap: 4px;
            max-height: 120px;
            overflow-y: auto;
        }}

        .history-item {{
            font-size: 12px;
            color: var(--muted);
            padding: 6px 10px;
            background: var(--surface2);
            border-radius: 2px;
            display: flex;
            justify-content: space-between;
            cursor: pointer;
            transition: color 0.15s;
        }}

        .history-item:hover {{
            color: var(--text);
        }}

        .history-item .hist-result {{
            color: var(--accent);
        }}

        /* Footer */
        .footer {{
            margin-top: 24px;
            text-align: center;
            font-size: 10px;
            letter-spacing: 2px;
            color: #333;
            text-transform: uppercase;
        }}

        /* Pulse animation on result */
        @keyframes pulse {{
            0% {{ opacity: 0; transform: translateY(4px); }}
            100% {{ opacity: 1; transform: translateY(0); }}
        }}

        .animate-in {{
            animation: pulse 0.3s ease forwards;
        }}
    </style>
</head>
<body>
<div class="wrapper">
    <div class="header">
        <h1>CALC</h1>
        <span class="tag">v2.0 · Railway</span>
    </div>

    <div class="card">
        <!-- Display -->
        <div class="display">
            <div class="display-label">Output</div>
            <div class="display-value {result_class} {animate_class}" id="display">{display_value}</div>
        </div>

        <!-- Form -->
        <form action="/" method="get" id="calcForm">
            <select name="operation" id="operation">
                <option value="add" {sel_add}>+</option>
                <option value="subtract" {sel_sub}>-</option>
                <option value="multiply" {sel_mul}>×</option>
                <option value="divide" {sel_div}>÷</option>
            </select>

            <div class="input-row">
                <div class="field-group">
                    <label for="a">A</label>
                    <input type="number" name="a" id="a" step="any" placeholder="0" value="{val_a}" required autocomplete="off">
                </div>

                <div class="op-selector">
                    <button type="button" class="op-btn {cls_add}" onclick="setOp('add')">+</button>
                    <button type="button" class="op-btn {cls_sub}" onclick="setOp('subtract')">−</button>
                    <button type="button" class="op-btn {cls_mul}" onclick="setOp('multiply')">×</button>
                    <button type="button" class="op-btn {cls_div}" onclick="setOp('divide')">÷</button>
                </div>

                <div class="field-group">
                    <label for="b">B</label>
                    <input type="number" name="b" id="b" step="any" placeholder="0" value="{val_b}" required autocomplete="off">
                </div>
            </div>

            <button type="submit" class="submit-btn">CALCULATE</button>
        </form>

        <!-- History -->
        <div class="history" id="historySection" style="display:none">
            <div class="history-label">History</div>
            <div class="history-list" id="historyList"></div>
        </div>
    </div>

    <div class="footer">arithmetic · railway · 2025</div>
</div>

<script>
    // Operation selection
    function setOp(op) {{
        document.getElementById('operation').value = op;
        document.querySelectorAll('.op-btn').forEach(b => b.classList.remove('active'));
        event.currentTarget.classList.add('active');
    }}

    // Live display preview
    function updateDisplay() {{
        const a = parseFloat(document.getElementById('a').value);
        const b = parseFloat(document.getElementById('b').value);
        const op = document.getElementById('operation').value;
        const display = document.getElementById('display');

        const symbols = {{ add: '+', subtract: '−', multiply: '×', divide: '÷' }};

        if (!isNaN(a) && !isNaN(b)) {{
            display.textContent = a + ' ' + (symbols[op] || op) + ' ' + b;
            display.className = 'display-value';
        }} else if (!isNaN(a)) {{
            display.textContent = a + ' ' + (symbols[op] || op) + ' ?';
            display.className = 'display-value';
        }} else {{
            display.textContent = '{display_placeholder}';
            display.className = 'display-value';
        }}
    }}

    document.getElementById('a').addEventListener('input', updateDisplay);
    document.getElementById('b').addEventListener('input', updateDisplay);

    // History
    const HISTORY_KEY = 'calc_history';

    function loadHistory() {{
        try {{ return JSON.parse(localStorage.getItem(HISTORY_KEY)) || []; }}
        catch {{ return []; }}
    }}

    function saveHistory(entry) {{
        const h = loadHistory();
        h.unshift(entry);
        const trimmed = h.slice(0, 10);
        try {{ localStorage.setItem(HISTORY_KEY, JSON.stringify(trimmed)); }} catch {{}}
        renderHistory(trimmed);
    }}

    function renderHistory(items) {{
        const section = document.getElementById('historySection');
        const list = document.getElementById('historyList');
        if (!items.length) {{ section.style.display = 'none'; return; }}
        section.style.display = 'block';
        list.innerHTML = items.map(item =>
            `<div class="history-item" onclick="fillFrom('${{item.a}}','${{item.b}}','${{item.op}}')">
                <span>${{item.expr}}</span>
                <span class="hist-result">${{item.result}}</span>
            </div>`
        ).join('');
    }}

    function fillFrom(a, b, op) {{
        document.getElementById('a').value = a;
        document.getElementById('b').value = b;
        document.getElementById('operation').value = op;
        document.querySelectorAll('.op-btn').forEach(btn => btn.classList.remove('active'));
        const opMap = {{ add: 0, subtract: 1, multiply: 2, divide: 3 }};
        const btns = document.querySelectorAll('.op-btn');
        if (btns[opMap[op]]) btns[opMap[op]].classList.add('active');
        updateDisplay();
    }}

    // On load
    window.addEventListener('DOMContentLoaded', () => {{
        renderHistory(loadHistory());

        // If we got a result, save it
        const hasResult = {has_result};
        if (hasResult) {{
            const expr = '{expr_js}';
            const result = '{result_js}';
            const a = '{js_a}';
            const b = '{js_b}';
            const op = '{js_op}';
            if (expr && result) {{
                saveHistory({{ expr, result, a, b, op }});
            }}
        }}
    }});
</script>
</body>
</html>"""


@app.get("/")
def home(
    a: Optional[float] = None,
    b: Optional[float] = None,
    operation: Optional[str] = None
):
    # Defaults
    display_value = "ready"
    display_placeholder = "ready"
    result_class = ""
    animate_class = ""
    has_result = "false"
    expr_js = ""
    result_js = ""

    val_a = str(a) if a is not None else ""
    val_b = str(b) if b is not None else ""

    op = operation if operation in ("add", "subtract", "multiply", "divide") else "add"

    sel_add = "selected" if op == "add" else ""
    sel_sub = "selected" if op == "subtract" else ""
    sel_mul = "selected" if op == "multiply" else ""
    sel_div = "selected" if op == "divide" else ""

    cls_add = "active" if op == "add" else ""
    cls_sub = "active" if op == "subtract" else ""
    cls_mul = "active" if op == "multiply" else ""
    cls_div = "active" if op == "divide" else ""

    op_symbols = {"add": "+", "subtract": "−", "multiply": "×", "divide": "÷"}
    js_a = ""
    js_b = ""
    js_op = op

    if a is not None and b is not None and operation in op_symbols:
        sym = op_symbols[operation]

        if operation == "add":
            res = a + b
        elif operation == "subtract":
            res = a - b
        elif operation == "multiply":
            res = a * b
        elif operation == "divide":
            if b == 0:
                res = None
            else:
                res = a / b
        else:
            res = None

        if res is None:
            display_value = "Division by zero"
            result_class = "error"
            animate_class = "animate-in"
        else:
            # Format cleanly: remove trailing .0 for whole numbers
            def fmt(n):
                if isinstance(n, float) and n.is_integer():
                    return str(int(n))
                return f"{n:.6g}"

            display_value = f"{fmt(a)} {sym} {fmt(b)} = {fmt(res)}"
            result_class = "result"
            animate_class = "animate-in"
            has_result = "true"
            expr_js = f"{fmt(a)} {sym} {fmt(b)}"
            result_js = fmt(res)
            js_a = fmt(a)
            js_b = fmt(b)
            js_op = operation

    html = HTML_TEMPLATE.format(
        display_value=display_value,
        display_placeholder=display_placeholder,
        result_class=result_class,
        animate_class=animate_class,
        val_a=val_a,
        val_b=val_b,
        sel_add=sel_add,
        sel_sub=sel_sub,
        sel_mul=sel_mul,
        sel_div=sel_div,
        cls_add=cls_add,
        cls_sub=cls_sub,
        cls_mul=cls_mul,
        cls_div=cls_div,
        has_result=has_result,
        expr_js=expr_js,
        result_js=result_js,
        js_a=js_a,
        js_b=js_b,
        js_op=js_op,
    )

    return HTMLResponse(content=html)