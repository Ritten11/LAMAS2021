import pandas as pd
import itertools


def read_data(n):
    """Finds the results for a run with N agents and returns a pandas dataframe"""
    return pd.read_json(f"N_{n}_output.json")


def get_results(df1, df2):
    s1 = [df1['sphok'].unique(), df1['rhok'].unique(), df1['ps'].unique()]
    p1 = list(itertools.product(*s1))
    df = pd.DataFrame(columns=['N', 'SPHOK', 'RHOK', 'PS', 'not revealed', 'average'])

    for i, combo in enumerate(p1):
        numbers = df1.query(f'sphok == {combo[0]} and rhok == {combo[1]}'
                              f' and ps == "{str(combo[2])}"')['identity_revealed']
        no_reveal = 0
        num = 0
        den = 0
        for n in numbers:
            if n == 0:
                no_reveal += 1
            else:
                num += n
                den += 1
        if den != 0:
            avg = num / den
        else:
            avg = 0
        df = df.append({'N': 5, 'SPHOK': combo[0], 'RHOK': combo[1], 'PS': combo[2],
                        'not revealed': no_reveal, 'average':avg},ignore_index=True)

    s2 = [df1['sphok'].unique(), df1['rhok'].unique()]
    p2 = list(itertools.product(*s2))
    for j, combo2 in enumerate(p2):
        numbers = df2.query(f'sphok == {combo2[0]} and rhok == {combo2[1]}')['identity_revealed']
        no_reveal = 0
        num = 0
        den = 0
        for n in numbers:
            if n == 0:
                no_reveal += 1
            else:
                num += n
                den += 1
        if den != 0:
            avg = num / den
        else:
            avg = 0
        df = df.append({'N': 6, 'SPHOK': combo2[0], 'RHOK': combo2[1], 'PS': 'def',
                        'not revealed': no_reveal, 'average':avg}, ignore_index=True)

    return df


def main():
    n5 = read_data(5)
    n6 = read_data(6)
    results = get_results(n5, n6)
    with open('identity_revealed_results.txt', 'w') as f:
        f.write(results.to_markdown(index=False))

if __name__ == "__main__":
    main()
