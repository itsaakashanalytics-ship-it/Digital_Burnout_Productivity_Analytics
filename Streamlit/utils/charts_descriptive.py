import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==========================
# Color Palette
# ==========================
BLUE = "#457B9D"
GREEN = "#2EC4B6"
RED = "#E63946"
ORANGE = "#F4A300"


# ==========================================================
# D2. Average Digital Habit Hours
# ==========================================================
def plot_d2(df):
    """
    Returns:
        fig : matplotlib figure
    """

    d2 = (
        df[
            [
                "DAILY_SCREEN_TIME",
                "SOCIAL_MEDIA_HOURS",
                "DOOMSCROLLING_DURATION",
            ]
        ]
        .agg(["mean", "median", "std"])
        .round(2)
    )

    means = d2.loc["mean"]

    labels = [
        "Screen Time",
        "Social Media",
        "Doomscrolling",
    ]

    fig, ax = plt.subplots(figsize=(6, 4))

    bars = ax.bar(
        labels,
        means.values,
        color=[BLUE, GREEN, RED],
        edgecolor="black",
        linewidth=0.7,
    )

    for bar, value in zip(bars, means.values):

        height = bar.get_height()

        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"{value:.2f} hrs",
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold",
        )

    ax.set_title(
        "D2. Average Digital-Habit Hours",
        fontsize=13,
        fontweight="bold",
        pad=15,
    )

    ax.set_ylabel(
        "Hours / Day",
        fontsize=11,
        fontweight="bold",
    )

    ax.grid(axis="y", alpha=0.30)

    fig.tight_layout()

    return fig

# ==========================================================
# D3. Sleep Hours Distribution
# ==========================================================
def plot_d3(df):
    """
    Returns
    -------
    matplotlib.figure.Figure
    """

    sleep_mean = round(df["SLEEP_HOURS"].mean(), 2)
    sleep_median = round(df["SLEEP_HOURS"].median(), 2)
    sleep_quality = round(df["SLEEP_QUALITY"].mean(), 2)

    fig, ax = plt.subplots(figsize=(13, 10))

    n, bins, patches = ax.hist(
        df["SLEEP_HOURS"],
        bins=20,
        color=BLUE,
        edgecolor="black",
        linewidth=0.7,
    )

    # Count labels
    for count, patch in zip(n, patches):

        height = patch.get_height()

        if height > 0:
            ax.text(
                patch.get_x() + patch.get_width() / 2,
                height,
                f"{int(count):,}",
                ha="center",
                va="bottom",
                fontsize=8,
                fontweight="bold",
            )

    stats_text = (
        f"Mean: {sleep_mean} hrs\n"
        f"Median: {sleep_median} hrs\n"
        f"Quality: {sleep_quality}/10\n"
        f"n = {len(df):,}"
    )

    ax.text(
        0.98,
        0.97,
        stats_text,
        transform=ax.transAxes,
        fontsize=10,
        fontweight="bold",
        verticalalignment="top",
        horizontalalignment="right",
        bbox=dict(
            boxstyle="round",
            facecolor="lightblue",
            alpha=0.7,
        ),
    )

    ax.set_title(
        "D3. Sleep Hours Distribution",
        fontsize=13,
        fontweight="bold",
        pad=15,
    )

    ax.set_xlabel(
        "Sleep Hours",
        fontsize=10,
        fontweight="bold",
    )

    ax.set_ylabel(
        "Employee-Day Count",
        fontsize=10,
        fontweight="bold",
    )

    ax.grid(axis="y", alpha=0.30)

    fig.tight_layout()

    return fig
# ==========================================================
# D4. Mental State Breakdown
# ==========================================================
def plot_d4(df):
    """
    Returns
    -------
    matplotlib.figure.Figure
    """

    d4 = df["MENTAL_STATE"].value_counts()

    fig, ax = plt.subplots(figsize=(5, 5))

    colors = [
        RED,
        BLUE,
        GREEN,
        ORANGE,
    ]

    wedges, texts, autotexts = ax.pie(
        d4.values,
        labels=d4.index,
        autopct="%1.1f%%",
        colors=colors,
        startangle=90,
        textprops={
            "fontsize": 11,
            "fontweight": "bold",
        },
    )

    # Percentage text styling
    for autotext in autotexts:
        autotext.set_color("white")
        autotext.set_fontsize(11)
        autotext.set_fontweight("bold")

    # Count labels outside slices
    for i, (label, count) in enumerate(zip(d4.index, d4.values)):

        angle = (wedges[i].theta1 + wedges[i].theta2) / 2

        x = 1.30 * np.cos(np.radians(angle))
        y = 1.30 * np.sin(np.radians(angle))

        ax.text(
            x,
            y,
            f"n={count:,}",
            ha="center",
            va="center",
            fontsize=9,
            fontweight="bold",
        )

    ax.set_title(
        "D4. Mental State Breakdown",
        fontsize=13,
        fontweight="bold",
        pad=15,
    )

    fig.tight_layout()

    return fig
