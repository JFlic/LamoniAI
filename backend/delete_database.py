from pymilvus import connections, utility

# Connect to Milvus
connections.connect(alias="default", uri="http://localhost:19530")

# Specify the collection name
collection_name = "lamoni_collection"  # Change this to the collection you want to delete

# Check if the collection exists
if utility.has_collection(collection_name):
    # Drop the collection (delete all data)
    utility.drop_collection(collection_name)
    print(f"Collection '{collection_name}' has been deleted.")
else:
    print(f"Collection '{collection_name}' does not exist.")