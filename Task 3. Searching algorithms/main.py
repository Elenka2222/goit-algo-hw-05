import os
import timeit as t
import matplotlib.pyplot as plt
import pandas as pd # Used for better data presentation

# Boyer-Moore algorithm
def bm_table(p):
    L=len(p); d={}
    for i,c in enumerate(p[:-1]): d[c]=L-i-1
    d.setdefault(p[-1],L); return d

def bm(s,p):
    L=len(p); d=bm_table(p); i=0
    while i<=len(s)-L:
        j=L-1
        while j>=0 and s[i+j]==p[j]: j-=1
        if j<0: return i
        i+=d.get(s[i+L-1],L)
    return -1

# Knuth-Morris-Pratt algorithm
def lps(p):
    a=[0]*len(p); l=0; i=1
    while i<len(p):
        if p[i]==p[l]: l+=1; a[i]=l; i+=1
        elif l: l=a[l-1]
        else: i+=1
    return a

def kmp(s,p):
    i=j=0; L=len(p); A=lps(p)
    while i<len(s):
        if s[i]==p[j]: i+=1; j+=1
        elif j: j=A[j-1]
        else: i+=1
        if j==L: return i-L
    return -1

# Rabin-Karp algorithm
def rk(s,p):
    m=len(p); n=len(s); B=256; M=101
    h=lambda x: sum(ord(c)*pow(B,m-i-1,M) for i,c in enumerate(x))%M
    hp=h(p); hs=h(s[:m]); H=pow(B,m-1,M)
    for i in range(n-m+1):
        if hp==hs and s[i:i+m]==p: return i
        if i<n-m:
            hs=(hs-ord(s[i])*H)%M
            hs=(hs*B+ord(s[i+m]))%M
    return -1

# Load texts from files (assumes files are in the same directory)
paths=["article1.txt", "article2.txt"]
texts=[open(p,encoding="utf-8").read() for p in paths]

# Patterns for each text: 4 existing (common in both) + 1 fake ("БАНАН")
patterns = [
    ["список", "дерево", "інформації", "систем", "БАНАН"],
    ["список", "дерево", "інформації", "систем", "БАНАН"]
]

algs={"Boyer-Moore":bm,"KMP":kmp,"Rabin-Karp":rk}
results = [] # List to store dicts of results

# Measure execution time
NUM_RUNS = 5
for i,txt in enumerate(texts):
    text_name = f"T{i+1}"
    for alg_name, func in algs.items():
        for pat in patterns[i]:
            time_spent = t.timeit(lambda: func(txt,pat), number=NUM_RUNS)/NUM_RUNS
            found = func(txt,pat) != -1
            results.append({
                "Text": text_name,
                "Algorithm": alg_name,
                "Pattern": pat,
                "Time (sec)": time_spent,
                "Found": "Yes" if found else "No"
            })

# Create DataFrame for better output and plotting data
df = pd.DataFrame(results)

# Print detailed table
print("Detailed Performance Results")
print(df.to_markdown(index=False))

# Prepare data for plotting
df['Label'] = df['Text'] + "-" + df['Algorithm'] + "-" + df['Pattern']
plot_data = df.sort_values(by='Time (sec)', ascending=False)

# Plotting
plt.figure(figsize=(12, 8))
bars = plt.barh(plot_data['Label'], plot_data['Time (sec)'], color='teal')
plt.xlabel("Time (sec)")
plt.title(f"Substring Search Performance (Average of {NUM_RUNS} runs)")
plt.gca().invert_yaxis() # To have the fastest at the top

# Add 'Found' status as text next to the bars
for bar, status in zip(bars, plot_data['Found']):
    plt.text(bar.get_width() + 0.0000001, bar.get_y() + bar.get_height()/2, status,
             ha='left', va='center', fontsize=9)

plt.tight_layout()

plt.show()

# Conclusion
print("\n--- Conclusion ---")
for text_name in df['Text'].unique():
    text_df = df[df['Text'] == text_name]
    min_time_overall = text_df['Time (sec)'].min()
    fastest_alg_overall = text_df[text_df['Time (sec)'] == min_time_overall]['Algorithm'].iloc[0]
    
    # Calculate average time per algorithm for the text
    avg_times = text_df.groupby('Algorithm')['Time (sec)'].mean().sort_values()
    fastest_avg = avg_times.index[0]
    
    print(f"\n{text_name}:")
    print(f"  Fastest run: {fastest_alg_overall} with time {min_time_overall:.6f} sec.")
    print(f"  Overall average fastest: {fastest_avg} (Avg Time: {avg_times.iloc[0]:.6f} sec.)")