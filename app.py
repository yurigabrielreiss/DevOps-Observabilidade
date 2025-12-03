from flask import Flask, Response
from prometheus_client import Counter, generate_latest

app = Flask(__name__)

# Métrica para o Prometheus monitorar
VOTOS = Counter('app_votos_total', 'Total de votos computados',
['opcao'])

@app.route('/')
def home():
    return "<h1>Sistema de Votação</h1><p>Vote acessando: <a
href='/votar/a'>/votar/a</a> ou <a
href='/votar/b'>/votar/b</a></p>"

@app.route('/votar/<opcao>')
def votar(opcao):
    if opcao.lower() in ['a', 'b']:
        VOTOS.labels(opcao=opcao.lower()).inc()
        return f"Voto computado para: {opcao.upper()}!"
    return "Opção inválida! Tente A ou B.", 400

@app.route('/metrics')
def metrics():
    # Rota que expõe as métricas para o Prometheus
    return Response(generate_latest(), mimetype='text/plain')

if __name__ == '__main__':
 app.run(host='0.0.0.0', port=5000)