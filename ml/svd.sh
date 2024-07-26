dvc run -n KNN_$2_$1 -o KNN_$2_$1/data.json -o KNN_$2_$1/ratings.csv -o KNN_$2_$1/model.pickle python3 ml/KNN_recommendation.py $2
dvc remote add -d storage gdrive://1FfjotJsAccDsz6nDX1LmJPDbjmJWtwY6
dvc push