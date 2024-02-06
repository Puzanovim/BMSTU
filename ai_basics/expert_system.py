import pandas as pd
import numpy as np
from numpy.linalg import norm


whiskey_columns = [
    'name',
    'brand',
    'sort',
    'extract',
    'concentration',
    'country',
]

names = np.array([
    ['Scotch 1'],
    ['Scotch 2'],
    ['Scotch 3'],
    ['Irish 1'],
    ['Irish 2'],
    ['Irish 3'],
    ['Bourbon 1'],
    ['Bourbon 2'],
    ['Bourbon 3'],
])


data = np.array([
    # scotch
    [1, 10, 3, 0.60, 1],
    [2, 10, 5, 0.55, 1],
    [3, 10, 10, 0.62, 1],
    # irish
    [4, 20, 3, 0.55, 2],
    [5, 20, 4, 0.53, 2],
    [6, 20, 5, 0.57, 2],
    # bourbon
    [7, 30, 3, 0.40, 3],
    [8, 30, 4, 0.55, 3],
    [9, 30, 4, 0.53, 3],
])

user_scores = {}

HELP_TEXT = 'You can use next commands:\n' \
            'help - print this notice\n' \
            'end - end the session\n' \
            'add_score - add user score to drink\n' \
            'get_advice - get advice from the system.'

num_to_sort = {
    10: 'Scotch',
    20: 'Irish',
    30: 'Bourbon'
}

sort_to_methods = {
    10: 'Drink with a little bit of water or ice. Without snacks.',
    20: 'Drink in its purest form. Without water, ice and snacks.',
    30: 'Drink with fruits or fruits juices. Also you can drink with snacks.'
}

num_to_country = {
    1: 'Scotland',
    2: 'Ireland',
    3: 'USA'
}

def print_drink(drink: np.ndarray) -> None:
    text = ''
    using_methods = None
    for col, value in zip(whiskey_columns, drink):
        match col:
            case 'name':
                text += f'{value}: '
            case 'brand':
                text += f'{names[int(float(value)) - 1][0]} '
            case 'sort':
                text += f'is {num_to_sort[int(float(value))]} '
                using_methods = sort_to_methods[int(float(value))]
            case 'extract':
                text += f'with {int(float(value))} years extract '
            case 'concentration':
                text += f'and {int(float(value) * 100)} C '
            case 'country':
                text += f'from {num_to_country[int(float(value))]}. '

    print(text)
    if using_methods is not None:
        print(f'We recommend the following methods of use: {using_methods}')


def main():
    print(f'Hello! Welcome to WhiskyAdvisor!\n{HELP_TEXT}')

    df_data = np.hstack((names, data))
    df = pd.DataFrame(df_data, columns=whiskey_columns)

    norms = np.zeros((len(data), len(data)))
    for i in range(len(data)):
        for j in range(len(data)):
            norms[i, j] = norm(data[i] - data[j], ord=1)

    max_norm = norms.max()
    norms = max_norm - norms


    while True:
        command = input('\nEnter a command: ')
        match command:
            case 'help':
                print(HELP_TEXT)
            case 'end':
                break
            case 'add_score':
                for i, name in enumerate(names):
                    print(f'№{i} Name: {name[0]}')
                key = int(input('Enter number of drink: '))
                value = int(input('Enter drink score from 0 to 10: '))
                user_scores[key] = value
            case 'get_advice':
                for key, score in user_scores.items():
                    norms[int(key)] *= score

                recommendations = np.zeros((len(data),))

                for i in range(len(data)):
                    recommendations[i] = norms[:, i].max()

                recommendations_dict = {i: recommendations[i] for i in range(len(data))}
                sorted_recommendations_keys = sorted(recommendations_dict, key=recommendations_dict.get, reverse=True)
                for key in sorted_recommendations_keys:
                    print_drink(df.iloc[key].values)

    print('Good bye!')


if __name__ == '__main__':
    main()
