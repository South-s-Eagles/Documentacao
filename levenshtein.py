def levenshtein(nome1, nome2):
    if len(nome1) < len(nome2):
        return levenshtein(nome2, nome1)
    if len(nome2) == 0:
        return len(nome1)

    linha_anterior = range(len(nome2) + 1)
    for i, c1 in enumerate(nome1):
        linha_atual = [i + 1]
        for j, c2 in enumerate(nome2):
            insercao = linha_anterior[j + 1] + 1
            exclusao = linha_atual[j] + 1
            substituicao = linha_anterior[j] + (c1 != c2)
            linha_atual.append(min(insercao, exclusao, substituicao))
        linha_anterior = linha_atual
    
    return linha_anterior[-1]

def correcao_nome(nome_incorreto, nome_correto, limiar):
    distancia = levenshtein(nome_incorreto, nome_correto)
    return distancia <= limiar

def destacar_diferencas(nome_incorreto, nome_correto):
    resultado = []
    tamanho_max = max(len(nome_incorreto), len(nome_correto))
    
    for i in range(tamanho_max):
        if i < len(nome_incorreto) and i < len(nome_correto):
            if nome_incorreto[i] != nome_correto[i]:
                resultado.append(f"\033[91m{nome_incorreto[i]}\033[0m")  # Vermelho para letras diferentes
            else:
                resultado.append(nome_incorreto[i])
        elif i < len(nome_incorreto):
            resultado.append(f"\033[91m{nome_incorreto[i]}\033[0m")  # Vermelho para letras adicionais no nome incorreto
        else:
            resultado.append(f"\033[92m{nome_correto[i]}\033[0m")  # Verde para letras faltantes no nome incorreto
    
    return ''.join(resultado)

nome_correto = "Saphnelo"
nomes_incorretos = ["Sapranelo", "Saranelo", "Zarynelo", "Sarimela", "Sarymeli"]
limiar = 4

for nome_incorreto in nomes_incorretos:
    if correcao_nome(nome_incorreto, nome_correto, limiar):
        print(f"Você quis dizer '{nome_correto}' em vez de '"+ destacar_diferencas(nome_incorreto, nome_correto) +"'?")
