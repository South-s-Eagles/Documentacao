import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time

NOME_USUARIO = ""
SENHA_USUARIO = ""
QUERY_BUSCA = "buceta"
PALAVRAO_PATH = "./palavrao-list.txt"


def iniciar_driver():
    service = Service()
    options = webdriver.FirefoxOptions()
    driver = webdriver.Firefox(service=service, options=options)
    return driver


def login_twitter(driver, nome_usuario, senha_usuario):
    driver.get("https://twitter.com/")
    time.sleep(2)
    login_button = driver.find_element(By.CSS_SELECTOR, "a[href='/login']")
    login_button.click()
    time.sleep(3)

    usuario_input = driver.find_element(By.NAME, "text")
    usuario_input.send_keys(nome_usuario)
    usuario_input.send_keys(Keys.ENTER)
    time.sleep(3)

    senha_input = driver.find_element(By.NAME, "password")
    senha_input.send_keys(senha_usuario)
    senha_input.send_keys(Keys.ENTER)
    time.sleep(3)


def buscar_tweets(driver, query):
    campo_pesquisa = driver.find_element(By.CSS_SELECTOR, "div.css-146c3p1 input")
    campo_pesquisa.send_keys(query)
    campo_pesquisa.send_keys(Keys.ENTER)
    time.sleep(5)
    return driver.find_elements(By.TAG_NAME, "article")


def extrair_tweet_e_sentimento(tweet, analyzer) -> dict | None:
    try:
        sentimento = analyzer.polarity_scores(tweet)
        return {"texto": tweet, "sentimento": sentimento}
    except Exception as e:
        print(f"Erro ao extrair tweet: {e}")
        return None


def calculate_levenshtein(str1: str, str2: str) -> int:
    if len(str1) > len(str2):
        str1, str2 = str2, str1

    distances = range(len(str1) + 1)
    for i2, c2 in enumerate(str2):
        distances_ = [i2 + 1]
        for i1, c1 in enumerate(str1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(
                    1 + min((distances[i1], distances[i1 + 1], distances_[-1]))
                )
        distances = distances_
    return distances[-1]


def is_palavrao(palavra: str, palavroes: list[str]) -> bool:
    menor_distancia = float("inf")
    for palavrao in palavroes:
        distancia = calculate_levenshtein(palavra.lower(), palavrao.lower())
        if distancia < menor_distancia:
            menor_distancia = distancia
    return True if menor_distancia < 1 else False


def extrai_palavras(tweet: str) -> list[str]:
    return tweet.split()


def remove_palavras_profanas(tweet: str, palavroes: list[str]) -> str:
    palavras = extrai_palavras(tweet)
    for i in range(len(palavras)):
        if is_palavrao(palavras[i], palavroes):
            palavras[i] = "*" * len(palavras[i])
    return " ".join(palavras)


def carregar_lista_palavroes(file_path: str) -> list[str]:
    with open(file_path, "r") as file:
        palavroes = file.read().split()
    return palavroes


def main():
    driver = iniciar_driver()
    analyzer = SentimentIntensityAnalyzer()

    try:
        login_twitter(driver, NOME_USUARIO, SENHA_USUARIO)
        tweets = buscar_tweets(driver, QUERY_BUSCA)

        lista_tweets = []
        for tweet in tweets:
            content = tweet.find_element(
                By.CSS_SELECTOR, "div[data-testid='tweetText']"
            ).text
            res = extrair_tweet_e_sentimento(content, analyzer)

            if res is not None:
                res["texto"] = remove_palavras_profanas(
                    res["texto"], carregar_lista_palavroes(PALAVRAO_PATH)
                )
                lista_tweets.append(res)
                print(res)

        df_tweets = pd.DataFrame(lista_tweets)
        df_tweets.to_csv("tweets_estresse.csv", index=False)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
