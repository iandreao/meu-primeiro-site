from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HealthCheck Web - IMC</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #1a2332; color: #ffffff; max-width: 450px; margin: 50px auto; padding: 20px; text-align: center; }
        h1 { margin-bottom: 5px; font-size: 28px; }
        p { color: #8a99ad; margin-bottom: 30px; font-size: 14px; }
        .card { background-color: #243145; padding: 30px; border-radius: 8px; text-align: left; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 8px; font-size: 11px; text-transform: uppercase; color: #8a99ad; font-weight: bold; }
        input[type="text"] { width: 100%; padding: 12px; box-sizing: border-box; background-color: #ffffff !important; color: #000000 !important; border: 1px solid #ccc; border-radius: 6px; font-size: 14px; }
        button { background-color: #0081cb; color: white; padding: 14px; border: none; border-radius: 6px; cursor: pointer; width: 100%; font-size: 15px; font-weight: bold; margin-top: 10px; }
        button:hover { background-color: #006dab; }
        .alert { padding: 12px; margin-top: 20px; border-radius: 6px; font-weight: bold; text-align: center; font-size: 14px; }
        .warning { background-color: #fff3cd; color: #856404; }
        .success { background-color: #d4edda; color: #155724; }
        .danger { background-color: #f8d7da; color: #721c24; }
    </style>
</head>
<body>
    <h1>HealthCheck Web</h1>
    <p>Calcular o IMC direto na Web</p>
    <div class="card">
        <form method="POST">
            <div class="form-group">
                <label>Nome Completo</label>
                <input type="text" name="nome" required placeholder="Ex: João Silva">
            </div>
            <div class="form-group">
                <label>Peso Atual (kg)</label>
                <input type="text" name="peso" required placeholder="Ex: 75.2">
            </div>
            <div class="form-group">
                <label>Altura Atual (m)</label>
                <input type="text" name="altura" required placeholder="Ex: 1.78">
            </div>
            <button type="submit">Calcular e Registrar</button>
        </form>
        {% if resultado %}
            <div class="alert {{ cor_classe }}">
                {{ resultado }}
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    resultado = None
    cor_classe = ""
    if request.method == "POST":
        nome = request.form.get("nome")
        peso_txt = request.form.get("peso")
        altura_txt = request.form.get("altura")
        if nome and peso_txt and altura_txt:
            try:
                peso = float(peso_txt.replace(",", "."))
                altura = float(altura_txt.replace(",", "."))
                imc = peso / (altura * altura)
                if imc < 18.5:
                    classificacao = "Abaixo do peso"
                    cor_classe = "warning"
                elif imc >= 18.5 and imc < 25:
                    classificacao = "Peso normal"
                    cor_classe = "success"
                else:
                    classificacao = "Acima do peso"
                    cor_classe = "danger"
                resultado = f"Olá {nome}! Seu IMC é {imc:.2f} ({classificacao})"
            except ValueError:
                resultado = "Erro: Digite apenas números válidos!"
                cor_classe = "danger"
    return render_template_string(HTML_TEMPLATE, resultado=resultado, cor_classe=cor_classe)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

