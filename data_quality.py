# Importa a biblioteca pandas para manipulação de dados em arquivos CSV
import pandas as pd

# Importa a biblioteca os para limpar a tela no terminal
import os

# Função para exibir a interface inicial
def display_welcome_interface():
    """
    Exibe a tela inicial com o nome do sistema e solicita ao usuário se deseja continuar ou sair.
    Retorna True se o usuário optar por continuar e False se optar por sair.
    """
    # Limpa a tela, utilizando 'cls' no Windows ou 'clear' em outros sistemas
    os.system('cls' if os.name == 'nt' else 'clear')

    # Exibe o cabeçalho da interface inicial
    print("====================================")
    print("     DATA QUALITY CRIADO POR CLEITON")
    print("====================================")
    print("\nBem-vindo ao sistema de navegação CSV.")
    print("Aqui você pode visualizar e filtrar os dados do CSV.")
    print("Digite 'h' a qualquer momento para exibir a ajuda.")
    print("====================================\n")
    
    # Laço para perguntar ao usuário se ele deseja continuar ou sair
    while True:
        choice = input("Deseja continuar? (s para Sim, q para Sair): ").strip().lower()  # Entrada do usuário
        if choice == 's':
            return True  # Continua o programa
        elif choice == 'q':
            print("Saindo do programa...")
            return False  # Encerra o programa
        else:
            # Mensagem de erro se o usuário digitar um valor inválido
            print("Entrada inválida! Digite 's' para continuar ou 'q' para sair.\n")

# Classe responsável por navegar e manipular os dados do CSV
class CSVNavigator:
    def __init__(self, dataframe):
        """
        Inicializa o objeto com o DataFrame fornecido.
        """
        self.dataframe = dataframe  # Armazena o DataFrame
        self.rows, self.cols = dataframe.shape  # Obtém o número de linhas e colunas do DataFrame
        self.current_row = 0  # Define a linha inicial para exibição
        self.page_size = 10  # Define o número de linhas a serem exibidas por página

    # Exibe a lista de comandos disponíveis ao usuário
    def display_help(self):
        """
        Exibe a lista de comandos disponíveis.
        """
        print("\nComandos disponíveis:")
        print("n - Próxima página")
        print("p - Página anterior")
        print("c - Listar colunas")
        print("f - Filtrar por uma coluna (seleção por número)")
        print("h - Exibir ajuda")
        print("q - Sair\n")

    # Exibe as colunas disponíveis no arquivo CSV
    def display_columns(self):
        """
        Exibe todas as colunas do DataFrame com seus respectivos índices.
        """
        print("\nColunas disponíveis no arquivo CSV:")
        for idx, col in enumerate(self.dataframe.columns):  # Itera sobre as colunas
            print(f"{idx} - {col}")  # Exibe o índice e o nome da coluna
        print("")

    # Exibe a página atual de dados
    def display_page(self):
        """
        Exibe uma página de dados do CSV, de acordo com a página atual.
        """
        start_row = self.current_row  # Define a linha inicial para exibição
        end_row = min(self.current_row + self.page_size, self.rows)  # Define a linha final

        # Exibe as linhas selecionadas e informações sobre a página
        print(f"\nMostrando linhas {start_row + 1} a {end_row} de {self.rows}:\n")
        print(self.dataframe.iloc[start_row:end_row].to_string(index=False))  # Exibe as linhas sem os índices
        print(f"\nPágina {self.current_row // self.page_size + 1} de {(self.rows // self.page_size) + 1}\n")

    # Função para filtrar os dados por uma coluna específica
    def filter_by_column(self):
        """
        Permite ao usuário filtrar os dados do CSV por uma coluna específica.
        """
        self.display_columns()  # Exibe as colunas disponíveis
        try:
            col_number = int(input("Digite o número da coluna para filtrar: "))  # Solicita o número da coluna

            # Verifica se o número da coluna é válido
            if 0 <= col_number < len(self.dataframe.columns):
                col_name = self.dataframe.columns[col_number]  # Obtém o nome da coluna
                filter_value = input(f"Digite o valor para filtrar na coluna '{col_name}': ")  # Valor para filtrar
                filtered_df = self.dataframe[self.dataframe[col_name] == filter_value]  # Aplica o filtro

                # Verifica se há resultados para o filtro
                if not filtered_df.empty:
                    print("\nResultado do filtro:")
                    print(filtered_df.to_string(index=False))  # Exibe os resultados sem os índices
                else:
                    print(f"\nNenhum resultado encontrado para o filtro: {filter_value}")
            else:
                print(f"\nNúmero da coluna inválido!")  # Se o número da coluna não for válido
        except ValueError:
            print("\nEntrada inválida. Tente novamente.")  # Se o usuário digitar algo inválido

    # Função principal que executa a navegação
    def run(self):
        """
        Executa a navegação no CSV, com a capacidade de mudar páginas, listar colunas e aplicar filtros.
        """
        self.display_help()  # Exibe a ajuda com os comandos disponíveis
        self.display_page()  # Exibe a primeira página de dados

        # Laço principal para receber comandos do usuário
        while True:
            command = input("Digite um comando: ").strip().lower()  # Comando do usuário

            if command == 'n':  # Próxima página
                if self.current_row + self.page_size < self.rows:
                    self.current_row += self.page_size
                else:
                    print("\nVocê já está na última página!")
                self.display_page()  # Exibe a página atualizada

            elif command == 'p':  # Página anterior
                if self.current_row - self.page_size >= 0:
                    self.current_row -= self.page_size
                else:
                    print("\nVocê já está na primeira página!")
                self.display_page()  # Exibe a página atualizada

            elif command == 'c':  # Listar colunas
                self.display_columns()

            elif command == 'f':  # Filtrar por coluna
                self.filter_by_column()

            elif command == 'h':  # Exibir ajuda
                self.display_help()

            elif command == 'q':  # Sair
                print("Saindo do programa...")
                break

            else:
                print("Comando inválido! Digite 'h' para ajuda.")  # Se o comando for inválido

# Função principal do programa
def main():
    """
    Função principal que controla o fluxo do programa.
    """
    # Exibe a interface inicial
    if display_welcome_interface():
        # Solicita o caminho do arquivo CSV
        csv_path = input("Caminho do arquivo CSV: ").strip()

        try:
            # Tenta carregar o arquivo CSV
            df = pd.read_csv(csv_path)
            navigator = CSVNavigator(df)  # Instancia a classe de navegação com o DataFrame
            navigator.run()  # Inicia a navegação
        except FileNotFoundError:
            print(f"Arquivo {csv_path} não encontrado!")  # Arquivo não encontrado
        except pd.errors.EmptyDataError:
            print("O arquivo está vazio.")  # Arquivo CSV vazio
        except pd.errors.ParserError:
            print("Ocorreu um erro ao processar o arquivo CSV. Verifique o formato.")  # Erro ao ler o arquivo
        except Exception as e:
            print(f"Ocorreu um erro ao carregar o CSV: {str(e)}")  # Erro geral

# Executa o programa apenas se este arquivo for executado diretamente
if __name__ == "__main__":
    main()

