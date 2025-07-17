# Verificador de Palíndromo

# Entrada do usuário
frase = input("Digite uma palavra ou frase: ")

frase_0 = ''
for letra in frase.lower():
    if letra.isalnum():  
        frase_0 += letra

# Verifica se a frase é igual ao seu inverso
if frase_0 == frase_0[::-1]:
    print("A frase é um palíndromo.")
else:
    print("A frase não é um palíndromo.")
