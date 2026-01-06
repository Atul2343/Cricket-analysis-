def generate_report(matches):
    report = "🏏 DAILY CRICKET ANALYSIS REPORT 🏏\n\n"
    for m in matches:
        report += f"• {m}\n"
    report += "\n⚠️ Disclaimer: This is analysis only."
    return report
