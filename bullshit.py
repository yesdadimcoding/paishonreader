import os

if __name__ == "__main__":
    for (root,dir, files) in os.walk(r"C:\Users\ADMIN\Desktop\MangaHaven\what", topdown = False):
        new_path = os.path.join(str(root), str(files))
        print(new_path)
