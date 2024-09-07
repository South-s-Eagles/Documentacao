#GRUPO 05

#Guilherme Coimbra
#Gustavo Nogueira
#Helder Rodrigues
#Ivan Freire
#Leonardo Aguiar


import pdfplumber
import re
import openpyxl
import random
from gender_guesser_br import Genero
from wonderwords import RandomWord
from cryptography.fernet import Fernet
from names_generator import generate_name
from DadosAbertosBrasil import ibge

r = RandomWord()
key = Fernet.generate_key()
fernet = Fernet(key)

def extrair_dados(text):
    cpf_pattern = re.compile(r'CPF:\s?(\d{11}|\d{9})')
    rg_pattern = re.compile(r'RG:\s?([\d\.-]+[Xx]?)')
    nome_pattern = re.compile(r'(?:CPF:\s?\d+\s+RG:\s?[\d\.-Xx]+)?\s+(AT\d+\s+-\s+SALA\s+\d+\s+)(.*)')

    cpfs = cpf_pattern.findall(text)
    rgs = rg_pattern.findall(text)
    nomes = [match[1] for match in nome_pattern.findall(text)]

    return list(zip(nomes, cpfs, rgs))

def enriquecer_dados(dados):
    dados_enriquecidos = []

    for nome, cpf, rg in dados:
        random_nb = random.randint(0, 26)

        estados = ibge.localidades(nivel="estados")
        uf = estados['sigla'][random_nb]
        estado = estados['nome'][random_nb]

        idade = random.randint(18, 80)

        # genero = Genero(nome=nome, uf=uf)

        endereco = f"Rua {r.word()} {random.randint(100, 999)}, Cidade {r.word()}, Estado {estado}, {random.randint(10000, 99999)}-{random.randint(100, 999)}"

        login = generate_name()

        senha = r.word()
        encSenha = fernet.encrypt(r.word().encode())

        dados_enriquecidos.append((nome, cpf, rg, idade, endereco, login, senha))

    return dados_enriquecidos

def salvar_em_excel(dados, caminho):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Dados dos Clientes Health Eagles"

    ws.append(["Nome", "CPF", "RG", "Idade", "Endereço", "Login", "Senha"])

    for nome, cpf, rg, idade, endereco, login, senha in dados:
        ws.append([nome, cpf, rg, idade, endereco, login, senha])

    wb.save(caminho)

def anonimizar_dados(dados):
    dados_anonimizados = []

    for nome, cpf, rg, idade, endereco, login, senha in dados:
        cpf_anonimizado = f"***.***.***-{cpf[-3:]}"
        rg_anonimizado = f"***.***.{rg[-2:]}"

        nome_anonimizado = ''.join([f"{n[0]}." for n in nome.split()])

        encSenha = fernet.encrypt(senha.encode())

        dados_anonimizados.append((nome_anonimizado, cpf_anonimizado, rg_anonimizado, idade, endereco, login, encSenha))

    return dados_anonimizados

pdf_path = "11971_profmat_exame_nacional_de_acesso_listagem_de_candiatos_por_sala.pdf"

with pdfplumber.open(pdf_path) as pdf:
    full_text = ""
    for page in pdf.pages:
        full_text += page.extract_text()

    dados_extraidos = extrair_dados(full_text)

    dados_enriquecidos = enriquecer_dados(dados_extraidos)

    dados_anonimizados = anonimizar_dados(dados_enriquecidos)

    caminho_excel = "dados_clientes_anonimizados.xlsx"
    salvar_em_excel(dados_anonimizados, caminho_excel)

    print("Pronto.")
