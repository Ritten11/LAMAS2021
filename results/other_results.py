import pandas as pd
import itertools


def read_data(n):
    """Finds the results for a run with N agents and returns a pandas dataframe"""
    return pd.read_json(f"N_{n}_output.json")


def get_numbers(nums):
    """Gets the number of rounds in which the spies aren't revealed and
    the average round number in which they were revealed (if they were revealed)"""
    no_reveal = 0
    num = 0
    den = 0
    for n in nums:
        if n == 0:
            no_reveal += 1
        else:
            num += n
            den += 1
    if den != 0:
        avg = num / den
    else:
        avg = 'NA'

    return no_reveal, avg



def get_results_5(df):
    """Builds the dataframe to put into markdown for N = 5"""
    s =[df['sphok'].unique(), df['rhok'].unique(), df['ps'].unique()]
    p = list(itertools.product(*s))
    new_df = pd.DataFrame(columns=['SPHOK', 'RHOK', 'PS', 'not revealed', 'average'])
    for i, combo in enumerate(p):
        nums = df.query(f'sphok == {combo[0]} and rhok == {combo[1]}'
                              f' and ps == "{str(combo[2])}"')['identity_revealed']
        no_reveal, avg = get_numbers(nums)
        new_df = new_df.append({'SPHOK': combo[0], 'RHOK': combo[1], 'PS': combo[2],
                        'not revealed': no_reveal, 'average':avg},ignore_index=True)

    return new_df

def get_results_6(df):
    """Builds the dataframe to put into markdown for N = 6"""
    s = [df['sphok'].unique(), df['rhok'].unique()]
    p = list(itertools.product(*s))
    new_df = pd.DataFrame(columns=['SPHOK', 'RHOK', 'not revealed', 'average'])
    for i, combo in enumerate(p):
        nums = df.query(f'sphok == {combo[0]} and rhok == {combo[1]}')['identity_revealed']
        no_reveal, avg = get_numbers(nums)
        new_df = new_df.append({'SPHOK': combo[0], 'RHOK': combo[1],
                                'not revealed': no_reveal, 'average': avg}, ignore_index=True)

    return new_df


def main():
    n5 = read_data(5)
    n6 = read_data(6)
    results5 = get_results_5(n5)
    results6 = get_results_6(n6)
    with open('identity_revealed_results.txt', 'w') as f:
        f.write(results5.to_markdown(index=False))
        f.write("\n\n")
        f.write(results6.to_markdown(index=False))

if __name__ == "__main__":
    main()
