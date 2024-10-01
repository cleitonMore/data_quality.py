import pandas as pd  # Importa a biblioteca pandas para manipulação de dados em formato de DataFrame
import os  # Importa a biblioteca os para interagir com o sistema operacional, como limpar a tela
import time  # Importa a biblioteca time para controlar o tempo, usado no efeito de digitação
import matplotlib.pyplot as plt  # Importa a biblioteca matplotlib para gerar gráficos

# Função para exibir a interface inicial com efeito de digitação
def type_out(text):
    """
    Exibe o texto com um efeito de digitação em tempo real.
    """
    for char in text:
        print(char, end='', flush=True)  # Exibe cada caractere um por um, simulando a digitação
        time.sleep(0.05)  # Controla a velocidade do efeito de digitação (0.05 segundos por caractere)
    print()  # Adiciona uma nova linha após exibir o texto

# Função para exibir a interface inicial
def display_welcome_interface():
    """
    Exibe a tela inicial com o nome do sistema e solicita ao usuário se deseja continuar ou sair.
    Retorna True se o usuário optar por continuar e False se optar por sair.
    """
    os.system('cls' if os.name == 'nt' else 'clear')  # Limpa a tela (cls no Windows, clear no Unix)

    # Exibe o cabeçalho da interface inicial
    type_out("====================================")
    type_out("     DATA QUALITY CRIADO POR CLEITON")
    type_out("====================================")
    type_out("\nBem-vindo ao sistema de navegação CSV.")  # Mensagem de boas-vindas
    type_out("Aqui você pode visualizar e filtrar os dados do CSV.")
    type_out("Digite 'h' a qualquer momento para exibir a ajuda.")
    type_out("====================================\n")
    
    # Laço para perguntar ao usuário se ele deseja continuar ou sair
    while True:
        choice = input("Deseja continuar? (s para Sim, q para Sair): ").strip().lower()  # Pede a escolha do usuário
        if choice == 's':  # Se escolher 's', o programa continua
            return True
        elif choice == 'q':  # Se escolher 'q', o programa encerra
            type_out("Saindo do programa...")
            return False
        else:  # Qualquer outra entrada é inválida
            type_out("Entrada inválida! Digite 's' para continuar ou 'q' para sair.\n")

