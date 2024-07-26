from scipy.stats import ttest_ind, levene
import os
import pandas as pd

def read_data(filename, model1, model2):
    df = pd.read_csv(filename)
    record_accuracy = [0, 0]
    recommendation_accuracy = [0, 0]
    average_rating = [0, 0]
    average_top_rating = [0, 0]
    for index, row in df.iterrows():
        if row['Attributes'] == "Record Accuracy":
            record_accuracy = [row[model1], row[model2]]
        elif row['Attributes'] == "Recommendation Accuracy":
            recommendation_accuracy = [row[model1], row[model2]]
        elif row['Attributes'] == "Average Rating":
            average_rating = [row[model1], row[model2]]
        elif row['Attributes'] == "Average Top Rating":
            average_top_rating = [row[model1], row[model2]]
        else:
            continue
    return record_accuracy, recommendation_accuracy, average_rating, average_top_rating
        

def get_statistical_data(directory, model1, model2):
    filenames = os.listdir(directory)
    times = []
    timedict = {}
    result = {}
    result[model1] = {"record_accuracy": [], "recommendation_accuracy": [], "average_rating": [], "average_top_rating": []}
    result[model2] = {"record_accuracy": [], "recommendation_accuracy": [], "average_rating": [], "average_top_rating": []}
    for file in filenames:
        time = file.replace("Eval", "").replace(".csv", "")[:-2] + "30"
        times.append(time)
        record_accuracy, recommendation_accuracy, average_rating, average_top_rating = read_data(directory + file, model1, model2)
        timedict[time] = (record_accuracy, recommendation_accuracy, average_rating, average_top_rating)
    times.sort()
    for time in times:
        record_accuracy, recommendation_accuracy, average_rating, average_top_rating = timedict[time]
        result[model1]["record_accuracy"].append(record_accuracy[0])
        result[model2]["record_accuracy"].append(record_accuracy[1])
        result[model1]["recommendation_accuracy"].append(recommendation_accuracy[0])
        result[model2]["recommendation_accuracy"].append(recommendation_accuracy[1])
        result[model1]["average_rating"].append(average_rating[0])
        result[model2]["average_rating"].append(average_rating[1])
        result[model1]["average_top_rating"].append(average_top_rating[0])
        result[model2]["average_top_rating"].append(average_top_rating[1])
    return result

def Ttest(result, attribute, model1, model2):
    data1 = result[model1][attribute]
    data2 = result[model2][attribute]
    print("model1 data on " + attribute, data1)
    print("model2 data on " + attribute, data2)
    print("The mean of model1 data on " + attribute, sum(data1)/len(data1))
    print("The mean of model2 data on " + attribute, sum(data2)/len(data2))
    #ttest, pval = ttest_ind(data1, data2, alternative="greater")
    _, variance_p = levene(data1, data2)
    equal_var = False
    if variance_p > 0.05:
        equal_var = True
    ttest, pval = ttest_ind(data1, data2, equal_var=equal_var, alternative="greater")
    print("t-test", '{0:.10f}'.format(ttest))
    print("p-value", '{0:.10f}'.format(pval))
    return ttest, pval

directory = "./Online0413/"
model1 = "KNN2022-04-08"
model2 = "KNN2022-04-12"
result = get_statistical_data(directory, model1, model2)
print(result)
attributes = ["record_accuracy", "recommendation_accuracy", "average_rating", "average_top_rating"]
for attr in attributes:
    ttest, pval = Ttest(result, attr, model1, model2)
    if pval < 0.05:
        print("we reject null hypothesis that " + model1 + " is not better than " + model2 + " on " + attr)
    else:
        print("we accept null hypothesis that " + model1 + " is not better than " + model2 + " on " + attr)