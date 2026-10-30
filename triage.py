"""Questionnaire-based inspection priority, NOT ML-based severity prediction.

These demonstration rules are not industrial acceptance criteria; expert review is required.
"""

DEPTHS = {"unknown", "surface", "deep"}
EXTENTS = {"unknown", "localized", "widespread"}
CRITICALS = {"unknown", "yes", "no"}


def assess_inspection_priority(depth: str, extent: str, critical: str) -> dict:
    if depth not in DEPTHS or extent not in EXTENTS or critical not in CRITICALS:
        raise ValueError("Invalid questionnaire values")

    if depth == "deep" or (extent == "widespread" and critical == "yes"):
        priority = "high"
        title = "أولوية فحص مرتفعة"
        action = "أوقف اتخاذ قرار القبول الآلي، واعرض القطعة على مسؤول الجودة أو مهندس مختص."
        reason = "أفاد المستخدم بعمق كبير، أو بانتشار واسع في جزء حساس."
    elif depth == "surface" and extent == "localized" and critical == "no":
        priority = "routine"
        title = "فحص روتيني مبدئي"
        action = "أجرِ فحصًا بصريًا وقياسات مناسبة وفق معايير الجودة المعتمدة قبل القبول."
        reason = "أفاد المستخدم بأن الأثر سطحي ومحدود والقطعة غير حساسة."
    else:
        priority = "review"
        title = "يحتاج مراجعة فنية"
        action = "استكمل قياسات العمق والامتداد ومعلومات استخدام القطعة قبل تحديد الشدة."
        reason = "المعلومات غير كافية أو تستلزم التحقق من شروط الاستخدام."

    return {
        "priority": priority,
        "priority_ar": title,
        "reason": reason,
        "recommended_action": action,
        "actual_severity": "غير محددة",
        "basis": "تقييم أولي مبني على إجابات المستخدم، وليس على نموذج يتنبأ بشدة الضرر.",
        "notice": "ليس حكمًا هندسيًا أو قرار قبول/رفض صناعيًا. لا يمكن استنتاج عمق العيب أو خطورته من هذا النموذج وحده.",
    }
