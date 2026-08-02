import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import roc_curve

BLUE = "#457B9D"
GREEN = "#2EC4B6"
RED = "#E63946"
ORANGE = "#F4A300"


# ==========================================================
# P1. Confusion Matrix
# ==========================================================
def plot_confusion_matrix(cm):
    """
    Parameters
    ----------
    cm : ndarray
        sklearn confusion matrix

    Returns
    -------
    matplotlib.figure.Figure
    """

    fig, ax = plt.subplots(figsize=(5, 5))

    im = ax.imshow(
        cm,
        cmap="Blues",
    )

    ax.set_title(
        "Confusion Matrix - High Burnout Risk",
        fontsize=13,
        fontweight="bold",
        pad=15,
    )

    ax.set_xlabel(
        "Predicted",
        fontsize=11,
        fontweight="bold",
    )

    ax.set_ylabel(
        "Actual",
        fontsize=11,
        fontweight="bold",
    )

    ax.set_xticks([0, 1])
    ax.set_xticklabels(
        [
            "Not High Risk",
            "High Risk",
        ]
    )

    ax.set_yticks([0, 1])
    ax.set_yticklabels(
        [
            "Not High Risk",
            "High Risk",
        ]
    )

    threshold = cm.max() / 2

    for i in range(cm.shape[0]):

        for j in range(cm.shape[1]):

            ax.text(
                j,
                i,
                f"{cm[i, j]}",
                ha="center",
                va="center",
                fontsize=14,
                fontweight="bold",
                color="white" if cm[i, j] > threshold else "black",
            )

    fig.colorbar(im)

    fig.tight_layout()

    return fig
# ==========================================================
# P2. ROC Curve
# ==========================================================
def plot_roc_curve(y_test, y_proba, auc):
    """
    Parameters
    ----------
    y_test : array-like
    y_proba : array-like
    auc : float

    Returns
    -------
    matplotlib.figure.Figure
    """

    fpr, tpr, _ = roc_curve(y_test, y_proba)

    fig, ax = plt.subplots(figsize=(6, 6))

    ax.plot(
        fpr,
        tpr,
        color=RED,
        linewidth=2,
        label=f"ROC Curve (AUC = {auc:.3f})",
    )

    ax.plot(
        [0, 1],
        [0, 1],
        linestyle="--",
        color="gray",
        linewidth=1.5,
        label="Random Guess",
    )

    ax.set_title(
        "ROC Curve - High Burnout Risk Model",
        fontsize=13,
        fontweight="bold",
        pad=15,
    )

    ax.set_xlabel(
        "False Positive Rate",
        fontsize=11,
        fontweight="bold",
    )

    ax.set_ylabel(
        "True Positive Rate",
        fontsize=11,
        fontweight="bold",
    )

    ax.grid(alpha=0.30)

    ax.legend(
        loc="lower right",
        fontsize=10,
    )

    fig.tight_layout()

    return fig
# ==========================================================
# P3. Burnout Feature Importance
# ==========================================================
def plot_burnout_feature_importance(
    burnout_model,
    numeric_features,
    categorical_features,
):
    """
    Top 10 Logistic Regression Feature Coefficients

    Parameters
    ----------
    burnout_model : trained sklearn Pipeline
    numeric_features : list
    categorical_features : list

    Returns
    -------
    matplotlib.figure.Figure
    """

    feature_names = (
        numeric_features
        + list(
            burnout_model.named_steps["prep"]
            .named_transformers_["cat"]
            .get_feature_names_out(categorical_features)
        )
    )

    coefficients = (
        burnout_model.named_steps["model"]
        .coef_[0]
    )

    coef_df = pd.DataFrame(
        {
            "Feature": feature_names,
            "Coefficient": coefficients,
        }
    )

    coef_df = (
        coef_df.iloc[
            coef_df["Coefficient"]
            .abs()
            .sort_values(ascending=False)
            .index
        ]
        .head(10)
    )

    colors = [
        GREEN if value > 0 else RED
        for value in coef_df["Coefficient"]
    ]

    fig, ax = plt.subplots(figsize=(8, 5))

    bars = ax.barh(
        coef_df["Feature"][::-1],
        coef_df["Coefficient"][::-1],
        color=colors[::-1],
        edgecolor="black",
        linewidth=0.7,
    )

    # Value Labels
    for bar, value in zip(
        bars,
        coef_df["Coefficient"][::-1],
    ):

        width = bar.get_width()

        if width >= 0:

            ax.text(
                width,
                bar.get_y() + bar.get_height() / 2,
                f"{value:.3f}",
                ha="left",
                va="center",
                fontsize=10,
                fontweight="bold",
            )

        else:

            ax.text(
                width,
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
        linewidth=1,
    )

    ax.set_title(
        "Top 10 Feature Coefficients - Burnout Risk Model",
        fontsize=13,
        fontweight="bold",
        pad=15,
    )

    ax.set_xlabel(
        "Coefficient (Standardized Features)",
        fontsize=11,
        fontweight="bold",
    )

    ax.grid(
        axis="x",
        alpha=0.25,
    )

    fig.tight_layout()

    return fig
