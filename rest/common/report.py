"""Module for functions that generate report"""
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from rest.models.recruitment import Recruitment


def get_plot_date(recruitments):
    """
    Helper function for report generating

    :param recruitments: recruitmens
    :return: data used in plotting the report
    """
    plot_data = []
    for _, rec in enumerate(recruitments):
        major_name = rec['major_name']
        split_major_name = major_name.split(' ')
        if len(split_major_name) > 3:
            count = 0
            major_name = ''
            for word in split_major_name:
                major_name += word
                if count == 1:
                    major_name += '\n'
                else:
                    major_name += ' '
                count += 1

        plot_data.append([
            rec['slot_limit'],
            rec['candidates_num'],
            rec['point_limit'],
            rec['faculty'],
            '1' if 'pierwszego' in rec['degree'] else '2',
            major_name,
            rec['major_mode'].replace('Studia', '').strip()
        ])

    return plot_data


def generate_recruitment_year_report(year):
    """
    Gets all recruitments from a certain year and returns path to a pdf file
    created from it.

    :param year: year of recruitment
    :return: path to pdf file or 404 if found no recruitments for the year
    """
    recruitments = []
    for rec in Recruitment.query.all():
        summary = Recruitment.get_cycles_summary([rec])
        rec_json = Recruitment.to_json(rec, summary['overall_candidates_num'])

        if rec_json['end_date'].split(',')[0].split('/')[2] == str(year):
            recruitments.append(rec_json)

    if len(recruitments) == 0:
        return 404

    plot_data = get_plot_date(recruitments)

    columns = ['Liczba\nmiejsc', 'Liczba\nkandydatów', 'Limit\npunktów', 'Wydział',
               'Stopień', 'Nazwa kierunku', 'Tryb\nstudiów']

    with PdfPages("rest/recruitment_year.pdf") as pdf:
        current_row = 0
        row_limit = 24

        while current_row < len(plot_data):
            fig, axes = plt.subplots(figsize=(8.27, 11.69))

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
                loc='upper center',
                cellLoc='center'
            )

            rec_table.auto_set_font_size(False)
            rec_table.auto_set_column_width([0, 1, 2, 3, 4, 5, 6])
            rec_table.set_fontsize(9)

            for i in range(len(columns)):
                rec_table[(0, i)].set_facecolor("#56b5fd")
                rec_table[(0, i)].set_height(.025)

            rec_table.scale(1, 2)

            if current_row == 0:
                plt.title(f'Rekrutacje na rok {year}')

            pdf.savefig()
            plt.close()

            current_row += row_limit

    return "recruitment_year.pdf"
