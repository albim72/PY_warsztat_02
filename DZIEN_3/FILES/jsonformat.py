import json

data = {
"name":"Anna",
    "skills":["Python","C++","Java","AI"],
    "active":True
}

with open("data.json","w") as f:
    json.dump(data,f,indent=4,ensure_ascii=False)