# ==========================================================
# P4. Actual vs Predicted Productivity Score
# ==========================================================
def plot_actual_vs_predicted(y_test, y_pred, r2):
    """
    Actual vs Predicted Productivity Score

    Parameters
    ----------
    y_test : array-like
    y_pred : array-like
    r2 : float

    Returns
    -------
    matplotlib.figure.Figure
    """

    rng = np.random.RandomState(42)

    sample_size = min(15000, len(y_test))

    sample_idx = rng.choice(
        len(y_test),
        size=sample_size,
        replace=False,
    )

    actual = np.asarray(y_test)[sample_idx]
    predicted = np.asarray(y_pred)[sample_idx]

    fig, ax = plt.subplots(figsize=(7, 6))

    ax.scatter(
        actual,
        predicted,
        alpha=0.25,
        s=8,
        color=GREEN,
    )

    min_val = min(actual.min(), predicted.min())
    max_val = max(actual.max(), predicted.max())

    ax.plot(
        [min_val, max_val],
        [min_val, max_val],
        linestyle="--",
        color="gray",
        linewidth=2,
        label="Perfect Prediction",
    )

    ax.set_title(
        f"Actual vs Predicted Productivity Score (R² = {r2:.2f})",
        fontsize=13,
        fontweight="bold",
        pad=15,
    )

    ax.set_xlabel(
        "Actual Productivity Score",
        fontsize=11,
        fontweight="bold",
    )

    ax.set_ylabel(
        "Predicted Productivity Score",
        fontsize=11,
        fontweight="bold",
    )

    ax.grid(alpha=0.30)

    ax.legend()

    fig.tight_layout()

    return fig
# ==========================================================
# P5. Residual Plot
# ==========================================================
def plot_residuals(y_test, y_pred):
    """
    Residual Plot

    Parameters
    ----------
    y_test : array-like
    y_pred : array-like

    Returns
    -------
    matplotlib.figure.Figure
    """

    rng = np.random.RandomState(42)

    sample_size = min(15000, len(y_test))

    sample_idx = rng.choice(
        len(y_test),
        size=sample_size,
        replace=False,
    )

    actual = np.asarray(y_test)[sample_idx].astype(float)
    predicted = np.asarray(y_pred)[sample_idx]

    residuals = actual - predicted

    fig, ax = plt.subplots(figsize=(7, 5))

    ax.scatter(
        predicted,
        residuals,
        alpha=0.25,
        s=8,
        color=RED,
    )

    ax.axhline(
        0,
        linestyle="--",
        color="gray",
        linewidth=2,
    )

    ax.set_title(
        "Residual Plot - Productivity Score Model",
        fontsize=13,
        fontweight="bold",
        pad=15,
    )

    ax.set_xlabel(
        "Predicted Productivity Score",
        fontsize=11,
        fontweight="bold",
    )

    ax.set_ylabel(
        "Residual (Actual - Predicted)",
        fontsize=11,
        fontweight="bold",
    )

    ax.grid(alpha=0.30)

    fig.tight_layout()

    return fig
# ==========================================================
# P6. Productivity Feature Importance
# ==========================================================
def plot_productivity_feature_importance(
    productivity_model,
    numeric_features,
    categorical_features,
):
    """
    Top 10 Linear Regression Feature Coefficients

    Parameters
    ----------
    productivity_model : trained sklearn Pipeline
    numeric_features : list
    categorical_features : list

    Returns
    -------
    matplotlib.figure.Figure
    """

    feature_names = (
        numeric_features
        + list(
            productivity_model.named_steps["prep"]
            .named_transformers_["cat"]
            .get_feature_names_out(categorical_features)
        )
    )

    coefficients = (
        productivity_model.named_steps["model"]
        .coef_
    )

    coef_df = pd.DataFrame(
        {
            "Feature": feature_names,
            "Coefficient": coefficients,
        }
    )

    coef_df = (
        coef_df.iloc[
            coef_df["Coefficient"]
            .abs()
            .sort_values(ascending=False)
            .index
        ]
        .head(10)
    )

    colors = [
        GREEN if value > 0 else RED
        for value in coef_df["Coefficient"]
    ]

    fig, ax = plt.subplots(figsize=(8, 5))

    bars = ax.barh(
        coef_df["Feature"][::-1],
        coef_df["Coefficient"][::-1],
        color=colors[::-1],
        edgecolor="black",
        linewidth=0.7,
    )

    for bar, value in zip(
        bars,
        coef_df["Coefficient"][::-1],
    ):

        width = bar.get_width()

        if width >= 0:

            ax.text(
                width,
                bar.get_y() + bar.get_height() / 2,
                f"{value:.3f}",
                ha="left",
                va="center",
                fontsize=10,
                fontweight="bold",
            )

        else:

            ax.text(
                width,
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
        linewidth=1,
    )

    ax.set_title(
        "Top 10 Feature Coefficients - Productivity Model",
        fontsize=13,
        fontweight="bold",
        pad=15,
    )

    ax.set_xlabel(
        "Coefficient (Standardized Features)",
        fontsize=11,
        fontweight="bold",
    )

    ax.grid(
        axis="x",
        alpha=0.25,
    )

    fig.tight_layout()

    return fig
