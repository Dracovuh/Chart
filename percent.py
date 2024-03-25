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

def calculate_percentage_change(dataframes):
    percentages = {}
    for num_records, prefix in [(3, 'M15'), (6, 'M30'), (12, 'H1')]:
        percentages[prefix] = {col: [] for col in factors}
        for df in dataframes:
            for col in factors:
                # Check if the dataframe has enough records for the current section
                if len(df) >= num_records:
                    # Get the subset of records for the current section
                    subset_df = df.head(num_records)
                    
                    # Check if any value is null within the subset of records
                    if subset_df[col].isnull().any() or subset_df[col].iloc[0] == 0:
                        percentages[prefix][col].append(None)  # or 'NULL' as string if preferred
                    else:
                        first_value = subset_df[col].iloc[0]
                        last_value = subset_df[col].iloc[-1]
                        percentage_change = ((last_value - first_value) * 100) / first_value
                        percentages[prefix][col].append(percentage_change)
                else:
                    # If there are not enough records, append None for all factors
                    percentages[prefix][col].append(None)
    return percentages


def save_to_csv(data, token_addresses):
    for prefix, percentages in data.items():
        file_name = f'{prefix}.csv'
        df_dict = {'TokenAddress': token_addresses}
        df_dict.update(percentages)
        df = pd.DataFrame(df_dict)
        df.to_csv(file_name, index=False)

def main():
    try:
        # Load the CSV file
        data_file_name = 'token_x20_x50'
        data = load_data(data_file_name)

        # Divide DataFrame into multiple DataFrames for each token
        token_dataframes = divide_data_by_token(data)

        # Filter tokens by record count
        filtered_dataframes = filter_tokens_by_record_count(token_dataframes)

        # Extract token addresses
        token_addresses = [df['SmartContractAddress'].iloc[0] for df in filtered_dataframes]

        # Calculate percentage change for each token
        percentages = calculate_percentage_change(filtered_dataframes)

        # Save results to CSV with token addresses
        save_to_csv(percentages, token_addresses)

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
