from typing import List

from fastapi import FastAPI, UploadFile, File

from ImageFile import file_to_image
from Service import calculate_common_time

app = FastAPI()

# Controller 

@app.get("/classTime")
def info():
    return {"ecsimsw": "2022.08.10"}


@app.post("/classTime")
async def read_item(files: List[UploadFile] = File(...)):
    print(files)
    print(type(files[0]))
    images = []
    for file in files:
        file = await file.read()
        images.append(file_to_image(file))
    common_time = calculate_common_time(images)
    return {"common_table": common_time}