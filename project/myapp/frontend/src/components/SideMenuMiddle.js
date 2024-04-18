const MongoClient = require('mongodb').MongoClient;

// Connection URL
const url = 'mongodb://localhost:27017';

// Database Name
const dbName = 'your_database_name';

// Collection Name
const collectionName = 'your_collection_name';

// Create a new MongoClient
const client = new MongoClient(url, { useNewUrlParser: true });

// Connect to the MongoDB server
client.connect(function(err) {
    if (err) {
        console.error('Error connecting to the database:', err);
        return;
    }

    console.log('Connected successfully to the database');

    // Get the database instance
    const db = client.db(dbName);

    // Get the collection
    const collection = db.collection(collectionName);

    // Find all documents in the collection
    collection.find({}).toArray(function(err, documents) {
        if (err) {
            console.error('Error retrieving documents:', err);
            return;
        }

        console.log('Retrieved documents:', documents);
    });

    // Close the connection
    client.close();
});