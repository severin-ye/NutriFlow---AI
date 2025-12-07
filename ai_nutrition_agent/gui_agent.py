"""
图形界面版本 - 智能营养分析系统
一键选择图片，自动完成所有分析步骤
"""
import os
import sys
import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk
from datetime import datetime
import threading

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from agent import NutritionAgent


class NutritionAnalyzerGUI:
    """营养分析系统图形界面"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🍽️ 智能营养分析系统")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f0")
        
        # 初始化Agent
        self.agent = None
        self.analyzing = False
        
        self.setup_ui()
        self.init_agent()
    
    def setup_ui(self):
        """设置界面布局"""
        # 标题区域
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="🍽️ 智能营养分析系统",
            font=("Arial", 24, "bold"),
            fg="white",
            bg="#2c3e50"
        )
        title_label.pack(expand=True)
        
        subtitle_label = tk.Label(
            title_frame,
            text="基于 LangChain 1.0 + 阿里通义千问",
            font=("Arial", 10),
            fg="#ecf0f1",
            bg="#2c3e50"
        )
        subtitle_label.pack()
        
        # 主操作区域
        main_frame = tk.Frame(self.root, bg="#f0f0f0", pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        # 图片选择区域
        image_frame = tk.Frame(main_frame, bg="#ffffff", relief=tk.RAISED, borderwidth=2)
        image_frame.pack(fill=tk.X, pady=(0, 20))
        
        image_label = tk.Label(
            image_frame,
            text="📸 选择餐盘图片",
            font=("Arial", 14, "bold"),
            bg="#ffffff",
            pady=10
        )
        image_label.pack()
        
        # 选择图片按钮
        self.select_button = tk.Button(
            image_frame,
            text="🖼️ 选择图片并开始分析",
            font=("Arial", 14, "bold"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            relief=tk.RAISED,
            borderwidth=3,
            padx=30,
            pady=15,
            cursor="hand2",
            command=self.select_and_analyze
        )
        self.select_button.pack(pady=20)
        
        # 餐型选择
        meal_type_frame = tk.Frame(image_frame, bg="#ffffff")
        meal_type_frame.pack(pady=(0, 15))
        
        tk.Label(
            meal_type_frame,
            text="餐型: ",
            font=("Arial", 11),
            bg="#ffffff"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.meal_type_var = tk.StringVar(value="午餐")
        meal_types = ["早餐", "午餐", "晚餐", "加餐"]
        for meal_type in meal_types:
            tk.Radiobutton(
                meal_type_frame,
                text=meal_type,
                variable=self.meal_type_var,
                value=meal_type,
                font=("Arial", 10),
                bg="#ffffff",
                activebackground="#ffffff"
            ).pack(side=tk.LEFT, padx=5)
        
        # 图片路径显示
        self.image_path_label = tk.Label(
            image_frame,
            text="未选择图片",
            font=("Arial", 10),
            fg="#7f8c8d",
            bg="#ffffff",
            pady=5
        )
        self.image_path_label.pack()
        
        # 进度条
        self.progress_frame = tk.Frame(main_frame, bg="#f0f0f0")
        self.progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.progress_label = tk.Label(
            self.progress_frame,
            text="",
            font=("Arial", 10),
            fg="#2c3e50",
            bg="#f0f0f0"
        )
        self.progress_label.pack()
        
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            mode='indeterminate',
            length=400
        )
        
        # 结果显示区域
        result_frame = tk.Frame(main_frame, bg="#ffffff", relief=tk.RAISED, borderwidth=2)
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        result_title = tk.Label(
            result_frame,
            text="📊 分析结果",
            font=("Arial", 14, "bold"),
            bg="#ffffff",
            pady=10
        )
        result_title.pack()
        
        # 结果文本区域（支持滚动）
        self.result_text = scrolledtext.ScrolledText(
            result_frame,
            font=("Consolas", 10),
            wrap=tk.WORD,
            bg="#f8f9fa",
            fg="#2c3e50",
            padx=15,
            pady=15,
            relief=tk.FLAT
        )
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # 状态栏
        status_frame = tk.Frame(self.root, bg="#34495e", height=30)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame,
            text="准备就绪",
            font=("Arial", 9),
            fg="white",
            bg="#34495e",
            anchor=tk.W,
            padx=10
        )
        self.status_label.pack(fill=tk.X)
    
    def init_agent(self):
        """初始化Agent（异步）"""
        def _init():
            try:
                self.update_status("正在初始化 Agent...")
                self.agent = NutritionAgent()
                self.update_status("✅ Agent 初始化完成！准备就绪")
                self.log_result("✅ 系统初始化成功！\n\n请点击按钮选择餐盘图片开始分析。\n")
            except Exception as e:
                self.update_status(f"❌ 初始化失败: {str(e)}")
                self.log_result(f"❌ 初始化错误:\n{str(e)}\n\n请检查配置和网络连接。")
        
        threading.Thread(target=_init, daemon=True).start()
    
    def select_and_analyze(self):
        """选择图片并自动分析"""
        if self.analyzing:
            return
        
        if not self.agent:
            self.log_result("❌ Agent 尚未初始化完成，请稍候...\n")
            return
        
        # 打开文件选择对话框
        file_path = filedialog.askopenfilename(
            title="选择餐盘图片",
            filetypes=[
                ("图片文件", "*.jpg *.jpeg *.png *.bmp *.gif"),
                ("所有文件", "*.*")
            ]
        )
        
        if not file_path:
            return  # 用户取消选择
        
        # 显示选择的文件
        self.image_path_label.config(
            text=f"已选择: {os.path.basename(file_path)}",
            fg="#27ae60"
        )
        
        # 开始分析
        meal_type = self.meal_type_var.get()
        self.start_analysis(file_path, meal_type)
    
    def start_analysis(self, image_path: str, meal_type: str):
        """开始分析（异步）"""
        if self.analyzing:
            return
        
        self.analyzing = True
        self.select_button.config(state=tk.DISABLED, bg="#95a5a6")
        self.result_text.delete(1.0, tk.END)
        
        # 显示进度条
        self.progress_label.config(text="🔄 正在分析中，请稍候...")
        self.progress_bar.pack(pady=5)
        self.progress_bar.start(10)
        
        def _analyze():
            try:
                self.update_status(f"正在分析 {meal_type}...")
                
                # 记录开始时间
                start_time = datetime.now()
                self.log_result(f"{'='*60}\n")
                self.log_result(f"🍽️  开始分析: {meal_type}\n")
                self.log_result(f"📸 图片: {os.path.basename(image_path)}\n")
                self.log_result(f"⏰ 时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                self.log_result(f"{'='*60}\n\n")
                
                self.log_result("🔄 Agent 正在执行以下步骤:\n")
                self.log_result("  1️⃣  图像识别 (Qwen-VL)\n")
                self.log_result("  2️⃣  分量验证\n")
                self.log_result("  3️⃣  营养查询\n")
                self.log_result("  4️⃣  营养计算\n")
                self.log_result("  5️⃣  健康评分\n")
                self.log_result("  6️⃣  趋势分析\n")
                self.log_result("  7️⃣  下一餐推荐\n")
                self.log_result("  8️⃣  保存数据\n\n")
                
                # 执行分析
                result = self.agent.analyze_meal(image_path, meal_type)
                
                # 计算耗时
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                
                # 显示结果
                self.log_result(f"\n{'='*60}\n")
                self.log_result(f"✅ 分析完成！\n")
                self.log_result(f"⏱️  耗时: {duration:.2f} 秒\n")
                self.log_result(f"{'='*60}\n\n")
                
                # 显示Agent的输出
                if "messages" in result:
                    # 提取最后一条消息（Agent的最终回复）
                    messages = result["messages"]
                    if messages:
                        final_message = messages[-1]
                        if hasattr(final_message, 'content'):
                            self.log_result("📊 分析报告:\n\n")
                            self.log_result(final_message.content)
                        else:
                            self.log_result(str(final_message))
                else:
                    self.log_result(str(result))
                
                self.update_status(f"✅ 分析完成！耗时 {duration:.2f} 秒")
                
            except Exception as e:
                self.log_result(f"\n❌ 分析过程中出现错误:\n")
                self.log_result(f"{str(e)}\n")
                self.update_status(f"❌ 分析失败: {str(e)}")
            
            finally:
                # 恢复界面状态
                self.root.after(0, self._finish_analysis)
        
        # 在后台线程中执行
        threading.Thread(target=_analyze, daemon=True).start()
    
    def _finish_analysis(self):
        """完成分析后的界面恢复"""
        self.analyzing = False
        self.select_button.config(state=tk.NORMAL, bg="#3498db")
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        self.progress_label.config(text="")
    
    def log_result(self, message: str):
        """添加日志到结果区域"""
        self.result_text.insert(tk.END, message)
        self.result_text.see(tk.END)
        self.root.update_idletasks()
    
    def update_status(self, message: str):
        """更新状态栏"""
        self.status_label.config(text=message)
        self.root.update_idletasks()


def main():
    """主函数"""
    root = tk.Tk()
    app = NutritionAnalyzerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
