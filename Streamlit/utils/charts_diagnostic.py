import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

BLUE = "#457B9D"
GREEN = "#2EC4B6"
RED = "#E63946"
ORANGE = "#F4A300"


# ==========================================================
# G1. Burnout Risk vs Productivity Score
# ==========================================================
def plot_g1(df):
    """
    Returns
    -------
    matplotlib.figure.Figure
    """

    corr_g1 = df["BURNOUT_RISK"].corr(df["PRODUCTIVITY_SCORE"])

    sample = df[
        [
            "BURNOUT_RISK",
            "PRODUCTIVITY_SCORE",
        ]
    ].sample(
        frac=0.002,
        random_state=42,
    )

    fig, ax = plt.subplots(figsize=(6, 6))

    ax.scatter(
        sample["BURNOUT_RISK"],
        sample["PRODUCTIVITY_SCORE"],
        alpha=0.4,
        s=15,
        color=RED,
        edgecolors="none",
    )

    # Trend line
    z = np.polyfit(
        sample["BURNOUT_RISK"].astype(float),
        sample["PRODUCTIVITY_SCORE"].astype(float),
        1,
    )

    p = np.poly1d(z)

    x = np.linspace(
        float(sample["BURNOUT_RISK"].min()),
        float(sample["BURNOUT_RISK"].max()),
        100,
    )

    ax.plot(
        x,
        p(x),
        "b--",
        linewidth=2,
        alpha=0.7,
        label="Trend Line",
    )

    info = (
        f"Correlation: {corr_g1:.4f}\n"
        f"Sample Size: {len(sample):,}\n"
        f"Interpretation: Strong Negative"
    )

    ax.text(
        0.05,
        0.95,
        info,
        transform=ax.transAxes,
        fontsize=10,
        fontweight="bold",
        verticalalignment="top",
        bbox=dict(
            boxstyle="round",
            facecolor="lightyellow",
            alpha=0.7,
        ),
    )

    ax.set_title(
        "G1. Burnout Risk vs. Productivity Score",
        fontsize=13,
        fontweight="bold",
        pad=15,
    )

    ax.set_xlabel(
        "Burnout Risk",
        fontsize=11,
        fontweight="bold",
    )

    ax.set_ylabel(
        "Productivity Score",
        fontsize=11,
        fontweight="bold",
    )

    ax.grid(True, alpha=0.3)

    ax.legend()

    fig.tight_layout()

    return fig
# ==========================================================
# G2. Screen Time vs Burnout Risk
# ==========================================================
def plot_g2(df):
    """
    Returns
    -------
    matplotlib.figure.Figure
    """

    corr_g2 = df["DAILY_SCREEN_TIME"].corr(df["BURNOUT_RISK"])

    sample = df[
        [
            "DAILY_SCREEN_TIME",
            "BURNOUT_RISK",
        ]
    ].sample(
        frac=0.002,
        random_state=42,
    )

    fig, ax = plt.subplots(figsize=(8, 6))

    ax.scatter(
        sample["DAILY_SCREEN_TIME"],
        sample["BURNOUT_RISK"],
        alpha=0.4,
        s=15,
        color=BLUE,
        edgecolors="none",
    )

    # Trend Line
    z = np.polyfit(
        sample["DAILY_SCREEN_TIME"].astype(float),
        sample["BURNOUT_RISK"].astype(float),
        1,
    )

    p = np.poly1d(z)

    x = np.linspace(
        float(sample["DAILY_SCREEN_TIME"].min()),
        float(sample["DAILY_SCREEN_TIME"].max()),
        100,
    )

    ax.plot(
        x,
        p(x),
        "r--",
        linewidth=2,
        alpha=0.7,
        label="Trend Line",
    )

    info = (
        f"Correlation: {corr_g2:.4f}\n"
        f"Sample Size: {len(sample):,}\n"
        f"Interpretation: Moderate Positive"
    )

    ax.text(
        0.05,
        0.95,
        info,
        transform=ax.transAxes,
        fontsize=10,
        fontweight="bold",
        verticalalignment="top",
        bbox=dict(
            boxstyle="round",
            facecolor="lightyellow",
            alpha=0.7,
        ),
    )

    ax.set_title(
        "G2. Screen Time vs. Burnout Risk",
        fontsize=13,
        fontweight="bold",
        pad=15,
    )

    ax.set_xlabel(
        "Daily Screen Time (hrs)",
        fontsize=11,
        fontweight="bold",
    )

    ax.set_ylabel(
        "Burnout Risk",
        fontsize=11,
        fontweight="bold",
    )

    ax.grid(True, alpha=0.3)

    ax.legend()

    fig.tight_layout()

    return fig
