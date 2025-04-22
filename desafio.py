import re
import unicodedata

positivas = {
    "bom", "otimo", "excelente", "maneiro", "gostei", "massa", "legal", "top", "daora", "agradavel", "simples", "direto", "melhor"
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

def preprocessar(texto):
    texto = texto.lower()

    for original, substituto in substituicoes.items():
        texto = texto.replace(original, substituto)

    texto = unicodedata.normalize('NFD', texto).encode('ascii', 'ignore').decode('utf-8')

    texto = re.sub(r'[^\w\s-]', '', texto)  

    return texto

def analisar_sentimento(comentario_original):
    comentario = preprocessar(comentario_original)
    palavras = comentario.split()

    score = 0
    distancia_max = 2
    indices_intensificadores = [i for i, p in enumerate(palavras) if p in intensificadores]

    if any(p in palavras for p in ironicos):
        return "Irônico"

    if any(p in palavras for p in construtivos):
        return "Crítica Construtiva"

    # Calcular score
    for i, palavra in enumerate(palavras):
        if palavra in positivas:
            intensificador_perto = any(abs(i - j) <= distancia_max for j in indices_intensificadores)
            score += 2 if intensificador_perto else 1
        elif palavra in negativas:
            intensificador_perto = any(abs(i - j) <= distancia_max for j in indices_intensificadores)
            score -= 2 if intensificador_perto else 1

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

# --- Execução com validações ---
quantidade = input("Quantos comentários deseja analisar? ").strip()

while quantidade == "" or not quantidade.isdigit():
    if quantidade == "":
        print("Você não digitou nada. Tente novamente.")
    else:
        print("Entrada inválida. Digite apenas números.")
    quantidade = input("Digite apenas números: ").strip()

n = int(quantidade)

for i in range(n):
    comentario = ""
    while comentario == "":
        comentario = input(f"\nComentário {i + 1}: ").strip()
        if comentario == "":
            print("Você não digitou nada. Por favor, digite um comentário válido.")
    
    resultado = analisar_sentimento(comentario)
    print(f"Resultado: {resultado}")


# Lista de exemplos de comentarios:
"""

Achei super legal, ficou muito melhor do que eu esperava!

Sinceramente, isso ficou horrível pra caramba, não tem condição.

Seria melhor revisar essa parte antes de publicar, tem alguns pontos confusos.

Uau, que projeto incrível... só que não.

Gostei bastante, tá muito bom mesmo.

Esse resultado ficou ruim e meio chato de acompanhar.

Ficou ótimo, mas falta um pouco mais de clareza nos detalhes.

Tabom... jogar-fora, talvez seja o melhor destino mesmo.

Li o conteúdo todo, analisei bem, e ainda estou refletindo sobre ele.

Muito bom, excelente trabalho, direto ao ponto e super agradável de ver.
"""