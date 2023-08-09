import os

from .move import Move
from .random_timer import RandomTimer

g_tap = False
g_dragging = False

# 创建一个移动工具和计时器，分别用于移动窗口和变换角色动作
g_move = Move()
g_timer = RandomTimer()

def g_construct_path(*path):
    return "." + os.path.join(*path).replace('\\', '/')
