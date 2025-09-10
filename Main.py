import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, font
from datetime import datetime, timedelta
import json
import random
from collections import defaultdict, Counter
import re

class TimetableGenerator:
    def __init__(self):
        self.schedule = {}
    
    def create_timetable(self, subjects, study_hours_per_day=6, days=7):
        """Generate a study timetable"""
        timetable = {}
        subjects_cycle = subjects * ((study_hours_per_day * days) // len(subjects) + 1)
        
        for day in range(days):
            day_name = (datetime.now() + timedelta(days=day)).strftime("%A")
            daily_schedule = []
            start_time = 9  # 9 AM start
            
            for hour in range(study_hours_per_day):
                subject = subjects_cycle[(day * study_hours_per_day + hour) % len(subjects_cycle)]
                time_slot = f"{start_time + hour}:00 - {start_time + hour + 1}:00"
                daily_schedule.append(f"{time_slot}: {subject}")
            
            timetable[day_name] = daily_schedule
        
        self.schedule = timetable
        return timetable

class TextSummarizer:
    def __init__(self):
        pass
    
    def summarize(self, text, max_sentences=3):
        """Simple extractive text summarization"""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) <= max_sentences:
            return text
        
        # Score sentences by word frequency
        word_freq = Counter()
        for sentence in sentences:
            words = re.findall(r'\w+', sentence.lower())
            word_freq.update(words)
        
        sentence_scores = {}
        for sentence in sentences:
            words = re.findall(r'\w+', sentence.lower())
            score = sum(word_freq[word] for word in words)
            sentence_scores[sentence] = score
        
        # Get top sentences
        top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:max_sentences]
        summary = '. '.join([sentence for sentence, _ in top_sentences])
        
        return summary + '.'

