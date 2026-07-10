import pandas as pd
import argparse
import sys

# Set pandas options to show all data in output
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

class Logger:
    def __init__(self, filename="outputs/report.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "w", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        self.terminal.flush()
        self.log.flush()

def compare_results(gt_path, result_path, sheet_name="Study_characteristics", row_index=None):
    try:
        # Load ground truth from Excel
        gt_df = pd.read_excel(gt_path, sheet_name=sheet_name)
        # Load agent results from CSV
        res_df = pd.read_csv(result_path)
        
        # Ensure both dataframes are cleaned of whitespace in column names
        gt_df.columns = gt_df.columns.str.strip()
        res_df.columns = res_df.columns.str.strip()

        # Filter for a specific row if requested
        if row_index is not None:
            if row_index < 0 or row_index >= len(gt_df):
                print(f"Error: Row index {row_index} out of bounds for ground truth file.")
                return
            gt_df = gt_df.iloc[[row_index]]
            print("GT Paper title is ", gt_df["Title"])

        # Find common columns to compare
        common_cols = list(set(gt_df.columns) & set(res_df.columns))
        if not common_cols:
            print("No common columns found between ground truth and results.")
            return

        # We assume there is a unique identifier to align rows (e.g., 'Study' or 'ID')
        # If no obvious ID, we try to align by index or a likely ID column
        id_col = next((col for col in common_cols if 'id' in col.lower() or 'study' in col.lower()), None)
        
        if id_col:
            gt_df = gt_df.set_index(id_col)
            res_df = res_df.set_index(id_col)
        
        # Align dataframes
        common_index = gt_df.index.intersection(res_df.index)
        if common_index.empty:
            print("No matching identifiers found between ground truth and results.")
            return
            
        gt_df = gt_df.loc[common_index, common_cols]
        res_df = res_df.loc[common_index, common_cols]

        # Compute differences
        # fillna('') to ensure NaN == NaN is handled as equality for strings
        gt_filled = gt_df.fillna('')
        res_filled = res_df.fillna('')
        
        comparison = (gt_filled == res_filled)
        accuracy = comparison.mean().mean() * 100
        
        print(f"Comparison Results:\n")
        print(f"Overall Accuracy: {accuracy:.2f}%")
        print("\nAccuracy per column:")
        print(comparison.mean() * 100)
        
        # Find mismatches
        mismatches = []
        for col in common_cols:
            diff = gt_filled[col] != res_filled[col]
            for idx in gt_filled.index[diff]:
                mismatches.append({
                    'id': idx,
                    'column': col,
                    'expected': gt_filled.loc[idx, col],
                    'actual': res_filled.loc[idx, col]
                })
        
        if mismatches:
            print("\nMismatches found:")
            print(pd.DataFrame(mismatches))
        else:
            print("\nNo mismatches found!")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare agent results CSV with ground truth Excel.")
    parser.add_argument("--gt", required=True, help="Path to ground truth .xlsx file")
    parser.add_argument("--res", required=True, help="Path to results .csv file")
    parser.add_argument("--sheet", default="Study_characteristics", help="Sheet name in Excel file")
    parser.add_argument("--row", type=int, default=None, help="Specific row index from ground truth to compare")
    
    args = parser.parse_args()
    
    sys.stdout = Logger("outputs/barr-gemma4-0.0.log")
    compare_results(args.gt, args.res, args.sheet, args.row)
