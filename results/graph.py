import pandas as pd
import matplotlib.pyplot as plt
import itertools
from matplotlib.lines import Line2D


def read_data(n):
    """Finds the results for a run with N agents and returns a pandas dataframe"""
    return pd.read_json(f"N_{n}_output.json")


def redefine_rounds(old_rounds):
    """Redefines the bit integer into a bit array"""
    new_rounds = []
    for i in old_rounds:
        old_round = [char for char in str(i).zfill(5)]
        c = 0
        new_round = []
        for x in old_round:
            if int(x) == 1:
                c += 1
            new_round.append(c)
        new_rounds.append(new_round)
    return new_rounds


def calculate_average(l_all):
    """Calculates the average by the first column for a 2D-list"""
    l_avg = []
    for v in l_all:
        total = [0] * 5
        for single_list in v:
            for i, score in enumerate(single_list):
                total[i] += score
        avg = [t / 50 for t in total]
        l_avg.append(avg)

    return l_avg


def determine_style(sphok, rhok):
    """Determines the style in which to build a line"""
    if sphok:
        line = 'solid'
    else:
        line = 'dashed'
    if rhok:
        mark = 'o'
        marks = 8
        markc = 'green'
        z = 0
    else:
        mark = 's'
        marks = 5
        markc = 'red'
        z = 10

    return line, mark, marks, markc, z


def make_main_chart_5(df):
    """Produces the main line chart for 5 agents based on the dataframe"""
    # Make list of all combinations of variables
    s = [df['sphok'].unique(), df['rhok'].unique(), df['ps'].unique()]
    p = list(itertools.product(*s))

    # Find corresponding rounds won for each combination of variables
    l_all = []
    for combo in p:
        l_all.append(df.query(f'sphok == {combo[0]} and rhok == {combo[1]}'
                     f' and ps == "{str(combo[2])}"')['new_rounds_won'])

    l_avg = calculate_average(l_all)

    x = [1, 2, 3, 4, 5]
    plt.figure(figsize=(18, 12))
    legend_elements = [
        Line2D([0], [0], color='blue', label='PS = 2'),
        Line2D([0], [0], color='deeppink', label='PS = 3'),
        Line2D([0], [0], color='orange', label='PS = default'),
        Line2D([0], [0], linestyle='solid', label='SPHOK = True', color='black'),
        Line2D([0], [0], linestyle='dashed', label='SPHOK = False', color='black'),
        Line2D([0], [0], marker='o', mec='green', mfc='green',
               color='black', label='RHOK = True'),
        Line2D([0], [0], marker='s', mec='red', mfc='red', color='black', label='RHOK = False')
    ]
    for i in range(12):
        sphok, rhok, ps = p[i]
        line, mark, marks, markc, z = determine_style(sphok, rhok)
        if ps == '2':
            linec = 'blue'
        elif ps == '3':
            linec = 'deeppink'
        else:
            linec = 'orange'
        plt.plot(x, l_avg[i], linestyle=line, color=linec,
                 marker=mark, mec=markc, mfc=markc, ms=marks, zorder=z)
    plt.legend(handles=legend_elements, loc='upper left')
    plt.title('Results for N = 5')
    plt.xlabel('Mission number')
    plt.ylabel('Average number of missions won by spies')
    plt.xticks(x)
    plt.yticks(x)
    plt.savefig('figure_n5.png')
    plt.show()


