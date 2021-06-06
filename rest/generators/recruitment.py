"""
This script generates plots from recruitment data and saves them as pdf file
"""
import logging
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages


def column_chart(
        labels: list,
        chart_name: str,
        y_label: str,
        **kwargs):
    """
    Return matplotlib figure with given args
    Parameters
    ----------
    labels : list
    chart_name : str
    y_label : str

    Returns
    -------
    chart : matplotlib figure
    """

    fig, axes = plt.subplots()

    labels_num = len(labels)

    x_pos = np.arange(labels_num)
    bar_width = 1.0 / labels_num - 0.1

    idx = 0

    for label, value in kwargs.items():
        axes.bar(
            x_pos + idx * bar_width,
            value,
            bar_width,
            label=label
        )
        idx += 1

    axes.set_ylabel(y_label)
    axes.set_title(chart_name)
    axes.set_xticks(x_pos + bar_width * (labels_num - 1) / 2)
    axes.set_xticklabels(labels)
    axes.legend()
    fig.tight_layout()

    return fig


def generate_plots(recruitment_data: dict):
    """
    Generate plots for given recruitment data
    You have to provide given fields:
    {
        "major_name"
        "point_limit"
        "slot_limit"
        "candidates_num"
    }
    Parameters
    ----------
    recruitment_data : dict

    Returns
    -------
    path to pdf file : str
    """

    keys = ["major_name", "point_limit", "slot_limit", "candidates_num"]
    labels = []
    slot_limits = []
    point_limits = []
    candidates_num = []

    for rec in recruitment_data:
        if not all(key in rec for key in keys):
            logging.warning("Missing required fields!")
            return ""

        labels.append(rec['major_name'])
        slot_limits.append(rec['slot_limit'])
        point_limits.append(rec['point_limit'])
        candidates_num.append(rec['candidates_num'])

    with PdfPages("recruitment.pdf") as pdf:
        column_chart(labels=labels,
                     chart_name="Limit punktów do ilości kandydatów",
                     y_label="",
                     punkty=point_limits,
                     kandydaci=candidates_num)
        pdf.savefig()
        plt.close()
        column_chart(labels=labels,
                     chart_name="limit punktów do limitu miejsc",
                     y_label="",
                     punkty=point_limits,
                     miejsca=slot_limits)
        pdf.savefig()
        plt.close()
        column_chart(labels=labels,
                     chart_name="Limity punktów",
                     y_label="",
                     punkty=point_limits)
        pdf.savefig()
        plt.close()
        column_chart(labels=labels,
                     chart_name="Liczba miejsc",
                     y_label="",
                     miejsca=slot_limits)
        pdf.savefig()
        plt.close()
        column_chart(labels=labels,
                     chart_name="Liczba kandydatów",
                     y_label="",
                     kandydaci=candidates_num)
        pdf.savefig()
        plt.close()

    return "recruitment.pdf"