class QuizManager:
    def __init__(self):
        self.quizzes = {
            "Data Structures": [
                {"question": "What is the time complexity of accessing an element in an array?", "options": ["O(1)", "O(n)", "O(log n)", "O(n^2)"], "answer": 0},
                {"question": "Which data structure uses LIFO?", "options": ["Queue", "Stack", "Array", "Linked List"], "answer": 1},
                {"question": "What is the best case time complexity of Binary Search?", "options": ["O(1)", "O(log n)", "O(n)", "O(n log n)"], "answer": 0},
                {"question": "Which data structure is used to implement recursion?", "options": ["Queue", "Stack", "Tree", "Graph"], "answer": 1},
                {"question": "What is the space complexity of a complete binary tree with n nodes?", "options": ["O(1)", "O(log n)", "O(n)", "O(n^2)"], "answer": 2},
                {"question": "Which operation is NOT efficient in an array?", "options": ["Access", "Search", "Insertion at beginning", "Random access"], "answer": 2},
            ],
            "Algorithms": [
                {"question": "What is the worst-case time complexity of Quick Sort?", "options": ["O(n)", "O(n log n)", "O(n^2)", "O(log n)"], "answer": 2},
                {"question": "Which algorithm is used for finding the shortest path in a graph?", "options": ["Dijkstra's Algorithm", "Bubble Sort", "Merge Sort", "Binary Search"], "answer": 0},
                {"question": "What is the time complexity of Merge Sort?", "options": ["O(n)", "O(n log n)", "O(n^2)", "O(log n)"], "answer": 1},
                {"question": "Which sorting algorithm is stable?", "options": ["Quick Sort", "Selection Sort", "Merge Sort", "Heap Sort"], "answer": 2},
                {"question": "What is the best case time complexity of Bubble Sort?", "options": ["O(1)", "O(n)", "O(n log n)", "O(n^2)"], "answer": 1},
                {"question": "Which algorithm uses divide and conquer approach?", "options": ["Linear Search", "Bubble Sort", "Binary Search", "Selection Sort"], "answer": 2},
            ],
            "Operating Systems": [
                {"question": "What is the main function of an operating system?", "options": ["Manage hardware", "Run applications", "Provide security", "All of the above"], "answer": 3},
                {"question": "What does CPU stand for?", "options": ["Central Processing Unit", "Computer Personal Unit", "Central Program Unit", "Control Processing Unit"], "answer": 0},
                {"question": "Which scheduling algorithm gives the minimum average waiting time?", "options": ["FCFS", "SJF", "Round Robin", "Priority"], "answer": 1},
                {"question": "What is a deadlock?", "options": ["Process termination", "Memory overflow", "Circular wait condition", "CPU overload"], "answer": 2},
                {"question": "Which memory management technique uses fixed-size blocks?", "options": ["Paging", "Segmentation", "Virtual Memory", "Cache"], "answer": 0},
                {"question": "What is the purpose of system calls?", "options": ["Interface between user and kernel", "Memory allocation", "Process scheduling", "File management"], "answer": 0},
            ],
            "Database Management": [
                {"question": "What does ACID stand for in database transactions?", "options": ["Atomicity, Consistency, Isolation, Durability", "Access, Control, Integration, Data", "Automated, Centralized, Integrated, Distributed", "None of the above"], "answer": 0},
                {"question": "Which is NOT a type of database relationship?", "options": ["One-to-One", "One-to-Many", "Many-to-Many", "All-to-All"], "answer": 3},
                {"question": "What is normalization in databases?", "options": ["Data encryption", "Reducing data redundancy", "Increasing storage", "Data backup"], "answer": 1},
                {"question": "Which SQL command is used to retrieve data?", "options": ["INSERT", "UPDATE", "SELECT", "DELETE"], "answer": 2},
                {"question": "What is a primary key?", "options": ["First column in table", "Unique identifier for records", "Most important column", "Encrypted field"], "answer": 1},
                {"question": "Which normal form eliminates transitive dependencies?", "options": ["1NF", "2NF", "3NF", "BCNF"], "answer": 2},
            ],
            "Computer Networks": [
                {"question": "What layer of OSI model does HTTP operate at?", "options": ["Physical", "Network", "Transport", "Application"], "answer": 3},
                {"question": "What is the default port number for HTTP?", "options": ["21", "22", "80", "443"], "answer": 2},
                {"question": "Which protocol is used for secure web browsing?", "options": ["HTTP", "HTTPS", "FTP", "SMTP"], "answer": 1},
                {"question": "What does TCP stand for?", "options": ["Transmission Control Protocol", "Transfer Control Program", "Terminal Control Process", "Text Control Protocol"], "answer": 0},
                {"question": "Which device operates at the Network layer?", "options": ["Hub", "Switch", "Router", "Repeater"], "answer": 2},
                {"question": "What is the purpose of DNS?", "options": ["Data encryption", "Domain name resolution", "Data compression", "Network security"], "answer": 1},
            ],
            "Software Engineering": [
                {"question": "Which is NOT a software development life cycle model?", "options": ["Waterfall", "Agile", "Spiral", "Linear"], "answer": 3},
                {"question": "What is the main goal of software testing?", "options": ["Find bugs", "Improve performance", "Reduce cost", "All of the above"], "answer": 0},
                {"question": "Which testing approach tests individual components?", "options": ["Integration testing", "System testing", "Unit testing", "Acceptance testing"], "answer": 2},
                {"question": "What does UML stand for?", "options": ["Universal Modeling Language", "Unified Modeling Language", "User Modeling Language", "Unique Modeling Language"], "answer": 1},
                {"question": "Which is a functional requirement?", "options": ["Performance", "Security", "User login", "Scalability"], "answer": 2},
                {"question": "What is version control used for?", "options": ["Track code changes", "Compile code", "Test code", "Deploy code"], "answer": 0},
            ],
            "Machine Learning": [
                {"question": "Which is a supervised learning algorithm?", "options": ["K-means", "Linear Regression", "DBSCAN", "PCA"], "answer": 1},
                {"question": "What is overfitting?", "options": ["Model performs well on training data but poorly on test data", "Model performs poorly on both training and test data", "Model takes too long to train", "Model uses too much memory"], "answer": 0},
                {"question": "Which activation function is commonly used in neural networks?", "options": ["Linear", "ReLU", "Polynomial", "Exponential"], "answer": 1},
                {"question": "What is the purpose of cross-validation?", "options": ["Increase training speed", "Evaluate model performance", "Reduce overfitting", "Both B and C"], "answer": 3},
                {"question": "Which algorithm is used for dimensionality reduction?", "options": ["SVM", "PCA", "K-NN", "Decision Tree"], "answer": 1},
                {"question": "What type of learning is reinforcement learning?", "options": ["Supervised", "Unsupervised", "Semi-supervised", "Learning through trial and error"], "answer": 3},
            ],
            "Web Development": [
                {"question": "Which is NOT a front-end technology?", "options": ["HTML", "CSS", "JavaScript", "MySQL"], "answer": 3},
                {"question": "What does CSS stand for?", "options": ["Computer Style Sheets", "Cascading Style Sheets", "Creative Style Sheets", "Colorful Style Sheets"], "answer": 1},
                {"question": "Which HTTP method is used to submit form data?", "options": ["GET", "POST", "PUT", "DELETE"], "answer": 1},
                {"question": "What is responsive web design?", "options": ["Fast loading websites", "Websites that adapt to different screen sizes", "Interactive websites", "Secure websites"], "answer": 1},
                {"question": "Which is a popular JavaScript framework?", "options": ["Django", "Flask", "React", "Laravel"], "answer": 2},
                {"question": "What is the purpose of AJAX?", "options": ["Style web pages", "Create databases", "Make asynchronous requests", "Secure websites"], "answer": 2},
            ]
        }

    def get_quiz(self, subject, num_questions=3):
        """Get a random quiz for a subject"""
        if subject not in self.quizzes:
            return []
        
        questions = random.sample(self.quizzes[subject], min(num_questions, len(self.quizzes[subject])))
        return questions
    
    def add_question(self, subject, question, options, correct_answer_index):
        """Add a new question to a subject"""
        if subject not in self.quizzes:
            self.quizzes[subject] = []
        
        self.quizzes[subject].append({
            "question": question,
            "options": options,
            "answer": correct_answer_index
        })

