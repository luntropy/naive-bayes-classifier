#!/usr/bin/python3

import random
import math

# Create the dataframes
def create_dfs(lines_count, size_df, adjustments_cnt):
    df = []
    itr = 0

    while itr < lines_count:
        if adjustments_cnt > 0:
            temp_list = data[itr:itr+size_df+1]
            adjustments_cnt = adjustments_cnt - 1
            itr = itr + size_df + 1
        else:
            temp_list = data[itr:itr+size_df]
            itr = itr + size_df

        df.append(temp_list)

    return df

# dfs_test[i] is the test df for the training df - dfs_train[i], where i = 0,..,k; k = 10 in our case
def separate_dfs(df, dfs_test, dfs_train):
    for frame in range(0, len(df)):
        dfs_test.append(df[frame])

        temp_df = []
        for i in range(0, len(df)):
            if i != frame:
                temp_df = temp_df + df[i]

        dfs_train.append(temp_df)

def train_model(index, dfs_train, democrat, republican):
    for i in range(1, 17):
        cnt_democrats = 0
        cnt_democrats_y = 0
        cnt_democrats_n = 0

        cnt_republicans = 0
        cnt_republicans_y = 0
        cnt_republicans_n = 0

        for j in range(0, len(dfs_train[index])):
            temp = dfs_train[index][j].split(',')

            if temp[0] == 'democrat':
                if temp[i] == 'y':
                    cnt_democrats_y = cnt_democrats_y + 1
                elif temp[i] == 'n':
                    cnt_democrats_n = cnt_democrats_n + 1
                else:
                    cnt_democrats = cnt_democrats + 1
            elif temp[0] == 'republican':
                if temp[i] == 'y':
                    cnt_republicans_y = cnt_republicans_y + 1
                elif temp[i] == 'n':
                    cnt_republicans_n = cnt_republicans_n + 1
                else:
                    cnt_republicans = cnt_republicans + 1

        if cnt_democrats_y == 0:
            cnt_democrats_y = 1
        elif cnt_democrats_n == 0:
            cnt_democrats_n = 1
        elif cnt_democrats == 0:
            cnt_democrats = 1

        total_democrats = cnt_democrats_y + cnt_democrats_n + cnt_democrats
        democrats_attr_dict = {}

        democrats_attr_dict['y'] = math.log(cnt_democrats_y / total_democrats)
        democrats_attr_dict['n'] = math.log(cnt_democrats_n / total_democrats)
        democrats_attr_dict['?'] = math.log(cnt_democrats / total_democrats)

        democrat[i] = democrats_attr_dict

        if cnt_republicans_y == 0:
            cnt_republicans_y = 1
        elif cnt_republicans_n == 0:
            cnt_republicans_n = 1
        elif cnt_republicans == 0:
            cnt_republicans = 1

        total_republicans = cnt_republicans_y + cnt_republicans_n + cnt_republicans
        republicans_attr_dict = {}

        republicans_attr_dict['y'] = math.log(cnt_republicans_y / total_republicans)
        republicans_attr_dict['n'] = math.log(cnt_republicans_n / total_republicans)
        republicans_attr_dict['?'] = math.log(cnt_republicans / total_republicans)

        republican[i] = republicans_attr_dict

def test_model_example(index, example, dfs_test, democrat, republican):
    test = dfs_test[index][example].split(',')

    res_d = 0
    res_r = 0
    for i in range(1, 16):
        res_d = res_d + democrat[i][test[i]]
        res_r = res_r + republican[i][test[i]]

    if res_d > res_r:
        res = [test[0], 'democrat']
    elif res_d < res_r:
        res = [test[0], 'republican']
    else:
        res = [test[0], 'none']

    return res

def test_model(index, dfs_test, dfs_train):
    democrat = {}
    republican = {}
    train_model(index, dfs_train, democrat, republican)

    res = []
    for example in range(0, len(dfs_test[index])):
        res.append(test_model_example(index, example, dfs_test, democrat, republican))

    return res

def k_fold_test_model(dfs_test, dfs_train):
    res = []
    for i in range(0, 10):
        res.append(test_model(i, dfs_test, dfs_train))

    return res

def print_accuracy(dfs_test, dfs_train):
    results = k_fold_test_model(dfs_test, dfs_train)

    model_num = 0
    average = 0
    for list in results:
        correct_democrat = 0
        correct_republican = 0
        wrong_democrat = 0
        wrong_republican = 0

        # # Calculate accuracy using Confusion Matrix
        # for res in list:
        #     if res[0] == 'democrat':
        #         if res[0] == res[1]:
        #             correct_democrat = correct_democrat + 1
        #         else:
        #             wrong_democrat = wrong_democrat + 1
        #     elif res[0] == 'republican':
        #         if res[0] == res[1]:
        #             correct_republican = correct_republican + 1
        #         else:
        #             wrong_republican = wrong_republican + 1
        #
        # percision = correct_democrat / (correct_democrat + wrong_republican)
        # sensitivity = correct_democrat / (correct_democrat + wrong_democrat)
        # specificity = correct_republican / (correct_republican + wrong_republican)
        # accuracy = (correct_democrat + correct_republican) / (correct_democrat + correct_republican + wrong_republican + wrong_democrat)
        #
        # print('Model ', model_num, ': ', percision)
        # print('Model ', model_num, ': ', sensitivity)
        # print('Model ', model_num, ': ', specificity)
        # print('Model ', model_num, ': ', accuracy)

        correct_cnt = 0
        incorrect_cnt = 0

        for res in list:
            if res[0] == res[1]:
                correct_cnt = correct_cnt + 1
            else:
                incorrect_cnt = incorrect_cnt + 1

        total = correct_cnt + incorrect_cnt

        accuracy = correct_cnt / total
        average = average + accuracy
        model_num = model_num + 1
        print(f'Model {model_num} accuracy: {accuracy:.5f}')

    average = average / 10
    print(f'Model average accuracy: {average:.5f}')

if __name__ == '__main__':
    with open('./data/house-votes-84.data', 'r') as data_file:
        data = data_file.read().splitlines()

    random.shuffle(data)

    # k-fold cross-validation, k = 10
    lines_count = len(data)
    size_df = math.floor(lines_count / 10)
    adjustments_cnt = lines_count % 10

    df = create_dfs(lines_count, size_df, adjustments_cnt)

    dfs_test = []
    dfs_train = []
    separate_dfs(df, dfs_test, dfs_train)

    print_accuracy(dfs_test, dfs_train)
