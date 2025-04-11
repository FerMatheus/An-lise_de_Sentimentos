import re
import unicodedata

palavras_positivas = {"bom", "otimo", "excelente", "maneiro", "gostei", "massa", "legal", "top", "daora"}
palavras_negativas = {"ruim", "pessimo", "horrivel", "chato", "sem condicao", "jogar fora", "lixo"}
indicadores_ironicos = {"só que não", "aham", "sei", "legal né", "tabom", "imagina", "uau", "topzera", "só que ruim"}
indicadores_construtivos = {"mas", "porém", "contudo", "todavia", "seria melhor", "sugiro", "precisa melhorar", "falta"}
indicadores_intensivos = {"muito", "demais", "super", "incrivelmente", "extremamente", "totalmente", "pra caramba"}

quantidade = int(input("Quantos comentários você deseja analisar? "))

for i in range(quantidade):
    comentario_original = input(f"Digite o comentário {i + 1}: ")

    comentario = re.sub(r'[^\w\s]', '', comentario_original)
    comentario = unicodedata.normalize('NFD', comentario).encode('ascii', 'ignore').decode('utf-8')
    comentario = comentario.lower()

    ironico = False
    for expr in indicadores_ironicos:
        if expr in comentario:
            ironico = True

    construtivo = False
    for expr in indicadores_construtivos:
        if expr in comentario:
            construtivo = True

    tem_intensificador = False
    for expr in indicadores_intensivos:
        if expr in comentario:
            tem_intensificador = True

    palavras = comentario.split()
    score = 0

    for palavra in palavras:
        if palavra in palavras_positivas:
            score += 1
        elif palavra in palavras_negativas:
            score -= 1

    # Aplica intensificação depois da contagem
    if tem_intensificador:
        score *= 2

    # Inverte se for irônico
    if ironico:
        score *= -1

    if score >= 2:
        classificacao = "Muito Positivo"
    elif score == 1:
        classificacao = "Positivo"
    elif score == 0:
        classificacao = "Neutro"
    elif score == -1:
        classificacao = "Negativo"
    else:
        classificacao = "Muito Negativo"

    if construtivo and classificacao != "Neutro":
        classificacao += " (Construtivo)"

    print(f"{comentario_original} => {classificacao} (Score: {score})")
