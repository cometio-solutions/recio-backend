"""Module for functions that generate report"""
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from rest.models.recruitment import Recruitment


def generate_recruitment_year_report(year):
    """
    Gets all recruitments from a certain year and returns path to a pdf file
    created from it.

    :param year: year of recruitment
    :return: path to pdf file or 404 if found no recruitments for the year
    """
    all_recruitments = Recruitment.query.all()

    recruitments = []
    for rec in all_recruitments:
        summary = Recruitment.get_cycles_summary([rec])
        rec_json = Recruitment.to_json(rec, summary['overall_candidates_num'])

        if rec_json['end_date'].split(',')[0].split('/')[2] == str(year):
            recruitments.append(rec_json)

    if len(recruitments) == 0:
        return 404

    plot_data = []
    for rec in recruitments:
        plot_data.append([
            rec['slot_limit'],
            rec['candidates_num'],
            rec['point_limit'],
            rec['faculty'],
            rec['degree'],
            rec['major_name'],
            rec['major_mode']
        ])

    columns = ['Liczba miejsc', 'Liczba kandydatów', 'Limit punktów', 'Wydział',
               'Stopień', 'Nazwa kierunku', 'Tryb studiów']

    with PdfPages("rest/recruitment_year.pdf") as pdf:
        current_row = 0
        row_limit = 21

        while current_row < len(plot_data):
            fig, axes = plt.subplots()

            fig.patch.set_visible(False)
            axes.xaxis.set_visible(False)
            axes.yaxis.set_visible(False)

            if current_row + row_limit < len(plot_data):
                last_row = current_row + row_limit
            else:
                last_row = len(plot_data)

            rec_table = axes.table(
                cellText=plot_data[current_row:last_row],
                colLabels=columns,
                loc='center',
                cellLoc='center'
            )

            for i in range(len(columns)):
                rec_table[(0, i)].set_facecolor("#56b5fd")

            if current_row == 0:
                plt.title(f'Recruitments for year {year}')

            pdf.savefig()
            plt.close()

            current_row += row_limit

    return "recruitment_year.pdf"
