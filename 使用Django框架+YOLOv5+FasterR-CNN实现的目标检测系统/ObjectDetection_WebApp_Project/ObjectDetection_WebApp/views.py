from django.shortcuts import render

# Create your views here.
import os, re, sys
import mimetypes
from wsgiref.util import FileWrapper
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.shortcuts import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.http import FileResponse
from django.utils.encoding import smart_str
import subprocess
import glob
import time
import shutil


def index(request):
    return render(request, 'login.html')


def gotoregister(request):
    return render(request, 'register.html')


def gotologin(request):
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        # 获取注册信息
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 读取用户编号
        with open('user/id.txt', 'r') as f:
            data = f.read()
            last_id = int(data) if data.strip() else 0  # 如果文件为空，则默认为1

        # 创建新用户并保存信息
        new_id = last_id + 1
        with open('user/id.txt', 'w') as f:
            f.write(str(new_id))
        with open('user/username.txt', 'a') as f:
            f.write(f'{new_id} {username}\n')
        with open('user/password.txt', 'a') as f:
            f.write(f'{new_id} {password}\n')

        # 注册成功返回提示信息
        return render(request, 'login.html')


def login(request):
    if request.method == 'POST':
        # 获取登录信息
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)

        # 验证登录信息
        user_found = False
        with open('user/username.txt', 'r') as user_file:
            for line in user_file:
                line_id, line_username = line.strip().split(' ')
                if line_username == username:
                    user_found = True
                    break

        if not user_found:
            # 登录失败返回错误信息
            print("用户登录失败：用户名不存在")
            return render(request, 'login.html')

        with open('user/password.txt', 'r') as password_file:
            for line in password_file:
                line_id, line_password = line.strip().split(' ')
                if line_username == username and line_password == password:
                    # 登录成功返回提示信息
                    print("用户登录成功")
                    return render(request, 'index.html')

        # 登录失败返回错误信息
        print("用户登录失败：密码错误")
        return render(request, 'login.html')
    else:
        # 允许通过GET请求访问登录页面
        return HttpResponse('请使用POST请求进行登录')


def object_detection(request):
    return render(request, 'object_detection.html')


def upload_file(request):
    if request.method == 'POST' and request.FILES.get('video_file'):
        uploaded_file = request.FILES['video_file']
        # 在 MEDIA_ROOT 中直接保存上传的文件
        destination_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
        # 将路径中的 '\\' 替换为 '/'
        destination_path = destination_path.replace('\\', '/')

        # 确保目标文件夹存在，如果不存在则创建
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)

        with open(destination_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        return render(request, 'upload_success.html')

    # 如果请求不是 POST 方法或者没有上传文件，返回一个空的 HTTP 响应
    return HttpResponse()


def video(request):
    return render(request, 'video/video.html', {})


def start_detect(request):
    script = request.POST.get('script')  # 获取用户选择的脚本
    if script == "YOLOv5":
        # 获取命令行工具路径
        tool_path = os.path.join(os.path.dirname(__file__), '..', '..', 'yolov5-master', 'detect.py')
        # 获取Python解释器路径
        python_interpreter = r'C:\Users\LiTianyi\.conda\envs\object_detection\python.exe'
        # 构建权重文件路径
        weights_path = os.path.join(os.getcwd(), '..', 'yolov5-master', 'weights', 'uav-yolov5m-30epoc.pt')
        # 开始计时
        start_time = time.time()
        # 执行Python脚本
        subprocess.run([python_interpreter, tool_path, '--weights', weights_path])
        # 结束计时
        end_time = time.time()
        # 计算运行时间
        runtime = end_time - start_time
        print("目标检测耗时：{:.2f} 秒".format(runtime))
        # 将耗时信息保存
        save_path = "./media"
        filename = "detection_results.txt"
        with open(os.path.join(save_path, filename), 'a') as file:
            file.write("此次目标检测耗时：{:.2f} 秒".format(runtime))

        # 将检测完的视频放到media文件夹中
        # 定义相对路径
        detect_dir = "../yolov5-master/runs/detect/"
        # 找到最新创建的文件夹
        latest_folder = max(glob.glob(os.path.join(detect_dir, "*/")), key=os.path.getmtime)
        print(latest_folder)
        # 找到该文件夹下的所有mp4视频文件
        videos = glob.glob(os.path.join(latest_folder, "*.mp4"))
        # 如果目标文件夹只有一个mp4文件，则直接复制到media目录，并重命名为002.mp4
        if len(videos) == 1:
            video = videos[0]
            new_name = os.path.join(settings.MEDIA_ROOT, "002.mp4")
            shutil.copyfile(video, new_name)

    else:
        print("Faster-R-CNN还没接入")
        # 获取命令行工具路径
        tool_path = os.path.join(os.path.dirname(__file__), '..', '..', 'faster-rcnn-pytorch', 'predict.py')
        # 获取Python解释器路径
        python_interpreter = r'C:\Users\LiTianyi\.conda\envs\object_detection2\python.exe'
        # 开始计时
        start_time = time.time()
        # 执行Python脚本
        subprocess.run([python_interpreter, tool_path],
                       cwd=r'D:\python\pythonProject\ObjectDetection\faster-rcnn-pytorch')
        # 结束计时
        end_time = time.time()
        # 计算运行时间
        runtime = end_time - start_time
        print("目标检测耗时：{:.2f} 秒".format(runtime))
        # 将耗时信息保存
        save_path = "./media"
        filename = "detection_results.txt"
        with open(os.path.join(save_path, filename), 'a') as file:
            file.write("此次目标检测耗时：{:.2f} 秒".format(runtime))

    return render(request, 'object_detection.html')


def clear_cache(request):
    # 获取目录中的所有文件
    files = os.listdir(settings.MEDIA_ROOT)
    # 删除目录中的所有文件
    for file in files:
        file_path = os.path.join(settings.MEDIA_ROOT, file)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"已删除文件: {file_path}")
        except Exception as e:
            print(f"删除文件 '{file_path}' 时出错: {e}")
    return render(request, 'object_detection.html')


def download_data(request):
    file_path = "./media/detection_results.txt"  # 替换成你要下载的文件的本地路径
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            print(1)
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            print(2)
            response['Content-Disposition'] = 'attachment; filename="detection_results.txt"'
            return response
    else:
        return HttpResponse("File not found")

