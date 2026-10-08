import os
import shutil
import time
import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from tkinterdnd2 import DND_FILES, TkinterDnD

# 日志文件
log_file = os.path.join(os.path.dirname(__file__), "提取日志.txt")

def write_log(text):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {text}"
    txt.insert(tk.END, line + "\n")
    txt.see(tk.END)
    root.update()
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def unique_name(dst_dir, filename):
    name, ext = os.path.splitext(filename)
    candidate = filename
    index = 1
    while os.path.exists(os.path.join(dst_dir, candidate)):
        candidate = f"{name}_{index}{ext}"
        index += 1
    return candidate

def process_folder(folder):
    folder = os.path.abspath(folder)
    parent_dir = os.path.dirname(folder)
    moved_count = 0

    write_log(f"开始处理: {folder}")
    write_log(f"目标目录: {parent_dir}")

    for root_dir, dirs, files in os.walk(folder, topdown=False):
        for file in files:
            src_file = os.path.join(root_dir, file)
            dst_file = os.path.join(parent_dir, unique_name(parent_dir, file))
            try:
                shutil.move(src_file, dst_file)
                moved_count += 1
            except Exception as e:
                write_log(f"移动失败: {src_file} 原因: {e}")

    # 删除空文件夹
    for root_dir, dirs, files in os.walk(folder, topdown=False):
        for d in dirs:
            try:
                os.rmdir(os.path.join(root_dir, d))
            except:
                pass
    try:
        os.rmdir(folder)
    except:
        pass

    write_log(f"完成: 共移动 {moved_count} 个文件")
    write_log("="*60)
    return moved_count

def on_drop(event):
    folders = root.tk.splitlist(event.data)
    total = 0
    # 恢复窗口背景
    root.config(bg=default_bg)
    for folder in folders:
        folder = folder.strip("{}")
        if os.path.isdir(folder):
            total += process_folder(folder)
    messagebox.showinfo("完成", f"成功处理 {total} 个文件")
    
def on_drag_enter(event):
    root.config(bg="#d1ffd1")  # 浅绿色

def on_drag_leave(event):
    root.config(bg=default_bg)

# 创建窗口
root = TkinterDnD.Tk()
root.title("子文件夹文件提取器")
root.geometry("800x500")
default_bg = root.cget("bg")

# 提示标签
label = tk.Label(root, text="将一个或多个文件夹拖到窗口任意位置", font=("微软雅黑", 16))
label.pack(pady=10)

# 日志显示框
txt = ScrolledText(root)
txt.pack(fill="both", expand=True, padx=10, pady=10)

# 注册拖拽
root.drop_target_register(DND_FILES)
root.dnd_bind("<<Drop>>", on_drop)
root.dnd_bind("<<DragEnter>>", on_drag_enter)
root.dnd_bind("<<DragLeave>>", on_drag_leave)

# 运行
root.mainloop()