class PerformanceTracker:
    def __init__(self):
        self.scores = defaultdict(list)
        self.study_time = defaultdict(int)
    
    def record_quiz_score(self, subject, score, total):
        """Record quiz performance"""
        percentage = (score / total) * 100
        self.scores[subject].append(percentage)
    
    def record_study_time(self, subject, minutes):
        """Record study time in minutes"""
        self.study_time[subject] += minutes
    
    def get_performance_summary(self):
        """Get overall performance summary"""
        summary = {}
        
        for subject in self.scores:
            avg_score = sum(self.scores[subject]) / len(self.scores[subject])
            total_time = self.study_time[subject]
            summary[subject] = {
                "average_score": round(avg_score, 2),
                "total_study_time": total_time,
                "quiz_attempts": len(self.scores[subject])
            }
        
        return summary

class StudyAssistantChatbot:
    def __init__(self):
        self.timetable_gen = TimetableGenerator()
        self.summarizer = TextSummarizer()
        self.quiz_manager = QuizManager()
        self.performance_tracker = PerformanceTracker()
        
        # Color scheme
        self.colors = {
            'primary': '#2E86C1',      # Blue
            'secondary': '#28B463',     # Green
            'accent': '#F39C12',        # Orange
            'danger': '#E74C3C',        # Red
            'success': '#27AE60',       # Dark Green
            'warning': '#F1C40F',       # Yellow
            'dark': '#34495E',          # Dark Blue Gray
            'light': '#ECF0F1',         # Light Gray
            'white': '#FFFFFF',
            'purple': '#8E44AD',
            'pink': '#E91E63',
            'teal': '#1ABC9C'
        }
        
        # Initialize GUI
        self.root = tk.Tk()
        self.root.title("🎓 Intelligent Study Assistant Pro")
        self.root.geometry("1000x700")
        self.root.configure(bg=self.colors['light'])
        
        # Set up modern styling
        self.setup_styles()
        self.setup_gui()
    
    def setup_styles(self):
        """Setup modern styling for the application"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure notebook style
        style.configure('TNotebook', background=self.colors['light'])
        style.configure('TNotebook.Tab', 
                       background=self.colors['primary'],
                       foreground='white',
                       padding=[20, 10],
                       font=('Helvetica', 10, 'bold'))
        style.map('TNotebook.Tab',
                 background=[('selected', self.colors['secondary'])],
                 foreground=[('selected', 'white')])
        
        # Configure button styles
        style.configure('Primary.TButton',
                       background=self.colors['primary'],
                       foreground='white',
                       font=('Helvetica', 10, 'bold'),
                       padding=[10, 5])
        style.map('Primary.TButton',
                 background=[('active', self.colors['dark'])])
        
        style.configure('Success.TButton',
                       background=self.colors['success'],
                       foreground='white',
                       font=('Helvetica', 10, 'bold'),
                       padding=[10, 5])
        
        style.configure('Warning.TButton',
                       background=self.colors['warning'],
                       foreground='white',
                       font=('Helvetica', 10, 'bold'),
                       padding=[10, 5])
        
        # Configure frame styles
        style.configure('Card.TFrame',
                       background='white',
                       relief='raised',
                       borderwidth=2)
        
        # Configure labelframe styles
        style.configure('Card.TLabelframe',
                       background='white',
                       foreground=self.colors['dark'],
                       font=('Helvetica', 12, 'bold'))
    
    def setup_gui(self):
        """Setup the graphical user interface"""
        # Main header
        header_frame = tk.Frame(self.root, bg=self.colors['primary'], height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, 
                              text="🎓 Intelligent Study Assistant Pro",
                              font=('Helvetica', 20, 'bold'),
                              bg=self.colors['primary'],
                              fg='white')
        title_label.pack(expand=True)
        
        subtitle_label = tk.Label(header_frame,
                                 text="Your AI-Powered Learning Companion",
                                 font=('Helvetica', 12),
                                 bg=self.colors['primary'],
                                 fg=self.colors['light'])
        subtitle_label.pack()
        
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Chat Tab
        self.setup_chat_tab(notebook)
        
        # Timetable Tab
        self.setup_timetable_tab(notebook)
        
        # Summarizer Tab
        self.setup_summarizer_tab(notebook)
        
        # Quiz Tab
        self.setup_quiz_tab(notebook)
        
        # Dashboard Tab
        self.setup_dashboard_tab(notebook)
    
    def setup_chat_tab(self, notebook):
        """Setup main chat interface"""
        chat_frame = ttk.Frame(notebook)
        notebook.add(chat_frame, text="💬 Chat Assistant")
        
        # Create main container with gradient-like effect
        main_container = tk.Frame(chat_frame, bg='white')
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Chat display with custom styling
        chat_label = tk.Label(main_container, 
                             text="🤖 AI Study Assistant",
                             font=('Helvetica', 14, 'bold'),
                             bg='white',
                             fg=self.colors['primary'])
        chat_label.pack(pady=(10, 5))
        
        self.chat_display = scrolledtext.ScrolledText(main_container, 
                                                     height=18, 
                                                     width=80,
                                                     font=('Consolas', 11),
                                                     bg='#F8F9FA',
                                                     fg=self.colors['dark'],
                                                     wrap=tk.WORD,
                                                     relief='groove',
                                                     borderwidth=2)
        self.chat_display.pack(padx=10, pady=10, fill='both', expand=True)
        
        # Input frame with modern styling
        input_frame = tk.Frame(main_container, bg='white')
        input_frame.pack(fill='x', padx=10, pady=10)
        
        input_label = tk.Label(input_frame,
                              text="💭 Ask me anything:",
                              font=('Helvetica', 11, 'bold'),
                              bg='white',
                              fg=self.colors['dark'])
        input_label.pack(anchor='w')
        
        entry_frame = tk.Frame(input_frame, bg='white')
        entry_frame.pack(fill='x', pady=5)
        
        self.chat_input = tk.Entry(entry_frame,
                                  font=('Helvetica', 11),
                                  bg='white',
                                  fg=self.colors['dark'],
                                  relief='groove',
                                  borderwidth=2)
        self.chat_input.pack(side='left', fill='x', expand=True, padx=(0, 10))
        self.chat_input.bind('<Return>', self.process_chat_input)
        
        send_btn = tk.Button(entry_frame,
                            text="📤 Send",
                            font=('Helvetica', 10, 'bold'),
                            bg=self.colors['primary'],
                            fg='white',
                            relief='raised',
                            borderwidth=2,
                            command=self.process_chat_input)
        send_btn.pack(side='right')
        
        # Welcome message
        self.add_chat_message("🤖 Assistant", "Welcome to your AI Study Companion! 🎉\n\nI can help you with:\n🕒 Creating personalized study timetables\n📝 Summarizing complex texts\n🧠 Taking interactive quizzes\n📊 Tracking your learning progress\n\nWhat would you like to explore today?")
    
    def setup_timetable_tab(self, notebook):
        """Setup timetable generator interface"""
        tt_frame = ttk.Frame(notebook)
        notebook.add(tt_frame, text="📅 Smart Timetable")
        
        # Main container
        main_container = tk.Frame(tt_frame, bg='white')
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Header
        header = tk.Label(main_container,
                         text="📅 Smart Study Timetable Generator",
                         font=('Helvetica', 16, 'bold'),
                         bg='white',
                         fg=self.colors['primary'])
        header.pack(pady=10)
        
        # Input section with card styling
        input_section = tk.LabelFrame(main_container,
                                     text="🎯 Customize Your Schedule",
                                     font=('Helvetica', 12, 'bold'),
                                     bg='white',
                                     fg=self.colors['secondary'],
                                     relief='groove',
                                     borderwidth=2)
        input_section.pack(fill='x', padx=20, pady=10)
        
        subjects_label = tk.Label(input_section,
                                 text="📚 Enter your subjects (separated by commas):",
                                 font=('Helvetica', 11, 'bold'),
                                 bg='white',
                                 fg=self.colors['dark'])
        subjects_label.pack(anchor='w', padx=10, pady=(10, 5))
        
        self.subjects_entry = tk.Entry(input_section,
                                      font=('Helvetica', 11),
                                      bg=self.colors['light'],
                                      relief='groove',
                                      borderwidth=2)
        self.subjects_entry.pack(fill='x', padx=10, pady=5)
        
        hours_label = tk.Label(input_section,
                              text="⏰ Study hours per day:",
                              font=('Helvetica', 11, 'bold'),
                              bg='white',
                              fg=self.colors['dark'])
        hours_label.pack(anchor='w', padx=10, pady=(10, 5))
        
        self.hours_var = tk.StringVar(value="6")
        hours_spin = tk.Spinbox(input_section,
                               from_=1, to=12,
                               textvariable=self.hours_var,
                               font=('Helvetica', 11),
                               bg=self.colors['light'],
                               relief='groove',
                               borderwidth=2)
        hours_spin.pack(anchor='w', padx=10, pady=5)
        
        generate_btn = tk.Button(input_section,
                                text="✨ Generate My Timetable",
                                font=('Helvetica', 12, 'bold'),
                                bg=self.colors['success'],
                                fg='white',
                                relief='raised',
                                borderwidth=2,
                                command=self.generate_timetable)
        generate_btn.pack(pady=15)
        
        # Display section
        display_label = tk.Label(main_container,
                                text="📋 Your Personalized Timetable",
                                font=('Helvetica', 12, 'bold'),
                                bg='white',
                                fg=self.colors['purple'])
        display_label.pack(pady=(10, 5))
        
        self.timetable_display = scrolledtext.ScrolledText(main_container,
                                                          height=12,
                                                          font=('Consolas', 10),
                                                          bg='#F8F9FA',
                                                          fg=self.colors['dark'],
                                                          relief='groove',
                                                          borderwidth=2)
        self.timetable_display.pack(fill='both', expand=True, padx=20, pady=10)
    
    def setup_summarizer_tab(self, notebook):
        """Setup text summarizer interface"""
        sum_frame = ttk.Frame(notebook)
        notebook.add(sum_frame, text="📄 Text Summarizer")
        
        # Main container
        main_container = tk.Frame(sum_frame, bg='white')
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Header
        header = tk.Label(main_container,
                         text="📄 AI Text Summarizer",
                         font=('Helvetica', 16, 'bold'),
                         bg='white',
                         fg=self.colors['accent'])
        header.pack(pady=10)
        
        subtitle = tk.Label(main_container,
                           text="Transform lengthy texts into concise summaries",
                           font=('Helvetica', 11),
                           bg='white',
                           fg=self.colors['dark'])
        subtitle.pack(pady=(0, 15))
        
        input_label = tk.Label(main_container,
                              text="📝 Paste your text here:",
                              font=('Helvetica', 12, 'bold'),
                              bg='white',
                              fg=self.colors['dark'])
        input_label.pack(anchor='w', padx=20, pady=5)
        
        self.text_input = scrolledtext.ScrolledText(main_container,
                                                   height=8,
                                                   font=('Helvetica', 11),
                                                   bg=self.colors['light'],
                                                   fg=self.colors['dark'],
                                                   relief='groove',
                                                   borderwidth=2,
                                                   wrap=tk.WORD)
        self.text_input.pack(fill='both', expand=True, padx=20, pady=5)
        
        summarize_btn = tk.Button(main_container,
                                 text="🔍 Generate Summary",
                                 font=('Helvetica', 12, 'bold'),
                                 bg=self.colors['accent'],
                                 fg='white',
                                 relief='raised',
                                 borderwidth=2,
                                 command=self.summarize_text)
        summarize_btn.pack(pady=15)
        
        summary_label = tk.Label(main_container,
                                text="✨ Summary:",
                                font=('Helvetica', 12, 'bold'),
                                bg='white',
                                fg=self.colors['success'])
        summary_label.pack(anchor='w', padx=20, pady=5)
        
        self.summary_display = scrolledtext.ScrolledText(main_container,
                                                        height=6,
                                                        font=('Helvetica', 11),
                                                        bg='#E8F8F5',
                                                        fg=self.colors['dark'],
                                                        relief='groove',
                                                        borderwidth=2,
                                                        wrap=tk.WORD)
        self.summary_display.pack(fill='both', expand=True, padx=20, pady=5)
    
    def setup_quiz_tab(self, notebook):
        """Setup quiz interface"""
        quiz_frame = ttk.Frame(notebook)
        notebook.add(quiz_frame, text="🧠 Smart Quiz")
        
        # Main container
        main_container = tk.Frame(quiz_frame, bg='white')
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Header
        header = tk.Label(main_container,
                         text="🧠 Interactive Knowledge Quiz",
                         font=('Helvetica', 16, 'bold'),
                         bg='white',
                         fg=self.colors['purple'])
        header.pack(pady=10)
        
        # Subject selection with modern styling
        subject_container = tk.LabelFrame(main_container,
                                         text="🎯 Choose Your Challenge",
                                         font=('Helvetica', 12, 'bold'),
                                         bg='white',
                                         fg=self.colors['purple'],
                                         relief='groove',
                                         borderwidth=2)
        subject_container.pack(fill='x', padx=20, pady=10)
        
        subject_frame = tk.Frame(subject_container, bg='white')
        subject_frame.pack(fill='x', padx=10, pady=10)
        
        subject_label = tk.Label(subject_frame,
                                text="📚 Select Subject:",
                                font=('Helvetica', 11, 'bold'),
                                bg='white',
                                fg=self.colors['dark'])
        subject_label.pack(side='left')
        
        self.quiz_subject_var = tk.StringVar()
        subject_combo = ttk.Combobox(subject_frame,
                                    textvariable=self.quiz_subject_var,
                                    values=list(self.quiz_manager.quizzes.keys()),
                                    font=('Helvetica', 10),
                                    state='readonly')
        subject_combo.pack(side='left', padx=10)
        
        start_quiz_btn = tk.Button(subject_frame,
                                  text="🚀 Start Quiz",
                                  font=('Helvetica', 11, 'bold'),
                                  bg=self.colors['success'],
                                  fg='white',
                                  relief='raised',
                                  borderwidth=2,
                                  command=self.start_quiz)
        start_quiz_btn.pack(side='left', padx=10)
        
        # Quiz display
        quiz_label = tk.Label(main_container,
                             text="❓ Quiz Arena",
                             font=('Helvetica', 12, 'bold'),
                             bg='white',
                             fg=self.colors['danger'])
        quiz_label.pack(pady=(15, 5))
        
        self.quiz_display = scrolledtext.ScrolledText(main_container,
                                                     height=15,
                                                     font=('Helvetica', 11),
                                                     bg='#FDF2E9',
                                                     fg=self.colors['dark'],
                                                     relief='groove',
                                                     borderwidth=2,
                                                     wrap=tk.WORD)
        self.quiz_display.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.current_quiz = []
        self.current_question_index = 0
        self.quiz_score = 0
    
    def setup_dashboard_tab(self, notebook):
        """Setup performance dashboard"""
        dash_frame = ttk.Frame(notebook)
        notebook.add(dash_frame, text="📊 Dashboard")
        
        # Main container
        main_container = tk.Frame(dash_frame, bg='white')
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Header
        header = tk.Label(main_container,
                         text="📊 Performance Analytics Dashboard",
                         font=('Helvetica', 16, 'bold'),
                         bg='white',
                         fg=self.colors['teal'])
        header.pack(pady=10)
        
        subtitle = tk.Label(main_container,
                           text="Track your learning journey and celebrate your progress!",
                           font=('Helvetica', 11),
                           bg='white',
                           fg=self.colors['dark'])
        subtitle.pack(pady=(0, 15))
        
        refresh_btn = tk.Button(main_container,
                               text="🔄 Refresh Analytics",
                               font=('Helvetica', 12, 'bold'),
                               bg=self.colors['teal'],
                               fg='white',
                               relief='raised',
                               borderwidth=2,
                               command=self.refresh_dashboard)
        refresh_btn.pack(pady=10)
        
        dashboard_label = tk.Label(main_container,
                                  text="📈 Your Learning Statistics",
                                  font=('Helvetica', 12, 'bold'),
                                  bg='white',
                                  fg=self.colors['primary'])
        dashboard_label.pack(pady=(15, 5))
        
        self.dashboard_display = scrolledtext.ScrolledText(main_container,
                                                          height=18,
                                                          font=('Consolas', 11),
                                                          bg='#EBF5FB',
                                                          fg=self.colors['dark'],
                                                          relief='groove',
                                                          borderwidth=2)
        self.dashboard_display.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.refresh_dashboard()
    
    def add_chat_message(self, sender, message):
        """Add message to chat display with colors"""
        self.chat_display.insert('end', f"🔹 {sender}:\n", 'sender')
        self.chat_display.insert('end', f"{message}\n\n", 'message')
        
        # Configure tags for colored text
        self.chat_display.tag_config('sender', foreground=self.colors['primary'], font=('Helvetica', 11, 'bold'))
        self.chat_display.tag_config('message', foreground=self.colors['dark'], font=('Helvetica', 11))
        
        self.chat_display.see('end')
    
    def process_chat_input(self, event=None):
        """Process user input in chat"""
        user_input = self.chat_input.get().strip()
        if not user_input:
            return
        
        self.add_chat_message("👤 You", user_input)
        self.chat_input.delete(0, 'end')
        
        # Simple command processing
        response = self.generate_response(user_input.lower())
        self.add_chat_message("🤖 Assistant", response)
    
    def generate_response(self, user_input):
        """Generate enhanced chatbot response"""
        if "timetable" in user_input or "schedule" in user_input:
            return "🕒 I'd love to help you create the perfect study schedule! Head over to the 'Smart Timetable' tab to generate a personalized timetable that fits your learning style. You can customize subjects and study hours!"
        elif "quiz" in user_input or "test" in user_input:
            return "🧠 Ready to challenge your knowledge? Visit the 'Smart Quiz' tab! I have questions on 8 different subjects including Data Structures, Algorithms, Machine Learning, Web Development, and more. Let's see how much you've learned!"
        elif "summary" in user_input or "summarize" in user_input:
            return "📄 Need to digest large amounts of text quickly? The 'Text Summarizer' tab is your friend! Just paste any lengthy content and I'll extract the key points for you in seconds."
        elif "performance" in user_input or "progress" in user_input or "dashboard" in user_input:
            return "📊 Check out your learning analytics in the 'Dashboard' tab! You can track your quiz scores, study patterns, and see detailed performance metrics across all subjects."
        elif "subjects" in user_input:
            subjects = list(self.quiz_manager.quizzes.keys())
            return f"📚 I can help you with these exciting subjects:\n" + "\n".join([f"• {subject}" for subject in subjects]) + "\n\nWhich one interests you the most?"
        elif "help" in user_input or "what can you do" in user_input:
            return "🎉 I'm your comprehensive study companion! Here's what I can do:\n\n📅 Smart Timetables - Create personalized study schedules\n📄 Text Summarization - Condense long texts into key points\n🧠 Interactive Quizzes - Test knowledge across 8+ subjects\n📊 Performance Tracking - Monitor your learning progress\n💬 Study Guidance - Answer questions about your studies\n\nWhat would you like to explore first?"
        elif "thank" in user_input:
            return "🙏 You're very welcome! I'm here to support your learning journey. Keep up the great work, and remember - every expert was once a beginner! 🌟"
        else:
            return "🎯 I'm here to supercharge your learning experience! You can ask me about creating timetables, taking quizzes, summarizing texts, or checking your progress. I also have detailed features in each tab - feel free to explore them all! What interests you most right now?"
    
    def generate_timetable(self):
        """Generate and display colorful timetable"""
        subjects_text = self.subjects_entry.get().strip()
        if not subjects_text:
            messagebox.showwarning("⚠️ Input Required", "Please enter your subjects to create a timetable!")
            return
        
        subjects = [s.strip() for s in subjects_text.split(',')]
        hours = int(self.hours_var.get())
        
        timetable = self.timetable_gen.create_timetable(subjects, hours)
        
        # Display colorful timetable
        self.timetable_display.delete(1.0, 'end')
        self.timetable_display.insert('end', "🎓 YOUR PERSONALIZED STUDY TIMETABLE 🎓\n")
        self.timetable_display.insert('end', "=" * 50 + "\n\n")
        
        day_emojis = {
            'Monday': '🌟', 'Tuesday': '🔥', 'Wednesday': '⚡', 
            'Thursday': '🚀', 'Friday': '💎', 'Saturday': '🎯', 'Sunday': '🌈'
        }
        
        for day, schedule in timetable.items():
            emoji = day_emojis.get(day, '📅')
            self.timetable_display.insert('end', f"{emoji} {day.upper()}\n")
            self.timetable_display.insert('end', "-" * 25 + "\n")
            for slot in schedule:
                self.timetable_display.insert('end', f"  🕐 {slot}\n")
            self.timetable_display.insert('end', "\n")
        
        self.timetable_display.insert('end', "💪 Stay consistent and achieve your goals! 💪")
    
    def summarize_text(self):
        """Summarize input text"""
        text = self.text_input.get(1.0, 'end').strip()
        if not text:
            messagebox.showwarning("⚠️ Input Required", "Please enter text to summarize!")
            return
        
        summary = self.summarizer.summarize(text)
        
        self.summary_display.delete(1.0, 'end')
        self.summary_display.insert('end', "✨ SUMMARY GENERATED ✨\n")
        self.summary_display.insert('end', "=" * 30 + "\n\n")
        self.summary_display.insert('end', summary)
        self.summary_display.insert('end', "\n\n💡 Key points extracted successfully!")
    
    def start_quiz(self):
        """Start a colorful quiz for selected subject"""
        subject = self.quiz_subject_var.get()
        if not subject:
            messagebox.showwarning("⚠️ Selection Required", "Please select a subject first!")
            return
        
        self.current_quiz = self.quiz_manager.get_quiz(subject)
        self.current_question_index = 0
        self.quiz_score = 0
        
        self.display_current_question()
    
    def display_current_question(self):
        """Display current quiz question with styling"""
        if self.current_question_index >= len(self.current_quiz):
            self.end_quiz()
            return
        
        question_data = self.current_quiz[self.current_question_index]
        
        self.quiz_display.delete(1.0, 'end')
        self.quiz_display.insert('end', f"🎯 QUIZ CHALLENGE 🎯\n")
        self.quiz_display.insert('end', "=" * 40 + "\n\n")
        self.quiz_display.insert('end', f"📍 Question {self.current_question_index + 1} of {len(self.current_quiz)}\n\n")
        self.quiz_display.insert('end', f"❓ {question_data['question']}\n\n")
        
        option_emojis = ['🅰️', '🅱️', '🅲️', '🅳️']
        for i, option in enumerate(question_data['options']):
            emoji = option_emojis[i] if i < len(option_emojis) else f"{i+1}️⃣"
            self.quiz_display.insert('end', f"{emoji} {option}\n")
        
        self.quiz_display.insert('end', f"\n💭 Enter your answer (1-{len(question_data['options'])}): ")
        
        # Create answer input with modern styling
        answer_frame = tk.Frame(self.quiz_display.master, bg='white')
        
        self.answer_entry = tk.Entry(answer_frame,
                                    font=('Helvetica', 12),
                                    bg=self.colors['light'],
                                    relief='groove',
                                    borderwidth=2,
                                    width=5)
        self.answer_entry.pack(side='left', padx=5)
        
        submit_btn = tk.Button(answer_frame,
                              text="✅ Submit",
                              font=('Helvetica', 10, 'bold'),
                              bg=self.colors['success'],
                              fg='white',
                              relief='raised',
                              borderwidth=2,
                              command=self.submit_answer)
        submit_btn.pack(side='left', padx=5)
        
        answer_frame.pack(pady=10)
        
        self.answer_entry.focus()
        self.answer_entry.bind('<Return>', lambda e: self.submit_answer())
    
    def submit_answer(self):
        """Submit quiz answer with enhanced feedback"""
        try:
            answer = int(self.answer_entry.get()) - 1
            correct_answer = self.current_quiz[self.current_question_index]['answer']
            
            if answer == correct_answer:
                self.quiz_score += 1
                result = "🎉 CORRECT! Excellent work! ✅"
                # result_color = self.colors['success'] # Not used directly for text color in scrolledtext
            else:
                correct_option = self.current_quiz[self.current_question_index]['options'][correct_answer]
                result = f"❌ Incorrect! The correct answer was: {correct_answer + 1}. {correct_option}"
                # result_color = self.colors['danger'] # Not used directly for text color in scrolledtext
            
            self.quiz_display.insert('end', f"\n{result}\n")
            
            self.current_question_index += 1
            
            # Clear answer input
            for widget in self.quiz_display.master.pack_slaves():
                if isinstance(widget, tk.Frame) and widget != self.quiz_display.master.master:
                    widget.destroy()
            
            self.root.after(3000, self.display_current_question)
            
        except ValueError:
            messagebox.showerror("❌ Invalid Input", "Please enter a valid number!")
    
    def end_quiz(self):
        """End quiz with enhanced results display"""
        subject = self.quiz_subject_var.get()
        total_questions = len(self.current_quiz)
        
        # Record performance
        self.performance_tracker.record_quiz_score(subject, self.quiz_score, total_questions)
        
        percentage = (self.quiz_score / total_questions) * 100
        
        self.quiz_display.insert('end', f"\n🏆 QUIZ COMPLETED! 🏆\n")
        self.quiz_display.insert('end', "=" * 35 + "\n\n")
        self.quiz_display.insert('end', f"📊 Final Score: {self.quiz_score}/{total_questions} ({percentage:.1f}%)\n\n")
        
        if percentage >= 90:
            self.quiz_display.insert('end', "🌟 OUTSTANDING! You're a true expert! 🌟\n")
        elif percentage >= 80:
            self.quiz_display.insert('end', "🎉 EXCELLENT! Great knowledge! 🎉\n")
        elif percentage >= 70:
            self.quiz_display.insert('end', "👍 GOOD JOB! Keep it up! 👍\n")
        elif percentage >= 60:
            self.quiz_display.insert('end', "📚 Not bad! More practice will help! 📚\n")
        else:
            self.quiz_display.insert('end', "💪 Keep studying! You'll improve! 💪\n")
        
        self.quiz_display.insert('end', f"\n✨ Great effort in {subject}! ✨")
    
    def refresh_dashboard(self):
        """Refresh performance dashboard with enhanced visuals"""
        self.dashboard_display.delete(1.0, 'end')
        
        performance = self.performance_tracker.get_performance_summary()
        
        self.dashboard_display.insert('end', "📊 YOUR LEARNING ANALYTICS DASHBOARD 📊\n")
        self.dashboard_display.insert('end', "=" * 55 + "\n\n")
        
        if not performance:
            self.dashboard_display.insert('end', "🎯 Ready to start your learning journey?\n\n")
            self.dashboard_display.insert('end', "Take some quizzes to see your progress reflected here!\n")
            self.dashboard_display.insert('end', "You can also manually record study time if you wish.\n\n")
            return
        
        for subject, stats in performance.items():
            self.dashboard_display.insert('end', f"📚 {subject}:\n")
            self.dashboard_display.insert('end', f"  • Average Quiz Score: {stats['average_score']}%\n")
            self.dashboard_display.insert('end', f"  • Quiz Attempts: {stats['quiz_attempts']}\n")
            self.dashboard_display.insert('end', f"  • Total Study Time: {stats['total_study_time']} minutes\n\n")
        
        # Overall stats
        total_quizzes = sum(stats['quiz_attempts'] for stats in performance.values())
        
        # Calculate overall average score, handling division by zero if no quizzes taken
        total_score_sum = sum(stats['average_score'] * stats['quiz_attempts'] for stats in performance.values())
        avg_overall = total_score_sum / total_quizzes if total_quizzes > 0 else 0
        
        total_study_minutes = sum(stats['total_study_time'] for stats in performance.values())
        
        self.dashboard_display.insert('end', f"🎯 OVERALL STATISTICS:\n")
        self.dashboard_display.insert('end', f"  • Total Quizzes Taken: {total_quizzes}\n")
        self.dashboard_display.insert('end', f"  • Overall Average Score: {avg_overall:.1f}%\n")
        self.dashboard_display.insert('end', f"  • Total Study Time Across Subjects: {total_study_minutes} minutes\n\n")
        self.dashboard_display.insert('end', "Keep up the fantastic work! Your dedication is paying off! 🚀")
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

# Run the application
if __name__ == "__main__":
    app = StudyAssistantChatbot()
    app.run()
