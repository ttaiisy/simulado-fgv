import pandas as pd

# Lê o Excel
df = pd.read_excel("questoes_extraidas.xlsx")

html = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Simulado FGV com Feedback e Pontuação</title>
  <style>
    body { font-family: Arial, sans-serif; padding: 20px; background-color: #f6f6f6; }
    .questao-container { display: none; background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
    .questao-container.active { display: block; }
    .numero { font-weight: bold; color: #005999; margin-bottom: 10px; }
    .alternativa { margin: 8px 0; padding: 5px; border-radius: 4px; }
    .alternativa.certa { background-color: #d4edda; }
    .alternativa.errada { background-color: #f8d7da; }
    .botoes { margin-top: 20px; }
    button { padding: 10px 15px; margin-right: 10px; cursor: pointer; }
    #resultado { margin-top: 30px; font-size: 18px; font-weight: bold; color: #005999; }
  </style>
</head>
<body>

<h1>Simulado FGV com Feedback Imediato + Pontuação Final</h1>
<div id="questoes">
"""

# Gera as questões
for i, row in df.iterrows():
    gab = str(row['Gabarito']).strip().upper()
    enunciado = str(row['Enunciado']).replace('\n', '<br>')

    def alternativa(letra, texto):
        return f"""
        <div class="alternativa" data-letra="{letra}">
          <input type="radio" name="q{i}" value="{letra}" id="q{i}{letra.lower()}" onclick="verificarResposta({i}, '{letra}')">
          <label for="q{i}{letra.lower()}">{letra}) {texto}</label>
        </div>
        """

    html += f"""
    <div class="questao-container" id="questao-{i}" data-gabarito="{gab}">
      <div class="numero">Questão {row['Número']}</div>
      <p>{enunciado}</p>
      {alternativa('A', row['A'])}
      {alternativa('B', row['B'])}
      {alternativa('C', row['C'])}
      {alternativa('D', row['D'])}
      {alternativa('E', row['E'])}
    </div>
    """

# Fecha div de questões, adiciona botões e script
html += """
</div>

<div class="botoes">
  <button onclick="anterior()">Anterior</button>
  <button onclick="proxima()">Próxima</button>
  <button onclick="mostrarPontuacao()">Ver Pontuação</button>
</div>

<div id="resultado"></div>

<script>
  let questoes = document.querySelectorAll(".questao-container");
  let atual = 0;
  let respostas = {}; // Guarda as respostas

  function mostrarQuestao(index) {
    questoes.forEach((q, i) => {
      q.classList.toggle("active", i === index);
    });
  }

  function proxima() {
    if (atual < questoes.length - 1) {
      atual++;
      mostrarQuestao(atual);
    }
  }

  function anterior() {
    if (atual > 0) {
      atual--;
      mostrarQuestao(atual);
    }
  }

  function verificarResposta(index, letra) {
    const questao = document.getElementById("questao-" + index);
    const gabarito = questao.getAttribute("data-gabarito");
    const alternativas = questao.querySelectorAll(".alternativa");

    // Impede mudança depois de responder
    alternativas.forEach(alt => {
      alt.querySelector("input").disabled = true;
    });

    // Salva a resposta
    respostas[index] = letra;

    if (letra === gabarito) {
      const correta = questao.querySelector(`.alternativa[data-letra="${letra}"]`);
      correta.classList.add("certa");
    } else {
      const errada = questao.querySelector(`.alternativa[data-letra="${letra}"]`);
      const correta = questao.querySelector(`.alternativa[data-letra="${gabarito}"]`);
      errada.classList.add("errada");
      correta.classList.add("certa");
    }
  }

  function mostrarPontuacao() {
    let acertos = 0;

    questoes.forEach((q, index) => {
      let gabarito = q.getAttribute("data-gabarito");
      let resposta = respostas[index];

      if (resposta === gabarito) {
        acertos++;
      }
    });

    let total = questoes.length;
    let percentual = ((acertos / total) * 100).toFixed(2);

    document.getElementById("resultado").innerText = `✅ Você acertou ${acertos} de ${total} questões (${percentual}%)`;
  }

  mostrarQuestao(atual);
</script>

</body>
</html>
"""

# Salva o arquivo
with open("simulado_feedback_pontuacao.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ Arquivo gerado: simulado_feedback_pontuacao.html")
