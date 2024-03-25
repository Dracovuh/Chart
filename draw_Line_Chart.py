import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns

from constants import features, target

# Set seaborn style
sns.set(style="whitegrid", palette="husl")

def load_data(file_name):
    try:
        # Load the CSV file
        data = pd.read_csv(f'./data/data-tokens/{file_name}.csv')
        data = data.iloc[::-1]  # Reverse the DataFrame
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
    grouped_tokens = data.groupby('Id')
    token_dataframes = [group.copy() for _, group in grouped_tokens]
    return token_dataframes

def save_charts(data_file_name, token_address, dataAI, save_path):
    # Save charts for each feature
    bug_tokens = []

    for feature in features:
        valid_data = dataAI.dropna(subset=[feature])
        if not valid_data.empty:
            # Plot the data using seaborn
            sns.set(font_scale=1.2)
            plt.figure(figsize=(12, 8))

            # Plot the target and feature on the same axis with smooth lines
            ax = sns.lineplot(x=valid_data.index, y=valid_data[target], label=target, color='darkblue', linewidth=2)
            ax2 = ax.twinx()
            ax2 = sns.lineplot(x=valid_data.index, y=valid_data[feature], label=feature, color='darkorange', linewidth=2)

            # Set labels and title
            ax.set_xlabel('Index')
            ax.set_ylabel(f'{target}', color='darkblue')
            ax2.set_ylabel(f'{feature}', color='darkorange')

            # Set legend
            lines, labels = ax.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax2.legend(lines + lines2, labels + labels2, loc='upper left')

            # Set title and save chart
            plt.title(f'{feature} vs {target} for {token_address}', fontsize=16)
            plt.tight_layout()

            try:
                os.makedirs(save_path, exist_ok=True)
                plt.savefig(f'{save_path}/{feature}_{target}.png')
                plt.close()
            except Exception as e:
                bug_tokens.append([token_address, e])
                continue

    return bug_tokens

def main():
    try:
        # Load the CSV file
        data_file_name = 'data-100target-test-v3'
        data = load_data(data_file_name)

        # Statistic null data of each column
        analyze_null_values(data)

        # Divide DataFrame into multiple DataFrames for each token
        token_dataframes = divide_data_by_token(data)
        bug_tokens = []

        # Save charts
        for token_dataframe in token_dataframes:
            try:
                token_address = token_dataframe["SmartContractAddress"].iloc[0]
                feature_cols = features + [target]
                dataAI = token_dataframe[feature_cols]
                # dataAI.dropna(inplace=True)
                dataAI.reset_index(drop=True, inplace=True)

                save_path = fr'comparisons/{data_file_name}/{token_address}'
                bug_tokens.extend(save_charts(data_file_name, token_address, dataAI, save_path))

            except Exception as e:
                bug_tokens.append([token_address, e])
                continue

        print([len(bug_tokens), bug_tokens])

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
