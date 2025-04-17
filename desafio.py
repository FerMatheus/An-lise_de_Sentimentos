import re
import unicodedata

positivas = {
    "bom", "otimo", "excelente", "maneiro", "gostei", "massa", "legal", "top", "daora", "agradavel", "simples", "direto"
}
negativas = {
    "ruim", "pessimo", "horrivel", "chato", "lixo", "jogar-fora", "sem-condicao", "negativamente"
}
intensificadores = {
    "muito", "demais", "super", "incrivelmente", "extremamente", "totalmente", "pra-caramba", "total"
}
ironicos = {
    "so-que-nao", "aham", "sei", "legal-ne", "tabom", "imagina", "uau", "topzera", "so-que-ruim"
}
construtivos = {
    "mas", "porem", "contudo", "todavia", "seria-melhor", "sugiro", "precisa-melhorar", "falta"
}

# --- Substituições para expressões compostas ---
substituicoes = {
    "pra caramba": "pra-caramba",
    "só que não": "so-que-nao",
    "só que ruim": "so-que-ruim",
    "legal né": "legal-ne",
    "seria melhor": "seria-melhor",
    "precisa melhorar": "precisa-melhorar",
    "jogar fora": "jogar-fora",
    "sem condição": "sem-condicao"
}

# --- Função de pré-processamento ---
def preprocessar(texto):
    texto = texto.lower()
    texto = unicodedata.normalize('NFD', texto).encode('ascii', 'ignore').decode('utf-8')
    texto = re.sub(r'[^\w\s]', '', texto)

    for original, substituto in substituicoes.items():
        texto = texto.replace(original, substituto)

    return texto

# --- Função de análise de sentimentos ---
def analisar_sentimento(comentario_original):
    comentario = preprocessar(comentario_original)
    palavras = comentario.split()

    score = 0
    distancia_max = 2
    indices_intensificadores = [i for i, p in enumerate(palavras) if p in intensificadores]

    # Detectar ironia
    if any(p in palavras for p in ironicos):
        return "Irônico"

    # Detectar crítica construtiva
    if any(p in palavras for p in construtivos):
        return "Crítica Construtiva"

    # Calcular score
    for i, palavra in enumerate(palavras):
        if palavra in positivas:
            intensificador_perto = any(abs(i - j) <= distancia_max for j in indices_intensificadores)
            score += 2 if intensificador_perto else 1
        elif palavra in negativas:
            intensificador_perto = any(abs(i - j) <= distancia_max for j in indices_intensificadores)
            score -= 3 if intensificador_perto else 1

    # Classificação baseada no score
    if score >= 3:
        return f"Muito Positivo (Score: {score})"
    elif score == 2:
        return f"Positivo (Score: {score})"
    elif score == 1:
        return f"Levemente Positivo (Score: {score})"
    elif score == 0:
        return f"Neutro (Score: {score})"
    elif score == -1:
        return f"Levemente Negativo (Score: {score})"
    elif score == -2:
        return f"Negativo (Score: {score})"
    else:
        return f"Muito Negativo (Score: {score})"

# --- Execução ---
quantidade = int(input("Quantos comentários deseja analisar? "))

for i in range(quantidade):
    comentario = input(f"\nComentário {i + 1}: ")
    resultado = analisar_sentimento(comentario)
    print(f"Resultado: {resultado}")

# Lista de exemplos de comentarios:
"""

Achei super legal, ficou muito melhor do que eu esperava!
(Positiva)

Sinceramente, isso ficou horrível pra caramba, não tem condição.
(Muito Negativa)

Seria melhor revisar essa parte antes de publicar, tem alguns pontos confusos.
(Crítica construtiva)

Uau, que projeto incrível... só que não.
(Irônica)

Gostei bastante, tá muito bom mesmo.
(Positiva simples)

Esse resultado ficou ruim e meio chato de acompanhar.
(Negativa simples)

Ficou ótimo, mas falta um pouco mais de clareza nos detalhes.
(Construtiva com tom positivo)

Tabom... jogar-fora, talvez seja o melhor destino mesmo.
(Irônica e negativa)

Li o conteúdo todo, analisei bem, e ainda estou refletindo sobre ele.
(Neutra (sem palavras-chave claras))

Muito bom, excelente trabalho, direto ao ponto e super agradável de ver.
(Positiva com várias palavras boas)

"""