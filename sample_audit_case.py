import pandas as pd

# Synthetic audit cases based on the proposed framework
cases = [
    {
        "Case_ID": "CASE_A",
        "Context": "High load, occupied, scheduled",
        "Evidence": "Occupancy present; equipment expected",
        "Expected_State": "UNUSUAL",
        "Diagnosis": "Likely legitimate demand",
        "Recommendation": "No immediate escalation; continue monitoring"
    },
    {
        "Case_ID": "CASE_B",
        "Context": "High load, vacant, off-schedule",
        "Evidence": "No occupancy; equipment state unexpected",
        "Expected_State": "POTENTIALLY_ACTIONABLE",
        "Diagnosis": "Possible unnecessary energy use",
        "Recommendation": "Inspect equipment and operating schedule"
    },
    {
        "Case_ID": "CASE_C",
        "Context": "High load, occupancy data missing",
        "Evidence": "Context incomplete",
        "Expected_State": "INSUFFICIENT_EVIDENCE",
        "Diagnosis": "Unknown",
        "Recommendation": "Obtain or validate occupancy data"
    },
    {
        "Case_ID": "CASE_D",
        "Context": "Persistent high load",
        "Evidence": "Independent fault record available",
        "Expected_State": "CONFIRMED_ACTIONABLE",
        "Diagnosis": "Fault supported by independent evidence",
        "Recommendation": "Escalate for corrective action"
    }
]

df = pd.DataFrame(cases)

print("\nSYNTHETIC AUDIT CASES\n")
print(df.to_string(index=False))

df.to_csv("sample_audit_cases.csv", index=False)

print("\nSample audit cases saved as sample_audit_cases.csv")