import re

# Preprocess text
def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # remove punctuation
    sentences = text.split('.')          # split into sentences
    return [s.strip() for s in sentences if s.strip()]

# Edit Distance (Levenshtein)
def edit_distance(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0]*(n+1) for _ in range(m+1)]

    for i in range(m+1):
        for j in range(n+1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(
                    dp[i-1][j],     # delete
                    dp[i][j-1],     # insert
                    dp[i-1][j-1]    # replace
                )
    return dp[m][n]

# Main comparison function
def compare_reports(report1, report2, threshold=5):
    sentences1 = preprocess(report1)
    sentences2 = preprocess(report2)

    score = 0

    for s1 in sentences1:
        for s2 in sentences2:

            # Exact match using hash
            if hash(s1) == hash(s2):
                score += 1

            else:
                dist = edit_distance(s1, s2)
                if dist < threshold:
                    score += 0.5

    similarity = (score / len(sentences1)) * 100 if sentences1 else 0
    return similarity


# Example usage
report1 = "AI is transforming education. Students learn faster."
report2 = "Education is changing due to AI. Students can learn quickly."

result = compare_reports(report1, report2)

print(f"Similarity: {result:.2f}%")