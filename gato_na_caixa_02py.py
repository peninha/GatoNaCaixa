import random
import matplotlib.pyplot as plt

def cat_move(catState, boxes=5):
    """
    Função que determina o movimento do gato entre as caixas.

    Parâmetros:
    - catState (int): Estado atual do gato (posição na caixa).
    - boxes (int): Número total de caixas.

    Retorna:
    - int: Nova posição do gato.
    """
    if catState == 0:
        return random.randint(1, boxes)
    if catState == 1:
        return 2
    if catState == boxes:
        return catState - 1
    return catState + random.randint(-1, 0) * 2 + 1

def open_box(box, catState, boxes=5):
    """
    Função que verifica se a caixa aberta contém o gato.

    Parâmetros:
    - box (int): Número da caixa a ser aberta.
    - catState (int): Posição atual do gato.
    - boxes (int): Número total de caixas.

    Retorna:
    - bool: True se o gato estiver na caixa aberta, False caso contrário.
    """
    return catState == box

def main():
    # Configurações iniciais
    random.seed(42)  # Define a semente para reprodutibilidade
    boxes = 5        # Número de caixas
    runs = 100000   # Número de execuções (runs) para a simulação
    strategy = [2, 3, 4, 4, 3, 2]  # Sequência de caixas a serem abertas

    try_counts = []  # Lista para armazenar o número de tentativas por run

    for run in range(runs):
        catState = 0     # Inicializa a posição do gato
        found = False    # Indicador de que o gato ainda não foi encontrado
        try_count = 0    # Conta o número de tentativas na run atual

        while not found:
            catState = cat_move(catState, boxes)  # Move o gato
            box_to_open = strategy[try_count % len(strategy)]  # Seleciona a caixa a ser aberta seguindo a estratégia
            found = open_box(box_to_open, catState, boxes)  # Verifica se o gato está na caixa aberta
            try_count += 1  # Incrementa o contador de tentativas

            # Previne loops infinitos caso algo dê errado
            if try_count > 1000:
                print(f"Run {run + 1}: Número de tentativas excedeu 1000. Encerrando a run.")
                break

        try_counts.append(try_count)  # Registra o número de tentativas para esta run

    # Exibição dos resultados
    print(f"Simulação concluída após {runs} runs.")
    print(f"Média de tentativas: {sum(try_counts) / len(try_counts):.2f}")
    print(f"Máximo de tentativas: {max(try_counts)}")
    print(f"Mínimo de tentativas: {min(try_counts)}")

    # Plotagem do histograma da distribuição de tentativas
    plt.figure(figsize=(10, 6))
    plt.hist(try_counts, bins=range(1, max(try_counts) + 2), density=True, edgecolor='black', alpha=0.7)
    plt.title(f'Distribuição de Probabilidade das Tentativas para Encontrar o Gato\nSimulações: {runs}')

    plt.annotate(
        f'Estratégia: {"-".join(map(str, strategy))}',
        xy=(0.25, 0.95),
        xycoords='axes fraction',
        fontsize=10,
        ha='right',
        va='top',
        bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.5)
    )
    plt.xlabel('Número de Tentativas')
    plt.ylabel('Probabilidade')
    plt.grid(axis='y', alpha=0.75)
    plt.xticks(range(1, max(try_counts) + 1))
    plt.show()

if __name__ == '__main__':
    main()
