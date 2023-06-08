import sys
import os

from packer import Info, RUNTIME_DIR, Runnable, Packer

import os.path
from base64 import b64encode
from pathlib import Path
from time import sleep

import flet as ft
from flet import *

create_button = ElevatedButton(
    text="创建",
    bgcolor="#227eff",
    color="white",
    right=0,
    bottom=31,
    icon="create"
)

icon = Image(
    visible=False,
    top=17,
    width=120,
    height=120,
    fit=ImageFit.CONTAIN,
    repeat=ft.ImageRepeat.NO_REPEAT,
    border_radius=ft.border_radius.all(10),
)

choice_button = ElevatedButton(
    text="选择",
    top=145,
    left=10,
    bgcolor="#227eff",
    color="white",
    icon="add"
)

app_name_input = TextField(
    label="App名称",
    border=InputBorder.UNDERLINE,
    border_width=1,
    cursor_color="grey",
    color="#404040"
)

app_location_input = TextField(
    label="生成位置",
    border=InputBorder.UNDERLINE,
    border_width=1,
    cursor_color="grey",
    color="#404040",
    hint_style=TextStyle(color="grey")
)
app_location_choose = FilledButton()

app_command_input = TextField(
    label="二进制文件执行指令",
    multiline=True,
    border=InputBorder.UNDERLINE,
    border_width=1,
    cursor_color="grey",
    color="#404040",
    max_lines=2,
    min_lines=2,
    hint_text="若要调用库请加上RUNTIME并添加该库，例：java -jar RUNTIME/Hello.jar",
    hint_style=TextStyle(color="grey")
)

version_input = TextField(
    label="版本",
    border=InputBorder.UNDERLINE,
    border_width=1,
    cursor_color="grey",
    color="#404040",
    hint_style=TextStyle(color="grey")
)

#
# if __name__ == '__main__':
#     info = Info()
#     info.add_icon('/Users/lqc/Desktop/swthello.icns')
#     runnable = Runnable()
#     runnable.set_command(f"java -XstartOnFirstThread -jar {RUNTIME_DIR}/SWTHello.jar")
#     runnable.add_libs(["/Users/lqc/Desktop/SWTHello.jar"])
#
#     Packer(app_path="/Users/lqc/Desktop", app_info=info).app_builder(runnable)
#
libs_area = TextField(
    label="依赖（一次性选完）",
    border=InputBorder.UNDERLINE,
    border_width=1,
    cursor_color="grey",
    color="#404040",
    hint_style=TextStyle(color="grey")
)

choice_libs_button = IconButton(
    top=268,
    left=4,
    width=46,
    height=46,
    bgcolor="#227eff",
    icon="add",
    icon_color="white"
)

icon_no = ft.TextButton("否")
icon_yes = ft.TextButton("是")

pb = ProgressBar(width=200, top=38)
pb_text = Text(top=10, size=16)
pb_cancel_button = ft.TextButton()

libs = []


class AppInfos(object):
    app_name: str = "null"
    app_location: str = "null"
    app_version: str = "null"
    app_command: str = "null"
    app_icon: str = "null"


app_info = AppInfos()


def app_builder():
    info: Info = Info(name=app_info.app_name, version=app_info.app_version)
    if app_info.app_icon != "default":
        info.add_icon(app_info.app_icon)
    packer: Packer = Packer(app_path=app_info.app_location, app_info=info)
    runnable: Runnable = Runnable()
    runnable.set_command(app_info.app_command)
    runnable.add_libs(libs)
    packer.app_builder(runnable=runnable)


def image_to_icns(src: str):
    if os.path.exists(src):
        tmp_path = "./resources/tmp.iconset/"
        src = src.replace("/Volumes/Macintosh HD", "")
        os.system(f"sips -z 16 16 {src} --out {tmp_path}icon_16x16.png\n"
                  f"sips -z 32 32 {src} --out {tmp_path}icon_16x16@2x.png\n"
                  f"sips -z 32 32 {src} --out {tmp_path}icon_32x32.png\n"
                  f"sips -z 64 64 {src} --out {tmp_path}icon_32x32@2x.png\n"
                  f"sips -z 128 128 {src} --out {tmp_path}icon_128x128.png\n"
                  f"sips -z 256 256 {src} --out {tmp_path}icon_128x128@2x.png\n"
                  f"sips -z 256 256 {src} --out {tmp_path}icon_256x256.png\n"
                  f"sips -z 512 512 {src} --out {tmp_path}icon_256x256@2x.png\n"
                  f"sips -z 512 512 {src} --out {tmp_path}icon_512x512.png\n"
                  f"sips -z 1024 1024 {src} --out {tmp_path}/icon_512x512@2x.png\n")
        index = len(os.listdir('./resources/cache'))
        os.system("iconutil -c icns ./resources/tmp.iconset -o "
                  f"./resources/cache/logo{index}.icns")
        app_info.app_icon = os.path.abspath(f"./logo{index}.icns")


