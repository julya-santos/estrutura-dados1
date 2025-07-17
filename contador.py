print ("CONTADOR VOGAIS E CONSOANTES")
frase = input("Digite uma frase: ")
vogais = "aeiou"
cont_vogais = 0
cont_consoantes = 0

for letra in frase.lower():
    if letra.isalpha():
        if letra in vogais:
            cont_vogais += 1
        else:
            cont_consoantes += 1

print(f"Número de vogais: {cont_vogais}")
print(f"Número de consoantes: {cont_consoantes}")
