from fastapi import FastAPI
from enum import Enum


app = FastAPI()

class MlAlgorithm(str, Enum):
    lnr = "Linear Regression"
    lor = "Logistic Regression"
    dt = "Decision Tree"
    svm = "SVM Algorithm"
    nvb = "Naive Bayes Algorithm"
    knn = "KNN Algorithm"
    kmeans = "K-Means"
    randf = "Random Forest Algorithm"
    dr = "Dimensionality Reduction Algorithm"
    gb = "Gradient Boosting Algorithm"
    adab = "AdaBoosting Algorithm"

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

@app.get("/algos/{algo_id}")
async def get_ml_algo(algo_id: str):
    return MlAlgorithm[algo_id]



@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}, {"item_name": "CJs Cafe"}]

@app.get("/items/")
async def read_fake_items(skip: int = 0, limit: int = 10, item_name: str = None):
    query = list(filter(lambda d: (d["item_name"] == item_name), fake_items_db[skip: skip + limit]))
    return query