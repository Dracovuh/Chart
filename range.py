import pandas as pd
import matplotlib.pyplot as plt
import os
from constants import range_factors

def load_data(file_name):
    try: 
        # Load the CSV file
        data = pd.read_csv(f'./data/data-tokens-v2/token_x20_x50/Average/{file_name}.csv')
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

def filter_outliers(data, factor):
    Q1 = data[factor].quantile(0.25)
    Q3 = data[factor].quantile(0.75)
    IQR = Q3 - Q1
    filtered_data = data[(data[factor] >= (Q1 - 1.5 * IQR)) & (data[factor] <= (Q3 + 1.5 * IQR))]
    return filtered_data

def calculate_statistics(data):
    # Calculate statistics for each factor
    statistics = {}
    for factor in range_factors:
        filtered_data = filter_outliers(data, factor)  # Filter outliers before calculating statistics
        avg = round(filtered_data[factor].mean(), 2)
        var = filtered_data[factor].var()
        std_dev = filtered_data[factor].std()
        
        lower_bound = max(round(avg - std_dev, 2), 0)
        upper_bound = round(avg + std_dev, 2)
        statistics[factor] = {'Average': avg, 'Range': (lower_bound, upper_bound)}

    return statistics

# def calculate_statistics(data):
#     # Calculate statistics for each factor
#     statistics = {}
#     for factor in range_factors:
#         filtered_data = filter_outliers(data, factor)  # Filter outliers before calculating statistics
#         avg = filtered_data[factor].mean()
#         var = filtered_data[factor].var()
#         std_dev = filtered_data[factor].std()
        
#         lower_bound = max(avg - std_dev, 0)  # Ensure lower_bound is not negative
#         upper_bound = avg + std_dev
#         statistics[factor] = {'Average': avg, 'Range': (lower_bound, upper_bound)}

#     return statistics

def create_excel_table(data, output_file):
    # Calculate statistics for the data
    statistics = calculate_statistics(data)
    # Convert statistics to DataFrame
    df = pd.DataFrame(statistics).T
    # Write DataFrame to Excel file
    df.to_excel(output_file)

def main():
    try:
        # Load the CSV file
        data_file_name = 'H1'
        data = load_data(data_file_name)
        # Create Excel table with statistics for factors
        output_file = f'{data_file_name}.xlsx'
        create_excel_table(data, output_file)
        print(f"Excel table with factor statistics saved to: {output_file}")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()