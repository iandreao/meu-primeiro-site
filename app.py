from flask import Flask, render_template, request
from datetime import datetime
import os

app = Flask(__name__)
NOME_ARQUIVO = "historico_web.csv"

# Rota principal do site
@app.route("/", methods=["GET", "POST"])
def home():
    resultado = None
    cor_classe = ""
    
    # Se o usuário preencheu o formulário e clicou no botão
    if request.method == "POST":
        nome = request.form.get("nome")
        peso_txt = request.form.get("peso")
        altura_txt = request.form.get("altura")
        
        if nome and peso_txt and altura_txt:
            try:
                peso = float(peso_txt.replace(",", "."))
                altura = float(altura_txt.replace(",", "."))
                imc = peso / (altura * altura)
                data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
                
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
                
                # Salva no histórico da versão web
                if not os.path.exists(NOME_ARQUIVO):
                    with open(NOME_ARQUIVO, "w", encoding="utf-8") as f:
                        f.write("Data;Nome;Peso;Altura;IMC;Classificacao\n")
                        
                with open(NOME_ARQUIVO, "a", encoding="utf-8") as f:
                    f.write(f"{data_atual};{nome};{peso};{altura};{imc:.2f};{classificacao}\n")
                    
            except ValueError:
                resultado = "Erro: Digite apenas números válidos para Peso e Altura!"
                cor_classe = "danger"

    return render_template("index.html", resultado=resultado, cor_classe=cor_classe)

if __name__ == "__main__":
    # O servidor da nuvem vai ler a variável PORT automaticamente
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