# ==========================================================
# G3. Sleep Hours vs Burnout Risk
# ==========================================================
def plot_g3(df):
    """
    Returns
    -------
    matplotlib.figure.Figure
    """

    corr_g3 = df["SLEEP_HOURS"].corr(df["BURNOUT_RISK"])

    sample = df[
        [
            "SLEEP_HOURS",
            "BURNOUT_RISK",
        ]
    ].sample(
        frac=0.002,
        random_state=42,
    )

    fig, ax = plt.subplots(figsize=(8, 6))

    ax.scatter(
        sample["SLEEP_HOURS"],
        sample["BURNOUT_RISK"],
        alpha=0.4,
        s=15,
        color=GREEN,
        edgecolors="none",
    )

    # Trend Line
    z = np.polyfit(
        sample["SLEEP_HOURS"].astype(float),
        sample["BURNOUT_RISK"].astype(float),
        1,
    )

    p = np.poly1d(z)

    x = np.linspace(
        float(sample["SLEEP_HOURS"].min()),
        float(sample["SLEEP_HOURS"].max()),
        100,
    )

    ax.plot(
        x,
        p(x),
        "r--",
        linewidth=2,
        alpha=0.7,
        label="Trend Line",
    )

    info = (
        f"Correlation: {corr_g3:.4f}\n"
        f"Sample Size: {len(sample):,}\n"
        f"Interpretation: Strong Negative"
    )

    ax.text(
        0.05,
        0.95,
        info,
        transform=ax.transAxes,
        fontsize=10,
        fontweight="bold",
        verticalalignment="top",
        bbox=dict(
            boxstyle="round",
            facecolor="lightyellow",
            alpha=0.7,
        ),
    )

    ax.set_title(
        "G3. Sleep Hours vs. Burnout Risk",
        fontsize=13,
        fontweight="bold",
        pad=15,
    )

    ax.set_xlabel(
        "Sleep Hours",
        fontsize=11,
        fontweight="bold",
    )

    ax.set_ylabel(
        "Burnout Risk",
        fontsize=11,
        fontweight="bold",
    )

    ax.grid(True, alpha=0.30)

    ax.legend()

    fig.tight_layout()

    return fig
# ==========================================================
# G4. Average Burnout Risk by Occupation
# ==========================================================
def plot_g4(df):
    """
    Returns
    -------
    matplotlib.figure.Figure
    """

    g4 = (
        df.groupby("OCCUPATION")["BURNOUT_RISK"]
        .mean()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(9, 6))

    bars = ax.barh(
        g4.index[::-1],
        g4.values[::-1],
        color=BLUE,
        edgecolor="black",
        linewidth=0.7,
    )

    # Value labels
    for bar, value in zip(bars, g4.values[::-1]):

        width = bar.get_width()

        ax.text(
            width,
            bar.get_y() + bar.get_height() / 2,
            f"{value:.2f}",
            ha="left",
            va="center",
            fontsize=11,
            fontweight="bold",
            bbox=dict(
                boxstyle="round,pad=0.3",
                facecolor="white",
                alpha=0.7,
            ),
        )

    ax.set_title(
        "G4. Average Burnout Risk by Occupation",
        fontsize=13,
        fontweight="bold",
        pad=15,
    )

    ax.set_xlabel(
        "Average Burnout Risk",
        fontsize=11,
        fontweight="bold",
    )

    ax.grid(axis="x", alpha=0.30)

    ax.set_xlim(0, g4.max() + 6)

    fig.tight_layout()

    return fig

