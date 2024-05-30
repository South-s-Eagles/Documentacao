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

nome_correto = "puta"
palavras = [
    "Anus", "Baba-ovo", "Babaovo", "Babaca", "Bacura", "Bagos", "Baitola", "Bebum", "Besta", "Bicha", "Bisca", "Bixa", "Boazuda", "Boceta", 
    "Boco", "Boiola", "Bolagato", "Boquete", "Bolcat", "Bosseta", "Bosta", "Bostana", "Brecha", "Brexa", "Brioco", "Bronha", "Buca", "Buceta", 
    "Bunda", "Bunduda", "Burra", "Burro", "Busseta", "Cachorra", "Cachorro", "Cadela", "Caga", "Cagado", "Cagao", "Cagona", "Canalha", "Caralho", 
    "Casseta", "Cassete", "Checheca", "Chereca", "Chibumba", "Chibumbo", "Chifruda", "Chifrudo", "Chota", "Chochota", "Chupada", "Chupado", "Clitoris", 
    "Cocaina", "Coco", "Corna", "Corno", "Cornuda", "Cornudo", "Corrupta", "Corrupto", "Cretina", "Cretino", "Cruz-credo", "Cu", "Culhao", "Curalho", 
    "Cuzao", "Cuzuda", "Cuzudo", "Debil", "Debiloide", "Defunto", "Demonio", "Difunto", "Doida", "Doido", "Egua", "Escrota", "Escroto", "Esporrada", 
    "Esporrado", "Esporro", "Estupida", "Estupidez", "Estupido", "Fedida", "Fedido", "Fedor", "Fedorenta", "Feia", "Feio", "Feiosa", "Feioso", "Feioza", 
    "Feiozo", "Felacao", "Fenda", "Foda", "Fodao", "Fode", "Fodida", "Fodido", "Fornica", "Fudendo", "Fudecao", "Fudida", "Fudido", "Furada", "Furado", 
    "Furão", "Furnica", "Furnicar", "Furo", "Furona", "Gaiata", "Gaiato", "Gay", "Gonorrea", "Gonorreia", "Gosma", "Gosmenta", "Gosmento", "Grelinho", 
    "Grelo", "Homo-sexual", "Homossexual", "Homossexual", "Idiota", "Idiotice", "Imbecil", "Iscrota", "Iscroto", "Japa", "Ladra", "Ladrao", "Ladroeira", 
    "Ladrona", "Lalau", "Leprosa", "Leproso", "Lésbica", "Macaca", "Macaco", "Machona", "Machorra", "Manguaca", "Manguaça", "Masturba", "Meleca", "Merda", 
    "Mija", "Mijada", "Mijado", "Mijo", "Mocrea", "Mocreia", "Moleca", "Moleque", "Mondronga", "Mondrongo", "Naba", "Nadega", "Nojeira", "Nojenta", "Nojento", 
    "Nojo", "Olhota", "Otaria", "Ot-ria", "Otario", "Ot-rio", "Paca", "Paspalha", "Paspalhao", "Paspalho", "Pau", "Peia", "Peido", "Pemba", "Pênis", "Pentelha", 
    "Pentelho", "Perereca", "Peru", "Pica", "Picao", "Pilantra", "Piranha", "Piroca", "Piroco", "Piru", "Porra", "Prega", "Prostibulo", "Prost-bulo", "Prostituta", 
    "Prostituto", "Punheta", "Punhetao", "Pus", "Pustula", "Puta", "Puto", "Puxa-saco", "Puxasaco", "Rabao", "Rabo", "Rabuda", "Rabudao", "Rabudo", "Rabudona", 
    "Racha", "Rachada", "Rachadao", "Rachadinha", "Rachadinho", "Rachado", "Ramela", "Remela", "Retardada", "Retardado", "Ridícula", "Rola", "Rolinha", "Rosca", 
    "Sacana", "Safada", "Safado", "Sapatao", "Sifilis", "Siririca", "Tarada", "Tarado", "Testuda", "Tezao", "Tezuda", "Tezudo", "Trocha", "Trolha", "Troucha", 
    "Trouxa", "Troxa", "Vaca", "Vagabunda", "Vagabundo", "Vagina", "Veada", "Veadao", "Veado", "Viada", "Víado", "Viadao", "Xavasca", "Xerereca", "Xexeca", 
    "Xibiu", "Xibumba", "Xota", "Xochota", "Xoxota", "Xana", "Xaninha"
]

limiar = 4

# for nome_incorreto in palavras:
#     if correcao_nome(nome_incorreto, nome_correto, limiar):
#         print(f"Você quis dizer '{nome_correto}' em vez de '"+ destacar_diferencas(nome_incorreto, nome_correto) +"'?")
