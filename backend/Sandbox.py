import pandas as pd

def find_url(csv_file, document_name):
    """
    Search for a document name in a CSV file and return the corresponding URL.
    
    Parameters:
    csv_file (str): Path to the CSV file.
    document_name (str): The name of the document to search for.
    
    Returns:
    str: The corresponding URL if found, otherwise None.
    """
    try:
      df = pd.read_csv(csv_file)
      result = df.loc[df.iloc[:, 1] == document_name, df.columns[0]]
      return result.values[0] if not result.empty else None
    except Exception as e:
        print(f"Error: {e}")
        return None
    

print(find_url("GetPDFUrls.csv", "Graybill.pdf"))