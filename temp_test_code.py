import os
import shutil

def organize_files(base_path):
    # boxart와 snapshot 폴더 경로 생성
    boxart_path = os.path.join(base_path, 'boxart')
    snapshot_path = os.path.join(base_path, 'snapshot')
    logo_path = os.path.join(base_path, 'logo')

    os.makedirs(boxart_path, exist_ok=True)
    os.makedirs(snapshot_path, exist_ok=True)
    os.makedirs(logo_path, exist_ok=True)


    # 하위 폴더 탐색
    for root, dirs, files in os.walk(base_path):
        if root == boxart_path or root == snapshot_path:
            continue

        folder_name = os.path.basename(root)

        for file_name in files:
            file_path = os.path.join(root, file_name)

            if file_name == 'boxFront.jpg':
                new_file_name = f"{folder_name}.jpg"
                shutil.move(file_path, os.path.join(boxart_path, new_file_name))

            elif file_name == 'video.mp4':
                new_file_name = f"{folder_name}.mp4"
                shutil.move(file_path, os.path.join(snapshot_path, new_file_name))

            elif file_name == 'logo.png':
                new_file_name = f"{folder_name}.png"
                shutil.move(file_path, os.path.join(logo_path, new_file_name))

if __name__ == "__main__":
    # 사용자로부터 경로 입력 받기
    base_path = input("Enter the folder path: ").strip()

    if os.path.exists(base_path) and os.path.isdir(base_path):
        organize_files(base_path)
        print("Operation completed successfully!")
    else:
        print("Invalid path. Please provide a valid folder path.")