def image_to_base64(page: Page, image: str, to_icns: bool = False):
    if os.path.basename(image) == "example.png":
        app_info.app_icon = "default"
    else:
        if not to_icns:
            app_info.app_icon = image
        else:
            image_to_icns(src=image)
    with open(image, "rb") as r:
        icon.src_base64 = b64encode(r.read()).decode("utf-8")
        icon.visible = True
        page.update()


def main(page: Page):
    def create_modal():
        pb.value = 0
        if len(libs) > 0 and app_info.app_name != "null" and app_info.app_location != "null" \
                and app_info.app_version != "null" and app_info.app_command != "null" and app_info.app_icon != "null":
            pb_cancel_button.text = "取消"
            pb_text.value = "创建中..."
            page.dialog = creator_modal
            pb.visible = True
            creator_modal.open = True
            page.update()
            return True
        else:
            pb_cancel_button.text = "确定"
            pb_text.value = "请完善App信息"
            pb.visible = False
            page.dialog = creator_modal
            creator_modal.open = True
            page.update()
            return False

    def create_app(e):
        if create_modal():
            sleep(0.65)
            for i in range(0, 31):
                sleep(0.005)
                pb.value = i * 0.04
                if i == 30:
                    pb_text.value = "创建完成！"
                    pb_cancel_button.text = "关闭"
                page.update()
            app_builder()

    def close_creator_modal(e):
        creator_modal.open = False
        page.update()

    pb_cancel_button.on_click = close_creator_modal

    creator_modal = ft.AlertDialog(
        modal=True,
        content=ft.Stack([pb_text, pb], height=40),
        actions=[
            pb_cancel_button
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda e: print("Modal dialog dismissed!"),
    )

    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("图标格式不正确"),
        content=ft.Text("需要在生成时转成icns吗？"),
        actions=[
            icon_yes,
            icon_no
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda e: print("Modal dialog dismissed!"),
    )

    page.dialog = dlg_modal

    def choose_icon(e: FilePickerResultEvent):
        def close_dialog(e1):
            dlg_modal.open = False
            image_to_base64(page, path, to_icns=True)
            page.update()

        def cancel(e2):
            image_to_base64(page, "./resources/example.png")
            dlg_modal.open = False
            page.update()

        icon_yes.on_click = close_dialog
        icon_no.on_click = cancel
        page.dialog = dlg_modal
        if e.files is not None:
            suffix = Path(os.path.basename(e.files[0].path)).suffix
            path = e.files[0].path
            if suffix != ".icns":
                dlg_modal.open = True
                page.update()
            else:
                image_to_base64(page, path)

    def choose_libs(e: FilePickerResultEvent):
        if e.files is not None:
            result: list = e.files
            for i in result:
                libs.append(i.path.replace("/Volumes/Macintosh HD", ""))
            libs_area.value = ""
            for x in libs:
                libs_area.value += f"\"{x}\" "
            # libs_input.label_style = TextStyle(color="#6d6d6d", size=12)
            page.update()

    page.window_title_bar_hidden = True
    page.window_width = 300
    page.window_height = 420
    page.bgcolor = "#f3f3f3"
    page.theme_mode = "light"
    page.window_resizable = False
    # page.window_resizable = False
    page.window_center()

    icon_picker = FilePicker(on_result=choose_icon)
    libs_picker = FilePicker(on_result=choose_libs)

    page.overlay.append(icon_picker)
    page.overlay.append(libs_picker)
    image_to_base64(page, "./resources/example.png")
    create_button.on_click = create_app
    choice_button.on_click = \
        lambda x: icon_picker.pick_files(allow_multiple=False,
                                         allowed_extensions=["icns",
                                                             "png",
                                                             "jpg",
                                                             "jpeg"])
    choice_libs_button.on_click = lambda x: libs_picker.pick_files(allow_multiple=True)

    def app_name_onchange(e):
        app_info.app_name = e.control.value

    def app_location_onchange(e):
        app_info.app_location = e.control.value

    def app_version_onchange(e):
        app_info.app_version = e.control.value

    def app_command_onchange(e):
        app_info.app_command = str(e.control.value).replace("RUNTIME", RUNTIME_DIR)
        # java -XstartOnFirstThread -jar /Users/lqc/Desktop/SWTHello.jar

    app_name_input.on_change = app_name_onchange
    app_location_input.on_change = app_location_onchange
    version_input.on_change = app_version_onchange
    app_command_input.on_change = app_command_onchange
    page.add(
        ft.Stack(
            [create_button, icon, choice_button,
             Container(
                 content=app_name_input,
                 width=150,
                 height=60,
                 top=10,
                 right=0,
             ),
             Container(
                 content=app_location_input,
                 width=150,
                 height=60,
                 top=70,
                 right=0,
             ),
             Container(
                 content=version_input,
                 width=150,
                 height=60,
                 top=130,
                 right=0,
             ),
             Container(
                 content=app_command_input,
                 width=280,
                 height=82,
                 top=175,
                 left=0
             ),
             choice_libs_button,
             Container(
                 content=libs_area,
                 width=220,
                 height=54,
                 top=258,
                 right=0
             )],
            width=300,
            height=400,
        )
    )
    page.update()


if __name__ == '__main__':
    ft.app(target=main)
