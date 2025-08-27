# pip install pandas seaborn matplotlib
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
import textwrap
from pathlib import Path

data_blocks = {
    "Educational level": {
        "labels": ["K-12", "High school", "University", "Professionals", "General/not specified"],
        "counts": [10, 1, 13, 1, 6],
    },
    "Subject": {
        # 4 buckets visible in the % row (62.1, 20.7, 13.8, 3.4) -> counts 18, 6, 4, 1
        "labels": ["STEM", "Language and humanities", "General/not specified", "Other"],
        "counts": [18, 6, 4, 1],
    },
    "LLM type": {
        "labels": ["Open source", "Proprietary"],
        "counts": [24, 6],
    },
    "Data": {
        "labels": ["Human-generated", "Synthetic", "Hybrid", "Other"],
        "counts": [14, 7, 9, 0],
    },
    "Optimization technique": {
        "labels": ["Supervised methods", "Unsupervised pre-training", "RL/Preference Optimization", "Other"],
        "counts": [24, 3, 8, 6],
    },
    "Pedagogical principles": {
        "labels": ["Content and accuracy", "Process and strategy", "Learner adaption", "Engagement and affect", "Other"],
        "counts": [23, 25, 11, 15, 3],
    },
    "Evaluation": {
        "labels": ["Automated metrics", "Expert rating", "Learning outcomes", "Other"],
        "counts": [19, 22, 4, 1],
    },
}

# Global styling
mpl.rcParams["font.family"] = "serif"
mpl.rcParams["font.serif"] = ["Times New Roman", "Times", "DejaVu Serif", "Georgia"]
mpl.rcParams["axes.grid"] = False
sns.set_theme(style="white")  # clean background, no grid

SAVE_DIR = Path("figs_from_table")
SAVE_DIR.mkdir(exist_ok=True)

YMAX = 30  # fixed y-axis as requested

def wrap_xticks(ax, width=12):
    labels = [textwrap.fill(t.get_text(), width=width) for t in ax.get_xticklabels()]
    ax.set_xticklabels(labels, rotation=0, ha="center")

def annotate_counts(ax):
    for p in ax.patches:
        h = p.get_height()
        ax.annotate(
            f"{int(h)}",
            (p.get_x() + p.get_width()/2, h),
            ha="center", va="bottom",
            fontsize=9, xytext=(0, 2), textcoords="offset points"
        )

for title, block in data_blocks.items():
    df = pd.DataFrame({"label": block["labels"], "count": block["counts"]})

    # width scales with number of bars; height kept moderate for journal figs
    fig_w = max(5.5, min(14, 0.65 * len(df) + 3))
    fig_h = 4.2

    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    sns.barplot(data=df, x="label", y="count", ax=ax)

    ax.set_title(title, pad=10)
    ax.set_xlabel("")
    ax.set_ylabel("Paper count")
    ax.set_ylim(0, YMAX)
    sns.despine(ax=ax)
    wrap_xticks(ax, width=12)     # keeps labels horizontal
    annotate_counts(ax)           # numbers on bars

    plt.tight_layout()
    fig.savefig(SAVE_DIR / f"{title.replace(' ', '_').lower()}_bars.png", dpi=300)
    plt.close(fig)

print(f"Saved {len(data_blocks)} PNGs to: {SAVE_DIR.resolve()}")
plt.show()
