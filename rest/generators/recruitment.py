"""
This script generates plots from recruitment data and saves them as pdf file
"""
import logging
import matplotlib.pyplot as plt
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

    if not labels:
        return ""

    fig, axes = plt.subplots()

    labels_num = len(labels)

    x_pos = list(range(labels_num))
    bar_width = 3.0 / labels_num - 0.1

    idx = 0

    max_val = 0

    bars = []

    for label, value in kwargs.items():
        bars.append(axes.bar(
                [x + idx * bar_width for x in x_pos],
                value,
                bar_width,
                label=label
            )
        )
        idx += 1
        max_val = max(max_val, max(value))

    axes.set_ylabel(y_label)
    axes.set_title(chart_name)
    axes.set_xticks([x + bar_width * (len(kwargs) - 1) / 2 for x in x_pos])
    axes.set_ylim([0, int(1.3 * max_val)])
    axes.set_xticklabels(labels, rotation=45, size=3)
    axes.legend()

    fig.tight_layout()

    return fig


def generate_plots(recruitment_data):
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
    recruitment_data

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

    with PdfPages("rest/recruitment.pdf") as pdf:
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
