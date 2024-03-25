import pandas as pd
import os
from constants import factors

def load_data(file_name):
    try:
        # Load the CSV file
        data = pd.read_csv(f'./data/data-tokens/{file_name}.csv')
        return data
    except Exception as e:
        raise Exception(f"Error loading data: {e}")

def divide_data_by_token(data):
    # Divide DataFrame into multiple DataFrames for each token
    grouped_tokens = data.groupby('SmartContractAddress')
    token_dataframes = [group.copy() for _, group in grouped_tokens]
    return token_dataframes

def filter_tokens_by_record_count(token_dataframes, min_records=12):
    # Filter token DataFrames by record count
    filtered_dataframes = []
    for df in token_dataframes:
        if len(df) >= min_records:
            filtered_dataframes.append(df)
    return filtered_dataframes

def calculate_average(dataframes):
    averages = {}
    for num_records, prefix in [(3, 'M15'), (6, 'M30'), (12, 'H1')]:
        averages[prefix] = {col: [] for col in factors}
        for df in dataframes:
            for col in factors:
                # Check if any value is null within the specified number of records
                if df[col].head(num_records).isnull().any():
                    
                    averages[prefix][col].append(None)  # or 'NULL' as string if preferred
                else:
                    avg = df[col].head(num_records).mean()
                    averages[prefix][col].append(avg)
    return averages

def save_to_csv(data, token_addresses):
    for prefix, averages in data.items():
        file_name = f'{prefix}.csv'
        df_dict = {'TokenAddress': token_addresses}
        df_dict.update(averages)
        df = pd.DataFrame(df_dict)
        df.to_csv(file_name, index=False)

def main():
    try:
        # Load the CSV file
        data_file_name = 'ai_data_12_row_features_x20_x50'
        data = load_data(data_file_name)

        # Divide DataFrame into multiple DataFrames for each token
        token_dataframes = divide_data_by_token(data)

        # Filter tokens by record count
        filtered_dataframes = filter_tokens_by_record_count(token_dataframes)

        # Extract token addresses
        token_addresses = [df['SmartContractAddress'].iloc[0] for df in filtered_dataframes]

        # Calculate average QuantityHold for each token
        averages = calculate_average(filtered_dataframes)

        # Save results to CSV with token addresses
        save_to_csv(averages, token_addresses)

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()