# Classe responsável por navegar e manipular os dados do CSV
class CSVNavigator:
    def __init__(self, dataframe):
        """
        Inicializa o objeto com o DataFrame fornecido.
        """
        self.dataframe = dataframe  # Armazena o DataFrame passado
        self.rows, self.cols = dataframe.shape  # Armazena a quantidade de linhas e colunas
        self.current_row = 0  # Inicializa a posição da linha atual como a primeira
        self.page_size = 10  # Define o tamanho da página como 10 linhas

    # Exibe a lista de comandos disponíveis ao usuário
    def display_help(self):
        """
        Exibe a lista de comandos disponíveis.
        """
        type_out("\nComandos disponíveis:")  # Instruções para o usuário
        type_out("n - Próxima página")
        type_out("p - Página anterior")
        type_out("c - Listar colunas")
        type_out("f - Filtrar por uma coluna (seleção por número)")
        type_out("g - Gerar gráfico de barras (uma coluna)")
        type_out("s - Gerar gráfico de dispersão (duas colunas)")
        type_out("h - Exibir ajuda")
        type_out("q - Sair\n")

    # Exibe as colunas disponíveis no arquivo CSV
    def display_columns(self):
        """
        Exibe todas as colunas do DataFrame com seus respectivos índices.
        """
        type_out("\nColunas disponíveis no arquivo CSV:")
        for idx, col in enumerate(self.dataframe.columns):  # Exibe o índice e o nome de cada coluna
            type_out(f"{idx} - {col}")
        type_out("")  # Nova linha

    # Exibe a página atual de dados
    def display_page(self):
        """
        Exibe uma página de dados do CSV, de acordo com a página atual.
        """
        start_row = self.current_row  # Define a linha inicial da página
        end_row = min(self.current_row + self.page_size, self.rows)  # Define a linha final da página

        type_out(f"\nMostrando linhas {start_row + 1} a {end_row} de {self.rows}:\n")
        print(self.dataframe.iloc[start_row:end_row].to_string(index=False))  # Exibe as linhas atuais do DataFrame
        type_out(f"\nPágina {self.current_row // self.page_size + 1} de {(self.rows // self.page_size) + 1}\n")  # Mostra a página atual

    # Função para filtrar os dados por uma coluna específica
    def filter_by_column(self):
        """
        Permite ao usuário filtrar os dados do CSV por uma coluna específica.
        """
        self.display_columns()  # Exibe as colunas disponíveis
        try:
            col_number = int(input("Digite o número da coluna para filtrar: "))  # Pede ao usuário o número da coluna

            if 0 <= col_number < len(self.dataframe.columns):  # Verifica se o número da coluna é válido
                col_name = self.dataframe.columns[col_number]  # Obtém o nome da coluna
                filter_value = input(f"Digite o valor para filtrar na coluna '{col_name}': ")  # Pede o valor a ser filtrado
                filtered_df = self.dataframe[self.dataframe[col_name] == filter_value]  # Filtra o DataFrame

                if not filtered_df.empty:  # Verifica se o filtro retornou resultados
                    type_out("\nResultado do filtro:")
                    print(filtered_df.to_string(index=False))  # Exibe os dados filtrados
                else:
                    type_out(f"\nNenhum resultado encontrado para o filtro: {filter_value}")  # Se não houver resultados
            else:
                type_out(f"\nNúmero da coluna inválido!")  # Se o número da coluna for inválido
        except ValueError:
            type_out("\nEntrada inválida. Tente novamente.")  # Caso haja um erro na entrada do número da coluna

    # Função para gerar um gráfico de barras de uma coluna
    def generate_bar_chart(self):
        """
        Gera um gráfico de barras para uma coluna específica do DataFrame.
        """
        self.display_columns()  # Exibe as colunas disponíveis
        try:
            col_number = int(input("Digite o número da coluna para gerar gráfico de barras: "))  # Pede o número da coluna

            if 0 <= col_number < len(self.dataframe.columns):  # Verifica se o número da coluna é válido
                col_name = self.dataframe.columns[col_number]  # Obtém o nome da coluna
                self.dataframe[col_name].value_counts().plot(kind='bar', title=f'Gráfico de Barras - {col_name}')  # Cria o gráfico de barras
                plt.xlabel(col_name)
                plt.ylabel('Frequência')
                plt.show()  # Exibe o gráfico
            else:
                type_out(f"\nNúmero da coluna inválido!")  # Se o número da coluna for inválido
        except ValueError:
            type_out("\nEntrada inválida. Tente novamente.")  # Caso haja um erro na entrada do número da coluna

    # Função para gerar um gráfico de dispersão entre duas colunas
    def generate_scatter_plot(self):
        """
        Gera um gráfico de dispersão para duas colunas numéricas.
        """
        self.display_columns()  # Exibe as colunas disponíveis
        try:
            x_col_number = int(input("Digite o número da primeira coluna (eixo X): "))  # Pede a coluna para o eixo X
            y_col_number = int(input("Digite o número da segunda coluna (eixo Y): "))  # Pede a coluna para o eixo Y

            if 0 <= x_col_number < len(self.dataframe.columns) and 0 <= y_col_number < len(self.dataframe.columns):  # Verifica se os números das colunas são válidos
                x_col_name = self.dataframe.columns[x_col_number]  # Obtém o nome da coluna do eixo X
                y_col_name = self.dataframe.columns[y_col_number]  # Obtém o nome da coluna do eixo Y
                plt.scatter(self.dataframe[x_col_name], self.dataframe[y_col_name])  # Cria o gráfico de dispersão
                plt.title(f'Gráfico de Dispersão - {x_col_name} vs {y_col_name}')
                plt.xlabel(x_col_name)
                plt.ylabel(y_col_name)
                plt.show()  # Exibe o gráfico
            else:
                type_out(f"\nNúmero de coluna inválido!")  # Se os números das colunas forem inválidos
        except ValueError:
            type_out("\nEntrada inválida. Tente novamente.")  # Caso haja um erro na entrada dos números das colunas

    # Função principal que executa a navegação
    def run(self):
        """
        Executa a navegação no CSV, com a capacidade de mudar páginas, listar colunas, aplicar filtros e gerar gráficos.
        """
        self.display_help()  # Exibe a ajuda com os comandos
        self.display_page()  # Exibe a primeira página de dados

        while True:
            command = input("Digite um comando: ").strip().lower()  # Pede o comando do usuário

            if command == 'n':  # Próxima página
                if self.current_row + self.page_size < self.rows:  # Verifica se há mais páginas
                    self.current_row += self.page_size
                else:
                    type_out("\nVocê já está na última página!")  # Informa se o usuário está na última página
                self.display_page()  # Exibe a nova página

            elif command == 'p':  # Página anterior
                if self.current_row - self.page_size >= 0:  # Verifica se há páginas anteriores
                    self.current_row -= self.page_size
                else:
                    type_out("\nVocê já está na primeira página!")  # Informa se o usuário está na primeira página
                self.display_page()  # Exibe a nova página

            elif command == 'c':  # Listar colunas
                self.display_columns()  # Exibe as colunas disponíveis

            elif command == 'f':  # Filtrar por coluna
                self.filter_by_column()  # Aplica o filtro por coluna

            elif command == 'g':  # Gerar gráfico de barras
                self.generate_bar_chart()  # Gera um gráfico de barras

            elif command == 's':  # Gerar gráfico de dispersão
                self.generate_scatter_plot()  # Gera um gráfico de dispersão

            elif command == 'h':  # Exibir ajuda
                self.display_help()  # Exibe a ajuda novamente

            elif command == 'q':  # Sair
                type_out("Saindo do programa...")  # Informa que o programa está encerrando
                break  # Sai do loop

            else:
                type_out("Comando inválido! Digite 'h' para ajuda.")  # Mensagem de comando inválido

# Função principal do programa
def main():
    """
    Função principal que controla o fluxo do programa.
    """
    if display_welcome_interface():  # Exibe a interface inicial e pergunta se o usuário deseja continuar
        csv_path = input("Caminho do arquivo CSV: ").strip()  # Pede o caminho do arquivo CSV

        try:
            df = pd.read_csv(csv_path)  # Tenta ler o arquivo CSV e criar o DataFrame
            navigator = CSVNavigator(df)  # Cria uma instância da classe CSVNavigator
            navigator.run()  # Executa a navegação
        except FileNotFoundError:
            type_out(f"Arquivo {csv_path} não encontrado!")  # Erro se o arquivo não for encontrado
        except pd.errors.EmptyDataError:
            type_out("O arquivo CSV está vazio.")  # Erro se o arquivo estiver vazio
        except pd.errors.ParserError:
            type_out("Ocorreu um erro ao processar o arquivo CSV. Verifique o formato.")  # Erro no formato do CSV
        except Exception as e:
            type_out(f"Ocorreu um erro ao carregar o CSV: {str(e)}")  # Qualquer outro erro

    input("Pressione Enter para sair...")  # Espera o usuário pressionar Enter para encerrar

# Executa o programa apenas se este arquivo for executado diretamente
if __name__ == "__main__":
    main()  # Chama a função principal do programa
