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
        data = pd.read_csv(f'./data/data-tokens-v2/Tokens/{file_name}.csv')
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

def save_histogram(data, num_bins=20, directory='histograms'):
    # Create directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)

    # Save histogram for each factor
    for factor in factors:
        plt.figure(figsize=(10, 6))
        
        # Check if any value in the factor column is smaller than 0
        if (data[factor] < 0).any():
            # Calculate bin edges based on the maximum and minimum values of the factor column
            min_value = data[factor].min()
            max_value = data[factor].max()
            bin_edges = [min_value + i * (max_value - min_value) / num_bins for i in range(num_bins + 1)]
        else:
            # Calculate bin edges based only on the maximum value of the factor column
            max_value = data[factor].max()
            bin_width = max_value / num_bins
            bin_edges = [i * bin_width for i in range(num_bins + 1)]
        
        # Create histogram
        n, bins, patches  = plt.hist(data[factor], bins=bin_edges, alpha=0.7, color='skyblue', edgecolor='black')
        
        # Annotate each bin with its maximum value
        for edge in bin_edges[1:]:
            plt.text(edge, 0, f'{round(edge, 2)}', ha='center', va='bottom', rotation=90, fontsize=8)
        
        plt.xlabel(factor)
        plt.ylabel('Numbers of token')
        plt.title(f'Histogram of {factor}')
        plt.grid(True)
        
        # Display only integer values on the y-axis
        plt.yticks(range(int(max(n)) + 1))
        
        plt.savefig(os.path.join(directory, f'{factor}_histogram.png'))
        plt.close()

def main():
    try:
        # Load the CSV file
        data_file_name = 'M15'
        data = load_data(data_file_name)

        # Divide DataFrame into multiple DataFrames for each token
        token_dataframes = divide_data_by_token(data)

        # Filter tokens by record count
        filtered_dataframes = filter_tokens_by_record_count(token_dataframes)

        # Save histogram for each factor
        save_histogram(data, directory=f'{data_file_name}_histograms')

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()