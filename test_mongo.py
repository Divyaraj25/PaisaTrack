"""
Script to test MongoDB connection
"""
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

def test_mongo_connection():
    """Test MongoDB connection"""
    try:
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
        
        # Test the connection
        client.admin.command('ping')
        
        # Get database names
        db_names = client.list_database_names()
        
        print("MongoDB connection successful!")
        print(f"Available databases: {db_names}")
        
        # Check if paisatrack database exists
        if 'paisatrack' in db_names:
            db = client['paisatrackIN']
            collection_names = db.list_collection_names()
            print(f"PaisaTrack collections: {collection_names}")
            
            # Check if collections have data
            if 'info' in collection_names:
                info_count = db['info'].count_documents({})
                print(f"Info collection has {info_count} documents")
            
            if 'categories' in collection_names:
                categories_count = db['categories'].count_documents({})
                print(f"Categories collection has {categories_count} documents")
        else:
            print("PaisaTrack database not found. Run init_mongo.py to create it.")
            
        client.close()
        return True
        
    except ConnectionFailure:
        print("Failed to connect to MongoDB. Please ensure MongoDB is running.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

if __name__ == "__main__":
    test_mongo_connection()