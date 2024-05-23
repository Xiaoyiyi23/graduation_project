import os

weights_path = r"D:\python\pythonProject\ObjectDetection\ObjectDetection_WebApp_Project\..\yolov5-master\weights\uav-yolov5m-30epoc.pt"

if os.path.exists(weights_path):
    print("权重文件存在")
else:
    print("权重文件不存在")
