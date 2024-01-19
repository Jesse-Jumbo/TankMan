import pickle
import numpy as np
import os 
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
from sklearn.neighbors import KNeighborsClassifier
import pygame
from test import *


path  = os.path.join(os.path.dirname(__file__),"..", "log")
allFile = os.listdir(path)
data_set = []

for file in allFile[:]:
    with open(os.path.join(path, file), "rb") as f:
        data_set.append(pickle.load(f))

user_x = []
user_y = []
competitor_x = []
competitor_y = []
user_angle = []
user_gun_angle = []
is_wall_in_bullet_range = []
is_target_in_bullet_range = []
Command = []
bullet = Bullet()

for data in data_set:    
    for i, scene_info in enumerate(data["scene_info"]):
        user_x.append(scene_info["x"])
        user_y.append(scene_info["y"])
        competitor_x.append(scene_info["competitor_info"][0]["x"])
        competitor_y.append(scene_info["competitor_info"][0]["y"])
        user_angle.append(scene_info["angle"])        
        user_gun_angle.append(scene_info["gun_angle"])
        is_wall_in_bullet_range.append(bullet.is_wall_in_bullet_range({"x": scene_info["x"], "y": scene_info["y"]},scene_info["gun_angle"], scene_info["walls_info"], 100))
        is_target_in_bullet_range.append(bullet.is_target_in_bullet_range({"x": scene_info["x"], "y": scene_info["y"]}, scene_info["gun_angle"], {"x":scene_info["competitor_info"][0]["x"], "y":scene_info["competitor_info"][0]["y"]}, BULLET_TRAVEL_DISTANCE))
    for command in data["command"]:
        Command.append(command)

Command = np.array(Command)
Command = Command.reshape(len(Command), 1)

# Feature

X = np.array([0, 0, 0, 0, 0, 0, 0, 0])
for i in range(len(user_y)):
    X = np.vstack((X, [user_x[i], user_y[i], competitor_x[i], competitor_y[i], user_angle[i], user_gun_angle[i], is_wall_in_bullet_range[i], is_target_in_bullet_range[i]]))
X = X[1::]

Y = Command[:,0]

################## KNN ##################
print("KNN")
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.1) # 資料拆分成約 7:2:1 的訓練、驗證、測試集
x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.2)
k_range = range(1,30)
scores = []
k_final = 0
Accuracy = 0
FIScore = 0

for k in k_range:
    k = k+1
    model = KNeighborsClassifier(n_neighbors=k)
    model.fit(x_train, y_train)
    y_predict = model.predict(x_val)

    acc = accuracy_score(y_predict, y_val)
    print(f"k = {k}, Accurancy = {acc}")
    scores.append(acc)
    if acc > Accuracy:
        Accuracy = acc
        k_final = k

    fs = f1_score(y_val, y_predict, average="weighted")
    print("k = ", k, ",F1 score = %.2f" % fs)
    scores.append(fs)
    if fs > FIScore:
        FIScore = fs
        k_final = k

model = KNeighborsClassifier(n_neighbors=k_final)
model.fit(x_train, y_train)
y_predict = model.predict(x_test)
Accuracy = float('{:.3f}'.format(accuracy_score(y_predict, y_test))) # 分對的比例
training_score = float('{:.3f}'.format(model.score(x_train, y_train)))
testing_score = float('{:.3f}'.format(model.score(x_test, y_test)))
print("k = ", k_final, "Accuracy = ", Accuracy)
print("training data score = ", training_score)
print("testing data score = ", testing_score)

# save the model
path = os.path.join(os.path.dirname(__file__), "save")
if not os.path.isdir(path):
    os.mkdir(path)

with open(os.path.join(os.path.dirname(__file__), "save", \
        "KNN_classification.pickle"), "wb") as f:
    pickle.dump(model,f)