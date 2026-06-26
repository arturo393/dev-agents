import sys
import re
import os

class CPPTradingAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.filename = os.path.basename(file_path)
        self.content = ""
        self.issues = []
        
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                self.content = f.read()
        else:
            sys.exit(1)

    def add_issue(self, category, severity, line_no, message, snippet=""):
        self.issues.append({
            "category": category,
            "severity": severity,
            "line": line_no,
            "message": message,
            "snippet": snippet
        })

    def analyze(self):
        # Existing checks
        self.check_memory_management()
        self.check_trading_safety()
        self.check_performance_pro()
        self.check_error_handling()
        
        # New "Elite" checks
        self.check_configurability()
        self.check_latency_awareness()
        self.check_system_health()
        
        return self.issues

    def check_memory_management(self):
        lines = self.content.split('\n')
        for i, line in enumerate(lines):
            if re.search(r'\bnew\b', line) and 'std::make_' not in line and '//' not in line:
                self.add_issue("Memory", "High", i+1, "Raw pointer (new). Use smart pointers.", line.strip())
            
            if re.search(r'\bdelete\b', line) and not re.search(r'=\s*delete', line) and '//' not in line:
                self.add_issue("Memory", "Medium", i+1, "Manual delete. Use RAII.", line.strip())

    def check_trading_safety(self):
        if "place_market_order" in self.content or "place_limit_order" in self.content:
            if "round_price" not in self.content:
                self.add_issue("Trading", "Critical", 0, "No rounding before order placement.")
        
        # Slippage awareness check (Enhanced)
        has_market_order = "place_market_order" in self.content
        has_slippage_check = any(x in self.content.lower() for x in ["get_order_book", "orderbook", "get_ticker", "ticker.ask_price"])
        # Martingale / Toxic Risk detection
        martingale_patterns = ["size * 2", "size *= 2", "risk * 2", "double_down"]
        for pattern in martingale_patterns:
            if pattern in self.content.lower():
                self.add_issue("Risk", "Critical", 0, f"Potential Martingale pattern detected: '{pattern}'. High ruin risk.")

    def check_performance_pro(self):
        # Vector by value check
        matches = re.finditer(r'\(\s*(?:[^,)]+,)*\s*(std::vector<[^>]+>)\s+[^&,)]+\s*[ ,)]', self.content)
        for match in matches:
            line_no = self.content.count('\n', 0, match.start()) + 1
            self.add_issue("Performance", "Medium", line_no, "Pass vector by value. Use const&.")

        # Pre-allocation awareness
        if "std::vector" in self.content and ".push_back" in self.content and ".reserve" not in self.content:
            self.add_issue("Performance", "Low", 0, "Vector used with push_back but no reserve() found. Potential reallocations in hot-path.")

    def check_latency_awareness(self):
        # Tick-to-trade measurement
        if "high_resolution_clock" not in self.content and "chrono" in self.content:
             self.add_issue("Latency", "Low", 0, "No high-resolution timing found. Latency tracking is recommended for HFT.")

    def check_configurability(self):
        # Magic Numbers detection (simplified)
        magic_matches = re.finditer(r'=\s*(0\.[0-9]+|1\.[0-9]+)\s*;', self.content)
        for match in magic_matches:
            val = match.group(1)
            # Ignore 0.0 and 1.0 commonly
            if val not in ["0.0", "1.0", "0", "1"]:
                line_no = self.content.count('\n', 0, match.start()) + 1
                self.add_issue("Design", "Medium", line_no, f"Magic number detected ({val}). Move to config/env.", match.group(0).strip())

    def check_system_health(self):
        # Heartbeat/Watchdog existence check
        if self.filename == "main.cpp":
            if "heartbeat" not in self.content.lower() and "watchdog" not in self.content.lower():
                self.add_issue("Reliability", "High", 0, "No Heartbeat/Watchdog mechanism detected in main loop.")

    def check_error_handling(self):
        matches = re.finditer(r'catch\s*\([^{]*\)\s*\{\s*\}', self.content, re.MULTILINE)
        for match in matches:
            line_no = self.content.count('\n', 0, match.start()) + 1
            self.add_issue("Robustness", "Medium", line_no, "Empty catch block.")

    def generate_report(self):
        print(f"# Reporte de Auditoría Pro: {self.filename}")
        if not self.issues:
            print("✅ Auditoría Pro completada. Sin hallazgos graves.")
            return
        
        severity_map = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
        self.issues.sort(key=lambda x: severity_map.get(x['severity'], 99))
        print(f"Total Hallazgos: {len(self.issues)}")
        print("\n| Severidad | Categoría | Línea | Mensaje |")
        print("|-----------|-----------|-------|---------|")
        for i in self.issues:
            line = i['line'] if i['line'] > 0 else "File"
            print(f"| {i['severity']} | {i['category']} | {line} | {i['message']} |")

if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit(1)
    analyzer = CPPTradingAnalyzer(sys.argv[1])
    analyzer.analyze()
    analyzer.generate_report()
