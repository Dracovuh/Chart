import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns

from constants import factors

# Set seaborn style
sns.set(style="whitegrid", palette="husl")

def load_data(file_name):
    try: 
        # Load the CSV file
        data = pd.read_csv(f'./data/data-tokens-v2/Target10-50/Percent/{file_name}.csv')
        return data
    except Exception as e:
        raise Exception(f"Error loading data: {e}")

def analyze_null_values(data):
    # Analyze null values in the DataFrame
    total = data.shape[0]
    null_columns = data.columns[data.isnull().any()]

    print("Columns with null values:")
    columns = []
    for col in null_columns:
        num = data[col].isnull().sum()
        columns.append([col, num, round(num*100/total, 2)])

    print([total, columns])

def divide_data_by_token(data):
    # Divide DataFrame into multiple DataFrames for each token
    grouped_tokens = data.groupby('TokenAddress')
    token_dataframes = [group.copy() for _, group in grouped_tokens]
    return token_dataframes

def filter_tokens_by_record_count(token_dataframes, min_records=12):
    # Filter token DataFrames by record count
    filtered_dataframes = []
    for df in token_dataframes:
        if len(df) >= min_records:
            filtered_dataframes.append(df)
    return filtered_dataframes

def save_facet_grid_scatterplot(data, directory='facet_scatterplots'):
    # Create directory if it doesn't exist
    # os.makedirs(directory, exist_ok=True)

    # # Create a FacetGrid scatterplot for each factor
    # for factor in factors:
    #     plt.figure(figsize=(12, 8))
    #     g = sns.FacetGrid(data, col=factor, col_wrap=4, height=4, aspect=1, sharey=False)
    #     g.map_dataframe(sns.scatterplot, x='TokenAddress', y=factor)
    #     g.set_titles(col_template="{col_name}")
    #     g.set_axis_labels("Token Address", factor)
    #     plt.savefig(os.path.join(directory, f'{factor}_facet_scatterplot.png'))
    #     plt.close()

    sns.scatterplot(x = 'Vol24h-Marketcap', y = 'SMQuantityHold(Holder)', data = )

def main():
    try:
        # Load the CSV file
        data_file_name = 'H1'
        data = load_data(data_file_name)

        # Divide DataFrame into multiple DataFrames for each token
        token_dataframes = divide_data_by_token(data)

        # Filter tokens by record count
        filtered_dataframes = filter_tokens_by_record_count(token_dataframes)

        # Save Facet Grid scatterplot for each factor
        save_facet_grid_scatterplot(data, directory=f'{data_file_name}_facet_scatterplots')

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
