import os



PATH = "newData/images"
with open("newData/data_img.txt", "w") as f:
    for img in os.listdir(PATH):
        f.write(f"{PATH}/{img}\n")

print(len(os.listdir(PATH)))