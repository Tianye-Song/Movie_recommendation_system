# Mongo commands

## Create Collections
- db.createCollection("movies")
- db.createCollection("users")
- db.createCollection("rates")
- db.createCollection("recommend_history")
- db.createCollection("views_history")
- db.createCollection("recommendations")
- db.createCollection("recommendations_m1")
- db.createCollection("recommendations_m2")



## Create unique indexes
- db.users.createIndex({"user_id":1}, {unique: true})
- db.movies.createIndex({"movie_id":1}, {unique: true})
- db.rates.createIndex({"user_id":1, "movie_id":1}, {unique: true})
- db.views_history.createIndex({"time_read":1, "user_id":1}, {unique: true})
- db.recommend_history.createIndex({"time_read":1, "user_id":1}, {unique: true})
- db.recommendations.createIndex({"user_id":1}, {unique: true})
- db.recommendations_m1.createIndex({"user_id":1}, {unique: true})
- db.recommendations_m2.createIndex({"user_id":1}, {unique: true})

## Find unique
- db.users.distinct("user_id").length == db.users.countDocuments()
- db.movies.distinct("movie_id").length == db.movies.countDocuments()
- db.users.aggregate([{ $group: { _id: { user_id: "$user_id" }, uniqueIds: { $addToSet: "$user_id" }, count: { $sum: 1 } } }, { $match: { count: { "$gt": 1 } } }])
- db.users.aggregate([{ $group: { _id: { movie_id: "$movie_id" }, uniqueIds: { $addToSet: "$movie_id" }, count: { $sum: 1 } } }, { $match: { count: { "$gt": 1 } } }])



## Query examples
- query = {"user_id":28}
- query = {"movie_id":some+cool+movie+id}


## Projection examples (fields to include/exclue)
- query = {"_id":0} (not include filed _id) 
- query = {"user_id":1, "occupation":1} (show only user_id and occupation)


## Check responses
- db.recommend_history.find({ "time_read": { $regex:"2022-02-09" }}).count()
- db.recommend_history.find({ "time_read": { $regex:"2022-02-09" }, "status":200 }).count()
- db.recommend_history.find({ "time_read": { $regex:"2022-02-09" }, "status":200, response_time:{$lt:800} }).count()
- db.recommend_history.find({ "time_read": { $regex:"2022-02-09" }, response_time:{$gt:800} }).count()

### Percentage correct (should be > 40%)
- db.recommend_history.find({ "time_read": { $regex:"2022-02-09" }, "status":200, response_time:{$lt:800} }).count()/db.recommend_history.find({ "time_read": { $regex:"2022-02-09" }}).count()

### Metrics (Inference Cost)
(TODO: Change regex to date for versatility (e.g. comparision operators))

- db.recommend_history.aggregate([{$match :{ "time_read": { $regex:"2022-02-09" }}},  {$group:{_id: {},avgResponseTime: { $avg: "$response_time" }}}])
- db.recommend_history.aggregate([{$match :{ "time_read": { $regex:"2022-02-09" }}},  {$group:{_id: {},maxResponseTime: { $max: "$response_time" }}}])
- db.recommend_history.aggregate([{$match :{ "time_read": { $regex:"2022-02-09" }}},  {$group:{_id: {},minResponseTime: { $min: "$response_time" }}}])

