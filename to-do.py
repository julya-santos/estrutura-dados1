tarefas = []

while True:
    print("\n TO-DO LIST")
    print("1. Adicionar nova tarefa")
    print("2. Visualizar tarefas")
    print("3. Remover tarefa")
    print("4. Sair")
    escolha = input("Escolha uma opção (1-4): ")

    if escolha == "1":
        nova = input("Digite a nova tarefa: ")
        tarefas.append(nova)
        print("Tarefa adicionada!")

    elif escolha == "2":
        if tarefas:
            print("\nTarefas:")
            for i, t in enumerate(tarefas):
                print(f"{i+1}. {t}")
        else:
            print("Nenhuma tarefa na lista.")

    elif escolha == "3":
        if tarefas:
            print("\nTarefas:")
            for i, t in enumerate(tarefas):
                print(f"{i+1}. {t}")
            try:
                rem = int(input("Digite o número da tarefa a remover: "))
                if 1 <= rem <= len(tarefas):
                    removida = tarefas.pop(rem-1)
                    print(f"Tarefa '{removida}' removida.")
                else:
                    print("Índice inválido.")
            except ValueError:
                print("Entrada inválida. Use apenas números.")
        else:
            print("Lista de tarefas vazia.")

    elif escolha == "4":
        print("Saindo...")
        break

    else:
        print("Opção inválida. Tente novamente.")
