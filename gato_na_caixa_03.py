import random
import matplotlib.pyplot as plt
import numpy as np

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
    #random.seed(42)  # Define a semente para reprodutibilidade
    boxes = 5        # Número de caixas
    runs = 100000    # Número de execuções (runs) para a simulação

    # Definição das diferentes estratégias a serem comparadas
    strategies = [
        [2,3,4,4,3,2],
        [4,4,2,2],
        [4,2,3],
    ]

    # Geração automática das legendas a partir das listas de estratégias
    strategy_labels = [f"Estratégia: {'-'.join(map(str, strategy))}" for strategy in strategies]

    # Inicialização do dicionário para armazenar tentativas por estratégia
    results = {label: [] for label in strategy_labels}

    # Definição do limite máximo de tentativas a serem exibidas nos gráficos
    max_display_attempts = 15

    # Loop de Simulação para Cada Estratégia
    for label, strategy in zip(strategy_labels, strategies):
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
                    print(f"{label} - Run {run + 1}: Número de tentativas excedeu 1000. Encerrando a run.")
                    break

            results[label].append(try_count)  # Registra o número de tentativas para esta run

    # Exibição dos resultados
    for label in strategy_labels:
        try_counts = results[label]
        median = np.median(try_counts)
        print(f"{label}:")
        print(f"  Média de tentativas: {np.mean(try_counts):.2f}")
        print(f"  Mediana de tentativas: {median:.2f}")
        print(f"  Máximo de tentativas: {np.max(try_counts)}")
        print(f"  Mínimo de tentativas: {np.min(try_counts)}\n")

    # Plotagem do histograma da distribuição de tentativas para todas as estratégias (lado a lado)
    max_attempts_display = max_display_attempts

    # Definir os bins para todos os histogramas até o limite
    bins = np.arange(1, max_attempts_display + 2) - 0.5  # Ajuste para centralizar as barras

    # Definir a largura das barras
    bar_width = 0.2

    # Definir as posições das barras para cada estratégia
    positions = [np.arange(1, max_attempts_display + 1) + i * bar_width for i in range(len(strategies))]

    plt.figure(figsize=(12, 8))

    for idx, (label, strategy) in enumerate(zip(strategy_labels, strategies)):
        # Filtrar tentativas que excedem o limite e agrupá-las em max_attempts_display
        filtered_counts = [min(count, max_attempts_display) for count in results[label]]
        counts, _ = np.histogram(filtered_counts, bins=bins, density=True)
        plt.bar(positions[idx], counts, width=bar_width, edgecolor='black', label=label)
    
    
    # Adicionar uma anotação indicando o limite de tentativas
    plt.annotate(
        f"Mostrando até {max_display_attempts} tentativas",
        xy=(.98, 0.70),
        xycoords='axes fraction',
        fontsize=10,
        ha='right',
        va='bottom',
        bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.5)
    )
    
    # Ajustar os ticks do eixo x para o centro das barras
    plt.xticks(np.arange(1, max_attempts_display + 1), range(1, max_attempts_display + 1))
    plt.xlabel('Número de Tentativas')
    plt.ylabel('Probabilidade')
    plt.title('Distribuição de Probabilidade das Tentativas para Encontrar o Gato')
    plt.legend()
    plt.grid(axis='y', alpha=0.75)
    plt.xlim(0.5, max_attempts_display + 0.5)  # Limitar o eixo x
    plt.show()

    # Plotagem do gráfico de porcentagem acumulada para todas as estratégias (CDF)
    plt.figure(figsize=(12, 8))

    # Definir estilos de linha diferentes para cada estratégia
    line_styles = ['-', '--', '-.']  # Adicione mais estilos se houver mais estratégias

    for idx, (label, strategy) in enumerate(zip(strategy_labels, strategies)):
        try_counts = results[label]
        sorted_counts = np.sort(try_counts)
        # Filtrar apenas até o limite máximo para o CDF
        sorted_counts = sorted_counts[sorted_counts <= max_display_attempts]
        if len(sorted_counts) == 0:
            # Se todas as tentativas excederem o limite, pular
            continue
        cdf = np.arange(1, len(sorted_counts) + 1) / len(sorted_counts)
        plt.plot(
            sorted_counts,
            cdf,
            label=label,
            linewidth=2,
            linestyle=line_styles[idx % len(line_styles)],
            marker='o',
            markersize=3
        )

    # Adicionar uma anotação indicando o limite de tentativas
    plt.annotate(
        f"Mostrando até {max_display_attempts} tentativas",
        xy=(0.95, 0.05),
        xycoords='axes fraction',
        fontsize=10,
        ha='right',
        va='bottom',
        bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.5)
    )

    plt.title('Porcentagem Acumulada das Tentativas para Encontrar o Gato')
    plt.xlabel('Número de Tentativas')
    plt.ylabel('Probabilidade Acumulada')
    plt.legend()
    plt.grid(True)
    plt.xlim(1, max_display_attempts)  # Limitar o eixo x
    plt.show()
    
    plt.figure(figsize=(12, 8))
    data = [results[label] for label in strategy_labels]
    plt.boxplot(data, labels=strategy_labels, patch_artist=True)
    plt.xlabel('Estratégias')
    plt.ylabel('Número de Tentativas')
    plt.title('Box Plot das Tentativas para Encontrar o Gato por Estratégia')
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    main()
