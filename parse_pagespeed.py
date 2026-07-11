import json

try:
    with open('pagespeed_mobile.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if 'error' in data:
        print("Error from API:", data['error']['message'])
    else:
        metrics = data.get('lighthouseResult', {}).get('audits', {})
        print("Failing Audits:")
        for k, v in metrics.items():
            score = v.get('score')
            if score is not None and score < 0.9:
                print(f"{v.get('title')}: {score} - {v.get('displayValue', '')}")
except Exception as e:
    print("Failed to read JSON:", e)
