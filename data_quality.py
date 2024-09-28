import pandas as pd
import plotly.express as px

class DataQualityReport:
    def __init__(self, dataframe):
        self.dataframe = dataframe
        
    def generate_report(self):
        report = {}
        report['missing_values'] = self.dataframe.isnull().sum()
        report['unique_values'] = self.dataframe.nunique()
        
        # Descriptive statistics for numerical columns
        numeric_desc = self.dataframe.describe()
        report['numerical_stats'] = numeric_desc
        
        # Value counts for categorical columns
        categorical_cols = self.dataframe.select_dtypes(include=['object']).columns
        report['categorical_counts'] = {col: self.dataframe[col].value_counts() for col in categorical_cols}
        
        # Generate plots
        self.plot_distributions()
        
        return report

    def plot_distributions(self):
        # Distribution of numerical columns
        numeric_cols = self.dataframe.select_dtypes(include=['number']).columns
        
        for col in numeric_cols:
            fig = px.histogram(self.dataframe, x=col, title=f'Distribution of {col}', nbins=30)
            fig.update_layout(xaxis_title=col, yaxis_title='Frequency')
            fig.show()

        # Distribution of categorical columns
        categorical_cols = self.dataframe.select_dtypes(include=['object']).columns
        
        for col in categorical_cols:
            fig = px.bar(self.dataframe[col].value_counts().reset_index(), 
                         x='index', y=col, title=f'Distribution of {col}')
            fig.update_layout(xaxis_title=col, yaxis_title='Count')
            fig.show()

# Carregar o dataset
df = pd.read_csv('C:/Users/cleiton/Desktop/houses_to_rent_v2_corrigido.csv')  # Substitua pelo caminho do seu arquivo CSV

# Gerar o relatório de qualidade dos dados
report = DataQualityReport(df).generate_report()
