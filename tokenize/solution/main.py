"""
   NÃO MODIFIQUE ESTE ARQUIVO - autor MAC0122

   Este arquivo contem o programa principal do projeto.
"""

# tk.tokeniza(),
import esqueleto_tokeniza as tk

# categorias e dicionario "categoria: decrição"
import operadores as op

import levenshtein as lv

PROMPT = "expressão >>> "
QUIT = ""


# ------------------------------------------------------------
def main():
    """None -> None

    Programa que lê do teclado uma expressão aritmética
    e imprime cada item léxico na expressão.

    Exemplos:


    """
    print("Entre como uma expressão ou tecle apenas ENTER para encerrar.")
    expressao = input(PROMPT)
    while expressao != QUIT:
        lista_tokens = tk.tokeniza(expressao)
        for token in lista_tokens:
            # pegue item e tipo
            item, tipo = token

            for palavra in lv.palavras:
                if lv.levenshtein(item, palavra) <= 1:
                    item = "****"
                    break

            # cri string com a descriçao
            if tipo in [tk.OPERADOR, tk.PARENTESES]:
                descricao = "'%s' : %s" % (item, op.DESCRICAO[item])
            elif tipo == tk.VARIAVEL:
                if item == "****":
                    descricao = "'%s' : nome de variável (palavrão)" % item
                else:
                    descricao = "'%s' : nome de variável" % item
            elif tipo == tk.NUMERO:
                descricao = "%s : constante float" % str(item)
            else:
                descricao = "'%s' : categoria desconhecida" % item

            # imprima a descriçao
            #TODO implementar levenshtein antes de imprimir, 
            # para validar presença de palavrões
            print(descricao)

        # leia próxima expressão
        expressao = input(PROMPT)


# -------------------------------------------
# início da execução do programa
main()
