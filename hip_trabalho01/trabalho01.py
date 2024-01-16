import xml.etree.ElementTree as ET
import time

tree = ET.parse('verbetesWikipedia.xml')
root = tree.getroot()

paginas = root.findall('.//page')

#deixar as palavras minusculas
def minuscula(term):
    term=term.lower()
    return term

#remove o s de palavras com plural
def deleta_plural(term):
    if term.endswith('s'):
        term = term[:-1]
    return term

#guarda as palavras do titulo e texto, com seus indices
def indexador():
    lista_separa={}
    for page in paginas: 
        Id = page.find('id').text
        titulo = page.find('title').text
        texto = page.find('text').text
        for term in minuscula(titulo).split(' '):
            term=deleta_plural(term)
            if len(term) >=4:
                if term in lista_separa:
                        lista_separa[term]['titulo'].append(Id)
                else:
                    lista_separa[term]={"titulo" : [Id], "texto" : []}
        for term in minuscula(texto).split(' '):
            term=deleta_plural(term)
            if len(term) >=4:
                if term in lista_separa:
                        lista_separa[term]['texto'].append(Id)
                else:
                    lista_separa[term]={"titulo" : [], "texto" : [Id]}
    return lista_separa

#busca a quantidade de vezes que as palavras aparecem na lista
def pesquisar(term,lista_separa):
    resultado = {}
    if term in lista_separa:
        for id_texto in lista_separa[term]['titulo']:
            if id_texto in resultado:
                resultado[id_texto]['titulo'] += 1
            else:
                resultado[id_texto] = {'titulo': 1, 'texto': 0}
        for id_texto in lista_separa[term]['texto']:
            if id_texto in resultado:
                resultado[id_texto]['texto'] += 1
            else:
                resultado[id_texto] = {'titulo': 0, 'texto': 1}
    return resultado

#ordena os valores dando prioridade as palavras que aparecem no titulo e texto, dobra os valores do texto 
def ordenador(lista_separa):
    resultado = {}
    for id_texto, ocorrencias in lista_separa.items():
        if ocorrencias['titulo'] and ocorrencias['texto']:
            if id_texto in resultado:
                resultado[id_texto]['titulo'] = ocorrencias['titulo']
                resultado[id_texto]['textobase'] = ocorrencias['texto']
                resultado[id_texto]['texto'] = ocorrencias['texto'] * 2
            else:
                resultado[id_texto] = {'titulo': ocorrencias['titulo'], 'texto': ocorrencias['texto'] * 2, 'textobase':ocorrencias['texto']}
        else:
            resultado[id_texto] = {'titulo': ocorrencias['titulo'], 'texto': ocorrencias['texto'],'textobase': ocorrencias['texto']}
    ordenado = sorted(resultado.items(), key=lambda x: x[1]['texto'], reverse=True)
    return ordenado


while True:
    termo = input("Digite uma palavra:\n").lower()

    if termo == "0":
        break
    
    inicio = time.time()
    pesquisa=pesquisar(termo,indexador())
    ord=ordenador(pesquisa)
    final = time.time()
    tempo_decorrido = final - inicio

    for i in ord:
        print(f"id Pagina = {i[0]} | Relevancia: {i[1]['texto']} | Ocorrencia no titulo: {i[1]['titulo']} | Ocorrencia no texto: {i[1]['textobase']}")

    print(f"Tempo de execução: {tempo_decorrido:.2f} segundos")

