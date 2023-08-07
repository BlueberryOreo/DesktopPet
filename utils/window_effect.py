# coding:utf-8
from ctypes import POINTER, Structure, c_int, WinDLL, c_bool, sizeof, pointer
from ctypes.wintypes import DWORD, HWND, ULONG, POINT, RECT, UINT
from enum import Enum


class WINDOWCOMPOSITIONATTRIB(Enum):
    WCA_UNDEFINED = 0
    WCA_NCRENDERING_ENABLED = 1
    WCA_NCRENDERING_POLICY = 2
    WCA_TRANSITIONS_FORCEDISABLED = 3
    WCA_ALLOW_NCPAINT = 4
    WCA_CAPTION_BUTTON_BOUNDS = 5
    WCA_NONCLIENT_RTL_LAYOUT = 6
    WCA_FORCE_ICONIC_REPRESENTATION = 7
    WCA_EXTENDED_FRAME_BOUNDS = 8
    WCA_HAS_ICONIC_BITMAP = 9
    WCA_THEME_ATTRIBUTES = 10
    WCA_NCRENDERING_EXILED = 11
    WCA_NCADORNMENTINFO = 12
    WCA_EXCLUDED_FROM_LIVEPREVIEW = 13
    WCA_VIDEO_OVERLAY_ACTIVE = 14
    WCA_FORCE_ACTIVEWINDOW_APPEARANCE = 15
    WCA_DISALLOW_PEEK = 16
    WCA_CLOAK = 17
    WCA_CLOAKED = 18
    WCA_ACCENT_POLICY = 19
    WCA_FREEZE_REPRESENTATION = 20
    WCA_EVER_UNCLOAKED = 21
    WCA_VISUAL_OWNER = 22
    WCA_LAST = 23


class ACCENT_STATE(Enum):
    """ 客户区状态枚举类 """
    ACCENT_DISABLED = 0
    ACCENT_ENABLE_GRADIENT = 1
    ACCENT_ENABLE_TRANSPARENTGRADIENT = 2
    ACCENT_ENABLE_BLURBEHIND = 3          # Aero效果
    ACCENT_ENABLE_ACRYLICBLURBEHIND = 4   # 亚克力效果
    ACCENT_INVALID_STATE = 5


class ACCENT_POLICY(Structure):
    """ 设置客户区的具体属性 """

    _fields_ = [
        ("AccentState",     DWORD),
        ("AccentFlags",     DWORD),
        ("GradientColor",   DWORD),
        ("AnimationId",     DWORD),
    ]


class WINDOWCOMPOSITIONATTRIBDATA(Structure):
    _fields_ = [
        ("Attribute",   DWORD),
        # POINTER()接收任何ctypes类型，并返回一个指针类型
        ("Data",        POINTER(ACCENT_POLICY)),
        ("SizeOfData",  ULONG),
    ]


class WindowEffect:
    def __init__(self) -> None:
        self.user32 = WinDLL("user32")
        self.SetWindowCompositionAttribute = self.user32.SetWindowCompositionAttribute
        self.SetWindowCompositionAttribute.restype = c_bool
        self.SetWindowCompositionAttribute.argtypes = [
            c_int,
            POINTER(WINDOWCOMPOSITIONATTRIBDATA),
        ]
        # 初始化结构体
        self.accentPolicy = ACCENT_POLICY()
        self.winCompAttrData = WINDOWCOMPOSITIONATTRIBDATA()
        self.winCompAttrData.Attribute = WINDOWCOMPOSITIONATTRIB.WCA_ACCENT_POLICY.value
        self.winCompAttrData.SizeOfData = sizeof(self.accentPolicy)
        self.winCompAttrData.Data = pointer(self.accentPolicy)
    
    def setAcrylicEffect(self, hWnd, gradientColor: str = "F2F2F230", isEnableShadow: bool = True, animationId: int = 0):
        """ 给窗口开启Win10的亚克力效果

        Parameter
        ----------
        hWnd: int or `sip.voidptr`
            窗口句柄

        gradientColor: str
            十六进制亚克力混合色，对应 RGBA 四个分量

        isEnableShadow: bool
            控制是否启用窗口阴影

        animationId: int
            控制磨砂动画
        """
        # 亚克力混合色
        gradientColor = (
            gradientColor[6:]
            + gradientColor[4:6]
            + gradientColor[2:4]
            + gradientColor[:2]
        )
        gradientColor = DWORD(int(gradientColor, base=16))
        # 磨砂动画
        animationId = DWORD(animationId)
        # 窗口阴影
        accentFlags = DWORD(0x20 | 0x40 | 0x80 |
                            0x100) if isEnableShadow else DWORD(0)
        self.accentPolicy.AccentState = ACCENT_STATE.ACCENT_ENABLE_ACRYLICBLURBEHIND.value
        self.accentPolicy.GradientColor = gradientColor
        self.accentPolicy.AccentFlags = accentFlags
        self.accentPolicy.AnimationId = animationId
        # 开启亚克力
        self.SetWindowCompositionAttribute(int(hWnd), pointer(self.winCompAttrData))

    def setAeroEffect(self, hWnd):
        """ 给窗口开启Aero效果

        Parameter
        ----------
        hWnd: int or `sip.voidptr`
            窗口句柄
        """
        self.accentPolicy.AccentState = ACCENT_STATE.ACCENT_ENABLE_BLURBEHIND.value
        # 开启Aero
        self.SetWindowCompositionAttribute(int(hWnd), pointer(self.winCompAttrData))
    
    def resetEffect(self, hWnd):
        """ 重置窗口背景
        
        """
        self.accentPolicy.AccentState = ACCENT_STATE.ACCENT_DISABLED.value
        self.SetWindowCompositionAttribute(int(hWnd), pointer(self.winCompAttrData))
