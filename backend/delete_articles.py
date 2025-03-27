import os
from dotenv import load_dotenv
from pymilvus import connections, utility, Collection
from pymilvus.client.types import DataType
import glob

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)

# Constants
MILVUS_URI = "http://localhost:19530/"
COLLECTION_NAME = "lamoni_collection"
WEBSITE_DIR = "GracelandWebsite"

def delete_markdown_file(title):
    """
    Delete the corresponding markdown file from the GracelandWebsite directory.
    
    Args:
        title (str): The title of the article to delete
    """
    try:
        # Convert title to filename format (lowercase, replace spaces with hyphens)
        filename = title.lower().replace(" ", "-") + ".md"
        file_path = os.path.join(WEBSITE_DIR, filename)
        
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Successfully deleted markdown file: {filename}")
        else:
            print(f"No markdown file found for title: {title}")
            
    except Exception as e:
        print(f"Error deleting markdown file: {e}")

def delete_article_by_title(title):
    """
    Delete an article from the Milvus collection by its title.
    
    Args:
        title (str): The title of the article to delete
    """
    try:
        # Connect to Milvus
        connections.connect(alias="default", uri=MILVUS_URI)
        
        # Get the collection
        collection = Collection(name=COLLECTION_NAME)
        
        # Load the collection
        collection.load()
        
        # Create a query expression to find documents with matching title
        expr = f'title == "{title}"'
        
        # Execute the delete operation
        result = collection.delete(expr)
        
        if result:
            print(f"Successfully deleted article with title: {title}")
            print(f"Number of chunks deleted: {result}")
            # Also delete the markdown file
            delete_markdown_file(title)
        else:
            print(f"No article found with title: {title}")
            
    except Exception as e:
        print(f"Error deleting article: {e}")
    finally:
        # Disconnect from Milvus
        connections.disconnect("default")

def list_all_titles():
    """
    List all unique titles in the collection.
    """
    try:
        # Connect to Milvus
        connections.connect(alias="default", uri=MILVUS_URI)
        
        # Get the collection
        collection = Collection(name=COLLECTION_NAME)
        
        # Load the collection
        collection.load()
        
        # Query all titles
        results = collection.query(
            expr="",
            output_fields=["title"],
            consistency_level="Strong"
        )
        
        # Extract unique titles
        unique_titles = list(set(item["title"] for item in results))
        
        print("\nAvailable articles:")
        for i, title in enumerate(unique_titles, 1):
            print(f"{i}. {title}")
            
    except Exception as e:
        print(f"Error listing titles: {e}")
    finally:
        # Disconnect from Milvus
        connections.disconnect("default")

if __name__ == "__main__":
    # First, show all available titles
    print("Fetching available articles...")
    
    # Ask user which article to delete
    title_to_delete = input("\nEnter the title of the article to delete: ")
    
    delete_article_by_title(title_to_delete)