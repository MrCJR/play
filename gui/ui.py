import sys
import time
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QSlider, QLabel, QSizePolicy,
    QMessageBox
)
from PySide6.QtMultimedia import QMediaPlayer,QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from core.player import Player
from core.file import FileHandler
from PySide6.QtWidgets import QInputDialog


class PlayerUI(Player):
    """
    媒体播放器 UI, 负责界面布局和交互逻辑。
    """
    FPS_LIMIT = 1  # 每秒刷新一次 UI

    def __init__(self):
        super().__init__()
        self.file_handler = FileHandler()
        self.last_update_time = 0  # 限制进度更新频率的变量

        self.init_player()
        self.setup_ui()
        self.set_default_size()
        self.setWindowTitle("媒体播放器")
        self.connect_signals()

        # 添加音频输出对象
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)

    def setup_ui(self):
        """
        初始化 UI 界面，仅包含 UI 的组件初始化。
        """
        self.init_video_widget()
        self.init_controls()
        self.init_status_labels()
        self.init_layouts()

    def init_video_widget(self):
        """
        初始化视频组件。
        """
        self.video_widget = QVideoWidget()
        # 设置视频组件的大小策略为可扩展
        self.video_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.media_player.setVideoOutput(self.video_widget)


    def init_controls(self):
        """
        初始化按钮和滑块。
        """
        self.select_file_button = self.create_button("选择文件", self.open_file)
        self.play_button = self.create_button("暂停", self.toggle_play)
        self.volume_button = self.create_button("静音", self.toggle_mute)

        self.volume_slider = self.create_slider(0, 100, 50, self.set_volume)
        self.progress_slider = self.create_slider(0, 1000, 0)

        # 连接滑块的信号与槽函数
        self.progress_slider.sliderPressed.connect(self.slider_pressed)
        self.progress_slider.sliderReleased.connect(self.slider_released)
        self.progress_slider.sliderMoved.connect(self.update_label_preview)

    def init_status_labels(self):
        """
        初始化标签。
        """
        self.status_label = QLabel("未加载文件")
        self.current_file_label = QLabel("当前文件: 无")
        self.play_time_label = QLabel("播放时间: 00:00 / 00:00")

    def init_layouts(self):
        """
        初始化布局。
        """

        # 视频模块，包括视频播放和视频进度条，手动调整间距
        video_layout = self.create_layout(QVBoxLayout, self.video_widget, self.progress_slider, spacing=0,
                                          margins=(0, 0, 0, 0))

        # 声音模块，包含静音按钮和声音进度条
        volume_layout = self.create_layout(QHBoxLayout, self.volume_button, self.volume_slider)
        # 控制模块，包含选择文件按钮和播放暂停按钮
        controls_layout = self.create_layout(QHBoxLayout, self.select_file_button, self.play_button)
        # 状态模块，包含播放状态标签和播放时间标签，Qt.AlignmentFlag.AlignLeft设置左对齐
        labels_layout = self.create_layout(QHBoxLayout, self.status_label, self.play_time_label)
        labels_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # 主界面布局
        main_layout = QVBoxLayout()
        main_layout.addLayout(video_layout)
        main_layout.addLayout(volume_layout)
        main_layout.addLayout(controls_layout)
        main_layout.addLayout(labels_layout)

        self.setLayout(main_layout)

    @staticmethod
    def create_button(text, callback):
        """
        快速创建按钮并绑定点击事件。
        """
        button = QPushButton(text)
        button.clicked.connect(callback)
        return button

    @staticmethod
    def create_slider(min_value, max_value, initial_value, value_changed_callback=None):
        """
        快速创建滑块并绑定事件。
        """
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(min_value, max_value)
        slider.setValue(initial_value)
        if value_changed_callback:
            slider.valueChanged.connect(value_changed_callback)
        return slider

    @staticmethod
    def create_layout(layout_type, *widgets, spacing=10, margins=(0, 0, 0, 0)):
        """
        快速创建布局并添加控件。
        """
        layout = layout_type()
        layout.setSpacing(spacing)
        layout.setContentsMargins(*margins)
        for widget in widgets:
            layout.addWidget(widget)
        return layout

    def connect_signals(self):
        """
        连接播放器的信号与槽函数。
        """
        self.media_player.positionChanged.connect(self.update_slider)
        self.media_player.durationChanged.connect(self.set_slider_range)

    def toggle_play(self):
        """
        切换播放或暂停，并更新按钮文本。
        """
        super().toggle_play()
        is_playing = self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState

        # 根据播放状态更新播放按钮和播放状态的文本内容
        self.play_button.setText("暂停" if is_playing else "播放")
        self.status_label.setText("播放中" if is_playing else "已暂停")

    def set_volume(self, value):
        """
        设置音量大小，同时更新按钮状态和静音状态。
        """
        volume = value / 100.0  # 将百分比转换为 0-1 的值
        self.audio_output.setVolume(volume)

        # 当用户调整音量时，如果之前是静音状态，则取消静音
        if self.audio_output.isMuted() and value > 0:
            self.audio_output.setMuted(False)
            self.volume_button.setText("静音")

        # 当音量调到 0 时，自动设置为静音状态
        if value == 0:
            self.audio_output.setMuted(True)
            self.volume_button.setText("取消静音")
        elif not self.audio_output.isMuted():
            self.volume_button.setText("静音")

    def toggle_mute(self):
        """
        切换播放器静音状态，同时更新音量滑块的位置。
        """
        is_muted = self.audio_output.isMuted()
        self.audio_output.setMuted(not is_muted)

        if not is_muted:  # 即将静音
            # 保存当前音量值并设置滑块位置为0
            self._previous_volume = self.volume_slider.value()
            self.volume_slider.setValue(0)
        else:  # 取消静音
            # 恢复之前保存的音量值
            previous_volume = getattr(self, '_previous_volume', 50)
            self.volume_slider.setValue(previous_volume)

        self.volume_button.setText("取消静音" if not is_muted else "静音")

    def open_file(self):
        """
        打开文件选择对话框或输入流媒体 URL。
        """
        choice, ok = QInputDialog.getItem(self, "选择播放内容", "请选择:", ["本地文件", "流媒体 URL"], 0, False)
        if ok:
            if choice == "本地文件":
                # 通过实例对象调用 select_file 方法
                selected_file = self.file_handler.select_file()
            else:
                url, ok = QInputDialog.getText(self, "输入流媒体 URL", "请输入流媒体 URL:")
                if ok:
                    if not url.startswith(('http://', 'https://')):
                        QMessageBox.warning(self, "错误", "请输入有效的流媒体 URL。")
                        return
                    selected_file = url
                else:
                    return

            if not selected_file:
                return

            self.status_label.setText("加载中，请稍候...")
            QApplication.processEvents()
            self.play_file(selected_file)
            self.status_label.setText("播放中")
            self.current_file_label.setText(f"当前文件: {selected_file}")
        else:
            return

    def slider_pressed(self):
        """
        用户按下进度条，屏蔽播放器信号更新。
        """
        self.media_player.blockSignals(True)

    def slider_released(self):
        """
        用户释放进度条，更新进度位置。
        """
        self.media_player.blockSignals(False)
        position = self.progress_slider.value()
        duration = self.media_player.duration()
        if duration > 0:
            self.media_player.setPosition(position * duration // 1000)
        self.play_time_label.setStyleSheet("")  # 恢复原状

    def update_label_preview(self, value):
        """
        用户拖动进度条时，更新时间标签显示预览时间。
        """
        total_duration = self.media_player.duration()
        if total_duration > 0:
            preview_time = value * total_duration // 1000  # 将滑块值转换为时间戳
            current_time_str = self.format_time(preview_time // 1000)
            total_time_str = self.format_time(total_duration // 1000)
            self.play_time_label.setText(f"播放时间: {current_time_str} / {total_time_str}")
            self.play_time_label.setStyleSheet("color: red;")  # 设置高亮颜色

    def set_slider_range(self, duration):
        """
        根据视频的总时长设置进度条范围。
        """
        if duration > 0:
            self.progress_slider.setRange(0, 1000)  # 进度条范围保持不变
            total_time_str = self.format_time(duration // 1000)
            self.play_time_label.setText(f"播放时间: 00:00 / {total_time_str}")

    def update_slider(self, position):
        """
        更新进度条位置，限制更新频率。
        """
        current_time = time.time()
        if current_time - self.last_update_time < 1 / self.FPS_LIMIT:
            return

        self.last_update_time = current_time
        if not self.progress_slider.isSliderDown():
            duration = self.media_player.duration()
            if duration > 0:
                value = position * 1000 // duration
                self.progress_slider.setValue(value)

                # 更新时间标签
                current_time_str = self.format_time(position // 1000)
                total_time_str = self.format_time(duration // 1000)
                self.play_time_label.setText(f"播放时间: {current_time_str} / {total_time_str}")

    @staticmethod
    def format_time(seconds):
        """
        格式化时间为 mm:ss 格式。
        """
        minutes = seconds // 60
        seconds %= 60
        return f"{minutes:02}:{seconds:02}"

    def resizeEvent(self, event):
        """
        窗口大小调整时动态设置视频窗口高度。
        """
        super().resizeEvent(event)
        if self.video_widget and not event.oldSize().isEmpty():
            # 计算窗口的宽高比
            aspect_ratio = self.width() / self.height()
            if aspect_ratio > 16 / 9:  # 宽屏情况
                self.video_widget.setFixedHeight(int(self.height() * 0.8))
            else:  # 竖屏情况
                self.video_widget.setFixedHeight(int(self.height() * 0.6))

    def set_default_size(self):
        """
        设置默认窗口大小。
        """
        self.resize(800, 600)

    @staticmethod
    def create_app():
        """
        创建应用程序实例。
        """
        app = QApplication(sys.argv)
        app.setStyle("Fusion")
        player_ui = PlayerUI()
        return app, player_ui