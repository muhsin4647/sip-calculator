import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style
import math

class SIPCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("SIP Calculator")
        self.root.geometry("1000x750")

        # Color Scheme
        self.colors = {
            'dark_red': '#8B0000',
            'medium_red': '#B22222',
            'light_red': '#FFE5E5',
            'gold': '#FFD700',
            'off_white': '#FFF5E6',
            'dark_text': '#2C1A1A'
        }

        self.style = Style(theme='darkly')
        self._configure_styles()
        self._create_widgets()

    def _configure_styles(self):
        self.style.configure('TFrame', background=self.colors['dark_red'])
        self.style.configure('TLabelframe',
                             background=self.colors['medium_red'],
                             bordercolor=self.colors['gold'],
                             relief='solid',
                             borderwidth=2)
        self.style.configure('TLabelframe.Label',
                             font=('Helvetica', 12, 'bold'),
                             background=self.colors['medium_red'],
                             foreground=self.colors['gold'])
        self.style.configure('TLabel',
                             font=('Helvetica', 11),
                             background=self.colors['medium_red'],
                             foreground=self.colors['off_white'])
        self.style.configure('TEntry',
                             fieldbackground=self.colors['light_red'],
                             foreground=self.colors['dark_text'],
                             font=('Helvetica', 11))
        self.style.configure('Treeview',
                             background=self.colors['light_red'],
                             fieldbackground=self.colors['light_red'],
                             foreground=self.colors['dark_text'],
                             rowheight=25)
        self.style.configure('Treeview.Heading',
                             font=('Helvetica', 12, 'bold'),
                             background=self.colors['medium_red'],
                             foreground=self.colors['gold'])
        self.style.map('Treeview.Heading',
                       background=[('active', self.colors['dark_red'])])
        self.style.configure('Gold.TButton',
                             font=('Helvetica', 12, 'bold'),
                             background=self.colors['gold'],
                             foreground=self.colors['dark_text'],
                             bordercolor=self.colors['gold'],
                             focusthickness=0)
        self.style.map('Gold.TButton',
                       background=[('active', self.colors['medium_red'])])

    def _create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=(30, 20))
        main_frame.pack(fill='both', expand=True)

        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill='x', pady=(0, 20))

        ttk.Label(header_frame,
                  text="SIP CALCULATOR",
                  font=('Helvetica', 20, 'bold'),
                  foreground=self.colors['gold'],
                  background=self.colors['dark_red']).pack(side='left')

        input_frame = ttk.LabelFrame(main_frame, text=" Investment Parameters ")
        input_frame.pack(fill='x', pady=10, ipady=10)

        self._create_input_fields(input_frame)

        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=15)

        ttk.Button(btn_frame,
                   text="Calculate Projection",
                   style='Gold.TButton',
                   command=self.calculate_sip).pack(side='left', padx=10)
        ttk.Button(btn_frame,
                   text="Clear All",
                   style='Gold.TButton',
                   command=self.clear_inputs).pack(side='left', padx=10)

        results_frame = ttk.LabelFrame(main_frame, text=" Investment Breakdown ")
        results_frame.pack(fill='both', expand=True, pady=10)

        self._create_results_display(results_frame)

    def _create_input_fields(self, parent):
        fields = [
            ("Monthly Investment (₹)", 'monthly_investment'),
            ("Expected Annual Return (%)", 'annual_return'),
            ("Investment Period (Years)", 'investment_years')
        ]

        for label_text, var_name in fields:
            row = ttk.Frame(parent)
            row.pack(fill='x', pady=8)

            ttk.Label(row, text=label_text, width=25, anchor='w').pack(side='left', padx=10)

            entry = ttk.Entry(row, font=('Helvetica', 12), width=20)
            entry.pack(side='right', padx=10)
            setattr(self, var_name, entry)

    def _create_results_display(self, parent):
        summary_frame = ttk.Frame(parent)
        summary_frame.pack(fill='x', pady=10)

        summary_data = [
            ("Total Invested", "total_invested"),
            ("Estimated Returns", "estimated_returns"),
            ("Maturity Value", "total_value")
        ]

        for col, (label, var_name) in enumerate(summary_data):
            card = ttk.Frame(summary_frame, relief='solid', borderwidth=1)
            card.grid(row=0, column=col, padx=10, sticky='nsew')

            ttk.Label(card, text=label,
                      font=('Helvetica', 12),
                      foreground=self.colors['gold']).pack(pady=5)

            label_widget = ttk.Label(card, text="₹0.00",
                                     font=('Helvetica', 14, 'bold'),
                                     foreground=self.colors['off_white'])
            label_widget.pack(pady=5)
            setattr(self, var_name, label_widget)

        # Treeview uses simple internal column names
        self.tree = ttk.Treeview(parent,
                                 columns=('year', 'invested', 'returns', 'total'),
                                 show='headings',
                                 selectmode='none')

        headers = [
            ('year', 'Year', 100),
            ('invested', 'Invested (₹)', 150),
            ('returns', 'Returns (₹)', 150),
            ('total', 'Total (₹)', 150)
        ]

        for col_id, text, width in headers:
            self.tree.heading(col_id, text=text, anchor='center')
            self.tree.column(col_id, width=width, anchor='center')

        scrollbar = ttk.Scrollbar(parent, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

    def calculate_sip(self):
        try:
            p = float(self.monthly_investment.get())
            r = float(self.annual_return.get()) / 100
            n = float(self.investment_years.get())

            if p <= 0 or r <= 0 or n <= 0:
                raise ValueError("All values must be positive")

            months = n * 12
            monthly_rate = r / 12

            future_value = p * ((math.pow(1 + monthly_rate, months) - 1) * (1 + monthly_rate) / monthly_rate)
            total_invested = p * months
            estimated_returns = future_value - total_invested

            self.total_invested.config(text=f"₹{total_invested:,.2f}")
            self.estimated_returns.config(text=f"₹{estimated_returns:,.2f}")
            self.total_value.config(text=f"₹{future_value:,.2f}")

            self.generate_yearly_breakdown(p, r, n)

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid positive numbers")

    def generate_yearly_breakdown(self, monthly_investment, annual_rate, years):
        self.tree.delete(*self.tree.get_children())

        monthly_rate = annual_rate / 12

        for year in range(1, int(years) + 1):
            months = year * 12
            year_fv = monthly_investment * ((math.pow(1 + monthly_rate, months) - 1) *
                                            (1 + monthly_rate) / monthly_rate)
            year_invested = monthly_investment * months
            year_returns = year_fv - year_invested

            self.tree.insert('', 'end', values=(
                year,
                f"{year_invested:,.2f}",
                f"{year_returns:,.2f}",
                f"{year_fv:,.2f}"
            ))

    def clear_inputs(self):
        self.monthly_investment.delete(0, 'end')
        self.annual_return.delete(0, 'end')
        self.investment_years.delete(0, 'end')
        self.total_invested.config(text="₹0.00")
        self.estimated_returns.config(text="₹0.00")
        self.total_value.config(text="₹0.00")
        self.tree.delete(*self.tree.get_children())

if __name__ == "__main__":
    root = tk.Tk()
    app = SIPCalculator(root)
    root.mainloop()