# ==========================================================
# D5. Productivity Category
# ==========================================================
def plot_d5(df):
    """
    Returns
    -------
    matplotlib.figure.Figure
    """

    d5 = (
        df.groupby("PRODUCTIVITY_CATEGORY")["PRODUCTIVITY_SCORE"]
        .agg(["count", "mean"])
        .round(2)
        .sort_values("mean", ascending=False)
    )

    fig, ax = plt.subplots(figsize=(5, 4))

    bars = ax.bar(
        d5.index,
        d5["mean"],
        color=GREEN,
        edgecolor="black",
        linewidth=0.7,
    )

    for bar, (_, row) in zip(bars, d5.iterrows()):

        height = bar.get_height()

        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"{height:.2f}\n(n={int(row['count']):,})",
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
        )

    ax.set_title(
        "D5. Average Productivity Score by Category",
        fontsize=13,
        fontweight="bold",
        pad=15,
    )

    ax.set_xlabel(
        "Productivity Category",
        fontsize=11,
        fontweight="bold",
    )

    ax.set_ylabel(
        "Average Productivity Score",
        fontsize=11,
        fontweight="bold",
    )

    ax.set_ylim(0, 110)

    ax.grid(axis="y", alpha=0.30)

    fig.tight_layout()

    return fig

# ==========================================================
# D6. Average Daily Interruption Load
# ==========================================================
def plot_d6(df):
    """
    Returns
    -------
    matplotlib.figure.Figure
    """

    d6 = (
        df[
            [
                "NOTIFICATION_COUNT",
                "SMARTPHONE_UNLOCKS",
                "APP_SWITCH_FREQUENCY",
            ]
        ]
        .mean()
        .round(0)
    )

    fig, ax = plt.subplots(figsize=(5, 4))

    bars = ax.bar(
        [
            "Notifications",
            "Unlocks",
            "App Switches",
        ],
        d6.values,
        color=ORANGE,
        edgecolor="black",
        linewidth=0.7,
    )

    for bar, value in zip(bars, d6.values):

        height = bar.get_height()

        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 2,
            f"{value:.0f}",
            ha="center",
            va="bottom",
            fontsize=12,
            fontweight="bold",
        )

    ax.set_ylim(0, max(d6.values) * 1.15)

    ax.set_title(
        "D6. Average Daily Interruption Load",
        fontsize=13,
        fontweight="bold",
        pad=15,
    )

    ax.set_ylabel(
        "Count / Day",
        fontsize=11,
        fontweight="bold",
    )

    fig.tight_layout()

    return fig

# ==========================================================
# D7. Average Stress & Fatigue Indicators
# ==========================================================
def plot_d7(df):
    """
    Returns
    -------
    matplotlib.figure.Figure
    """

    d7 = (
        df[
            [
                "STRESS_LEVEL",
                "MENTAL_FATIGUE",
                "EMOTIONAL_EXHAUSTION",
            ]
        ]
        .mean()
        .round(2)
    )

    labels = [
        "Stress",
        "Mental Fatigue",
        "Emotional Exhaustion",
    ]

    fig, ax = plt.subplots(figsize=(5, 4))

    bars = ax.bar(
        labels,
        d7.values,
        color=RED,
        edgecolor="black",
        linewidth=0.7,
    )

    # Value Labels
    for bar, value in zip(bars, d7.values):

        height = bar.get_height()

        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"{value:.2f}/10",
            ha="center",
            va="bottom",
            fontsize=12,
            fontweight="bold",
        )

    ax.set_title(
        "D7. Average Stress & Fatigue Indicators",
        fontsize=13,
        fontweight="bold",
        pad=15,
    )

    ax.set_ylabel(
        "Score (1–10)",
        fontsize=11,
        fontweight="bold",
    )

    ax.set_ylim(0, d7.max() * 1.15)

    ax.grid(axis="y", alpha=0.30)

    fig.tight_layout()

    return fig