def make_subcharts_5(df):
    """Divides the main chart into three charts for different party sizes"""
    s = [df['sphok'].unique(), df['rhok'].unique(), df['ps'].unique()]
    p = list(itertools.product(*s))
    l_all = []
    for combo in p:
        l_all.append(df.query(f'sphok == {combo[0]} and rhok == {combo[1]}'
                              f' and ps == "{str(combo[2])}"')['new_rounds_won'])

    l_avg = calculate_average(l_all)

    x = [1, 2, 3, 4, 5]
    legend_elements = [
        Line2D([0], [0], linestyle='solid', label='SPHOK = True', color='black'),
        Line2D([0], [0], linestyle='dashed', label='SPHOK = False', color='black'),
        Line2D([0], [0], marker='o', mec='green', mfc='green',
               color='black', label='RHOK = True'),
        Line2D([0], [0], marker='s', mec='red', mfc='red', color='black', label='RHOK = False')
    ]
    fig, axs = plt.subplots(1, 3, figsize=(22, 12))
    for i in range(12):
        sphok, rhok, ps = p[i]
        line, mark, marks, markc, z = determine_style(sphok, rhok)
        if ps == '2':
            axs[0].plot(x, l_avg[i], linestyle=line, color='blue',
                        marker=mark, mec=markc, mfc=markc, ms=marks, zorder=z)
        elif ps == '3':
            axs[1].plot(x, l_avg[i], linestyle=line, color='deeppink',
                        marker=mark, mec=markc, mfc=markc, ms=marks, zorder=z)
        else:
            axs[2].plot(x, l_avg[i], linestyle=line, color='orange',
                        marker=mark, mec=markc, mfc=markc, ms=marks, zorder=z)

    axs[0].set_title("PS = 2", fontsize=20)
    axs[0].legend(handles=legend_elements, loc='upper left', fontsize=20)
    axs[1].set_title("PS = 3", fontsize=20)
    axs[2].set_title("PS = default", fontsize=20)
    fig.suptitle("Main plot for N=5 divided into party size-plots", fontsize=20)
    for i in range(3):
        axs[i].set_xlabel("Mission number", fontsize=20)
        axs[i].set_ylabel('Average number of missions won by spies', fontsize=20)
        axs[i].set_yticks(x)
        axs[i].set_xticks(x)
        axs[i].xaxis.set_tick_params(labelsize=15)
        axs[i].yaxis.set_tick_params(labelsize=15)
    plt.savefig('figure_subn5.png')
    plt.show()


def make_line_chart_6(n5, n6):
    """Produces the line chart for 6 agents based on the dataframe"""
    s = [n5['sphok'].unique(), n5['rhok'].unique()]
    p = list(itertools.product(*s))
    l5 = []
    l6 = []
    for combo in p:
        l6.append(n6.query(f'sphok == {combo[0]} and rhok == {combo[1]}')['new_rounds_won'])
        l5.append(n5.query(f'sphok == {combo[0]} and rhok == {combo[1]} and '
                            f'ps == "def"')['new_rounds_won'])
    l5_avg = calculate_average(l5)
    l6_avg = calculate_average(l6)
    x = [1, 2, 3, 4, 5]
    fig, axs = plt.subplots(1, 2, figsize=(22, 12))
    legend_elements = [
        Line2D([0], [0], color='orange', label='PS = default'),
        Line2D([0], [0], linestyle='solid', label='SPHOK = True', color='black'),
        Line2D([0], [0], linestyle='dashed', label='SPHOK = False', color='black'),
        Line2D([0], [0], marker='o', mec='green', mfc='green',
               color='black', label='RHOK = True'),
        Line2D([0], [0], marker='s', mec='red', mfc='red', color='black', label='RHOK = False')
    ]
    for i in range(4):
        sphok, rhok = p[i]
        line, mark, marks, markc, z = determine_style(sphok, rhok)
        axs[0].plot(x, l5_avg[i], linestyle=line, color='orange',
                 marker=mark, mec=markc, mfc=markc, ms=marks, zorder=z)
        axs[1].plot(x, l6_avg[i], linestyle=line, color='orange',
                    marker=mark, mec=markc, mfc=markc, ms=marks, zorder=z)
    axs[0].legend(handles=legend_elements, loc='upper left')

    axs[0].set_title('Results for N = 5')
    for i in range(2):
        axs[i].set_xlabel("Mission number", fontsize=20)
        axs[i].set_ylabel('Average number of missions won by spies', fontsize=20)
        axs[i].set_yticks(x)
        axs[i].set_xticks(x)
        axs[i].xaxis.set_tick_params(labelsize=15)
        axs[i].yaxis.set_tick_params(labelsize=15)
    fig.suptitle("Plots for N = 5 and N = 6 with the default party size")
    plt.savefig('figure_n6.png')
    plt.show()


def main():
    n5 = read_data(5)
    n5['new_rounds_won'] = redefine_rounds(n5['rounds_won_spies'])
    make_main_chart_5(n5)
    make_subcharts_5(n5)
    n6 = read_data(6)
    n6['new_rounds_won'] = redefine_rounds(n6['rounds_won_spies'])
    make_line_chart_6(n5, n6)


if __name__ == "__main__":
    main()
