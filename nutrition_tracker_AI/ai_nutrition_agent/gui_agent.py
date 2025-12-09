"""
GUI Version - Intelligent Nutrition Analysis System
One-click image selection, automatically complete all analysis steps
"""
import os
import sys
import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk
from datetime import datetime
import threading

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from agent import NutritionAgent


class NutritionAnalyzerGUI:
    """Nutrition Analysis System GUI"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🍽️ Intelligent Nutrition Analysis System")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f0")
        
        # Initialize Agent
        self.agent = None
        self.analyzing = False
        
        self.setup_ui()
        self.init_agent()
    
    def setup_ui(self):
        """Setup UI layout"""
        # Title area
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="🍽️ Intelligent Nutrition Analysis System",
            font=("Arial", 24, "bold"),
            fg="white",
            bg="#2c3e50"
        )
        title_label.pack(expand=True)
        
        subtitle_label = tk.Label(
            title_frame,
            text="Based on LangChain 1.0 + Alibaba Qwen",
            font=("Arial", 10),
            fg="#ecf0f1",
            bg="#2c3e50"
        )
        subtitle_label.pack()
        
        # Main operation area
        main_frame = tk.Frame(self.root, bg="#f0f0f0", pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        # Image selection area
        image_frame = tk.Frame(main_frame, bg="#ffffff", relief=tk.RAISED, borderwidth=2)
        image_frame.pack(fill=tk.X, pady=(0, 20))
        
        image_label = tk.Label(
            image_frame,
            text="📸 Select Meal Image",
            font=("Arial", 14, "bold"),
            bg="#ffffff",
            pady=10
        )
        image_label.pack()
        
        # Select image button
        self.select_button = tk.Button(
            image_frame,
            text="🖼️ Select Image and Start Analysis",
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
        
        # Meal type selection
        meal_type_frame = tk.Frame(image_frame, bg="#ffffff")
        meal_type_frame.pack(pady=(0, 15))
        
        tk.Label(
            meal_type_frame,
            text="Meal Type: ",
            font=("Arial", 11),
            bg="#ffffff"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.meal_type_var = tk.StringVar(value="Lunch")
        meal_types = ["Breakfast", "Lunch", "Dinner", "Snack"]
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
        
        # Image path display
        self.image_path_label = tk.Label(
            image_frame,
            text="No image selected",
            font=("Arial", 10),
            fg="#7f8c8d",
            bg="#ffffff",
            pady=5
        )
        self.image_path_label.pack()
        
        # Progress bar
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
        
        # Result display area
        result_frame = tk.Frame(main_frame, bg="#ffffff", relief=tk.RAISED, borderwidth=2)
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        result_title = tk.Label(
            result_frame,
            text="📊 Analysis Results",
            font=("Arial", 14, "bold"),
            bg="#ffffff",
            pady=10
        )
        result_title.pack()
        
        # Result text area (scrollable)
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
        
        # Status bar
        status_frame = tk.Frame(self.root, bg="#34495e", height=30)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready",
            font=("Arial", 9),
            fg="white",
            bg="#34495e",
            anchor=tk.W,
            padx=10
        )
        self.status_label.pack(fill=tk.X)
    
    def init_agent(self):
        """Initialize Agent (asynchronous)"""
        def _init():
            try:
                self.update_status("Initializing Agent...")
                self.agent = NutritionAgent()
                self.update_status("✅ Agent initialization complete! Ready")
                self.log_result("✅ System initialization successful!\n\nPlease click the button to select a meal image to start analysis.\n")
            except Exception as e:
                self.update_status(f"❌ Initialization failed: {str(e)}")
                self.log_result(f"❌ Initialization error:\n{str(e)}\n\nPlease check configuration and network connection.")
        
        threading.Thread(target=_init, daemon=True).start()
    
    def select_and_analyze(self):
        """Select image and analyze automatically"""
        if self.analyzing:
            return
        
        if not self.agent:
            self.log_result("❌ Agent not yet initialized, please wait...\n")
            return
        
        # Open file selection dialog
        file_path = filedialog.askopenfilename(
            title="Select Meal Image",
            filetypes=[
                ("Image Files", "*.jpg *.jpeg *.png *.bmp *.gif"),
                ("All Files", "*.*")
            ]
        )
        
        if not file_path:
            return  # User canceled selection
        
        # Display selected file
        self.image_path_label.config(
            text=f"Selected: {os.path.basename(file_path)}",
            fg="#27ae60"
        )
        
        # Start analysis
        meal_type = self.meal_type_var.get()
        self.start_analysis(file_path, meal_type)
    
    def start_analysis(self, image_path: str, meal_type: str):
        """Start analysis (asynchronous)"""
        if self.analyzing:
            return
        
        self.analyzing = True
        self.select_button.config(state=tk.DISABLED, bg="#95a5a6")
        self.result_text.delete(1.0, tk.END)
        
        # Show progress bar
        self.progress_label.config(text="🔄 Analyzing, please wait...")
        self.progress_bar.pack(pady=5)
        self.progress_bar.start(10)
        
        def _analyze():
            try:
                self.update_status(f"Analyzing {meal_type}...")
                
                # Record start time
                start_time = datetime.now()
                self.log_result(f"{'='*60}\n")
                self.log_result(f"🍽️  Starting Analysis: {meal_type}\n")
                self.log_result(f"📸 Image: {os.path.basename(image_path)}\n")
                self.log_result(f"⏰ Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                self.log_result(f"{'='*60}\n\n")
                
                self.log_result("🔄 Agent is executing the following steps:\n")
                self.log_result("  1️⃣  Image Recognition (Qwen-VL)\n")
                self.log_result("  2️⃣  Portion Verification\n")
                self.log_result("  3️⃣  Nutrition Query\n")
                self.log_result("  4️⃣  Nutrition Calculation\n")
                self.log_result("  5️⃣  Health Scoring\n")
                self.log_result("  6️⃣  Trend Analysis\n")
                self.log_result("  7️⃣  Next Meal Recommendation\n")
                self.log_result("  8️⃣  Save Data\n\n")
                
                # Execute analysis
                result = self.agent.analyze_meal(image_path, meal_type)
                
                # Calculate duration
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                
                # Display results
                self.log_result(f"\n{'='*60}\n")
                self.log_result(f"✅ Analysis complete!\n")
                self.log_result(f"⏱️  Duration: {duration:.2f} seconds\n")
                self.log_result(f"{'='*60}\n\n")
                
                # Display Agent's output
                if "messages" in result:
                    # Extract last message (Agent's final reply)
                    messages = result["messages"]
                    if messages:
                        final_message = messages[-1]
                        if hasattr(final_message, 'content'):
                            self.log_result("📊 Analysis Report:\n\n")
                            self.log_result(final_message.content)
                        else:
                            self.log_result(str(final_message))
                else:
                    self.log_result(str(result))
                
                self.update_status(f"✅ Analysis complete! Duration {duration:.2f} seconds")
                
            except Exception as e:
                self.log_result(f"\n❌ Error during analysis:\n")
                self.log_result(f"{str(e)}\n")
                self.update_status(f"❌ Analysis failed: {str(e)}")
            
            finally:
                # Restore UI state
                self.root.after(0, self._finish_analysis)
        
        # Execute in background thread
        threading.Thread(target=_analyze, daemon=True).start()
    
    def _finish_analysis(self):
        """Restore UI after analysis completion"""
        self.analyzing = False
        self.select_button.config(state=tk.NORMAL, bg="#3498db")
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        self.progress_label.config(text="")
    
    def log_result(self, message: str):
        """Add log to result area"""
        self.result_text.insert(tk.END, message)
        self.result_text.see(tk.END)
        self.root.update_idletasks()
    
    def update_status(self, message: str):
        """Update status bar"""
        self.status_label.config(text=message)
        self.root.update_idletasks()


def main():
    """Main function"""
    root = tk.Tk()
    app = NutritionAnalyzerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
