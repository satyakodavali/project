import math

def attendance_logic(attended, held):
    if held == 0:
        return {
            "percentage": 0,
            "prediction": "Data not available",
            "suggestion": "Keep attending classes to build your record.",
            "risk_level": "N/A"
        }
    
    perc = float(round((attended * 100.0) / held, 2))
    
    if perc < 60.0:
        status = "High risk"
        risk_level = "High"
        suggestion = "Your attendance is critically low. Contact your mentor immediately."
    elif perc < 75:
        status = "Recovery possible"
        risk_level = "Medium"
        suggestion = "You are below the 75% threshold. Regular attendance is required."
    else:
        status = "Safe"
        risk_level = "Low"
        suggestion = "Maintain your current attendance level to stay safe."

    # Calculate required classes for 75%
    # (attended + x) / (held + x) = 0.75
    # x = (0.75 * held - attended) / 0.25 = 3 * held - 4 * attended
    required_classes = 0
    if perc < 75:
        required_classes = max(0, math.ceil((0.75 * held - attended) / 0.25))
        suggestion += f" You need to attend {required_classes} more classes continuously to reach 75%."

    return {
        "percentage": perc,
        "prediction": status,
        "suggestion": suggestion,
        "risk_level": risk_level,
        "needed": required_classes
    }

def marks_prediction(mid1, mid2):
    # Assuming each mid is out of 25, total 50. Pass threshold is ~15-20.
    avg = (mid1 + mid2) / 2.0
    if avg < 10:
        risk = "Critical Risk"
        min_marks = 50 # Out of 70 for sem
        msg = f"Your internal marks are low. You need at least {min_marks} marks in the Semester exam to pass."
    elif avg < 15:
        risk = "Moderate Risk"
        min_marks = 35
        msg = f"Average performance. You need at least {min_marks} marks in the Semester exam to be safe."
    else:
        risk = "Low Risk"
        min_marks = 25
        msg = "Good internals! Just aim for 28+ in Semester exams to clear easily."
    
    return {
        "risk": risk,
        "min_needed": min_marks,
        "message": msg
    }

def cgpa_backlog_logic(cgpa):
    if cgpa < 8:
        risk = "Close to 8 CGPA"
        backlogs_needed = "1-10" # Dynamic logic in engine.py
        motivation = "You are close to 8 CGPA. With better performance in upcoming exams, you can easily improve. Focus on weak subjects and practice regularly."
    else:
        risk = "Excellent performance"
        backlogs_needed = "0"
        motivation = "Great! Your CGPA is good. Keep maintaining this performance."
    
    return {
        "risk_level": risk,
        "backlog_range": backlogs_needed,
        "motivation": motivation
    }

def fees_warning_logic(due_amount):
    if due_amount > 0:
        return f"Warning: You have a pending fee of Rs. {due_amount}. Pay before deadline to avoid fine."
    return "Great! No fees due."

def backlog_exam_message(subject, date):
    return f"Your backlog exam for {subject} is scheduled on {date}. Prepare before this date to clear it."