# ==========================================================
# G5. Focused vs Burnout Comparison
# ==========================================================
def plot_g5(df):
    """
    Returns
    -------
    matplotlib.figure.Figure
    """

    g5 = (
        df[df["MENTAL_STATE"].isin(["Focused", "Burnout"])]
        .groupby("MENTAL_STATE")[
            [
                "PRODUCTIVITY_SCORE",
                "DAILY_SCREEN_TIME",
                "SLEEP_HOURS",
                "STRESS_LEVEL",
            ]
        ]
        .mean()
        .round(2)
    )

    metrics = [
        "PRODUCTIVITY_SCORE",
        "DAILY_SCREEN_TIME",
        "SLEEP_HOURS",
        "STRESS_LEVEL",
    ]

    labels = [
        "Productivity",
        "Screen Time",
        "Sleep Hrs",
        "Stress",
    ]

    x = np.arange(len(metrics))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 4))

    bars1 = ax.bar(
        x - width / 2,
        g5.loc["Focused", metrics],
        width,
        label="Focused",
        color=GREEN,
        edgecolor="black",
        linewidth=0.7,
    )

    bars2 = ax.bar(
        x + width / 2,
        g5.loc["Burnout", metrics],
        width,
        label="Burnout",
        color=RED,
        edgecolor="black",
        linewidth=0.7,
    )

    # Value Labels
    for bars in [bars1, bars2]:

        for bar in bars:

            height = bar.get_height()

            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                f"{height:.2f}",
                ha="center",
                va="bottom",
                fontsize=9,
                fontweight="bold",
            )

    ax.set_xticks(x)
    ax.set_xticklabels(labels)

    ax.set_title(
        "G5. Focused vs. Burnout: Habit & Outcome Comparison",
        fontsize=13,
        fontweight="bold",
        pad=15,
    )

    ax.set_ylabel(
        "Value",
        fontsize=11,
        fontweight="bold",
    )

    ax.legend(fontsize=10)

    ax.grid(axis="y", alpha=0.30)

    fig.tight_layout()

    return fig
# ==========================================================
# G6. Productivity Driver Correlations
# ==========================================================
def plot_g6(df):
    """
    Returns
    -------
    matplotlib.figure.Figure
    """

    habit_cols = [
        "DAILY_SCREEN_TIME",
        "SOCIAL_MEDIA_HOURS",
        "SLEEP_HOURS",
        "STRESS_LEVEL",
        "DEEP_WORK_HOURS",
        "NOTIFICATION_COUNT",
    ]

    g6 = (
        df[habit_cols + ["PRODUCTIVITY_SCORE"]]
        .corr()["PRODUCTIVITY_SCORE"]
        .drop("PRODUCTIVITY_SCORE")
    )

    g6 = g6.reindex(
        g6.abs()
        .sort_values(ascending=False)
        .index
    ).round(3)

    colors = [
        GREEN if value > 0 else RED
        for value in g6.values
    ]

    fig, ax = plt.subplots(figsize=(7, 5))

    bars = ax.barh(
        g6.index[::-1],
        g6.values[::-1],
        color=colors[::-1],
        edgecolor="black",
        linewidth=0.7,
    )

    # Value Labels
    for bar, value in zip(bars, g6.values[::-1]):

        width = bar.get_width()

        if width >= 0:

            ax.text(
                width + 0.01,
                bar.get_y() + bar.get_height() / 2,
                f"{value:.3f}",
                ha="left",
                va="center",
                fontsize=10,
                fontweight="bold",
            )

        else:

            ax.text(
                width - 0.01,
                bar.get_y() + bar.get_height() / 2,
                f"{value:.3f}",
                ha="right",
                va="center",
                fontsize=10,
                fontweight="bold",
            )

    ax.axvline(
        0,
        color="black",
        linewidth=1.2,
    )

    ax.set_xlim(-0.30, 0.70)

    ax.set_title(
        "G6. Habit Correlation with Productivity Score (Ranked)",
        fontsize=13,
        fontweight="bold",
        pad=18,
    )

    ax.set_xlabel(
        "Correlation Coefficient",
        fontsize=11,
        fontweight="bold",
    )

    ax.grid(
        axis="x",
        alpha=0.20,
    )

    fig.tight_layout()

    return fig
