To check existing database
show dbs
use production

To check existing collections
show collections
db.movies.findOne()

find duplicates
db.movies.aggregate([
    {"$group" : { "_id": "$movie_id", "count": { "$sum": 1 } } },
    {"$match": {"_id" :{ "$ne" : null } , "count" : {"$gt": 1} } }, 
    {"$project": {"name" : "$_id", "_id" : 0} }
])

find max value
db.sales.aggregate(
   [{$group:{_id: "$item",
            maxTotalAmount: { $max: { $multiply: [ "$price", "$quantity" ] } },
           maxQuantity: { $max: "$quantity" }
           }}])

db.inventory.find( { quantity: { $gt: 20 } } )
