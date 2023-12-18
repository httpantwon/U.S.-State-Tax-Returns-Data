
import csv
import json
import requests

# import matplotlib.pyplot as plt


# function to get the format from filename if the format is not known
def get_data_from_file(filename, format_=""):
    '''Returns the the object created from the data.  For a csv file, a list of lists. For a json file, a list or a dictionary (depends on the file contents)'''

    if format_ == "csv" or format_ == ".csv":
        '''if csv, handle csv file'''
        list_merged = []
        f = open(filename)
        lines = csv.reader(f)

        for line in lines:
            list_merged.append(line)
        f.close()
        return list_merged

    elif format_ == "json" or format_ == ".json":
        '''if json, handle json file'''
        list_merged = []
        f = open(filename)
        data = f.read()
        list_merged = json.loads(data)
        return list_merged


# return object
def get_data_from_internet(url):
    '''Grabs a list of dictionaries the population of each state from the Github url'''
    r = requests.get(url)
    data = r.json()
    return (data)


def get_state_name(state_names, state_code):
    '''Returns full name of a state if the user correctly inputs the state's abbreviation'''
    for state in range(len(state_names)):
        '''For each state in the list of 50 states & DC'''
        if state_code == state_names[state]["abbreviation"]:
            return state_names[state]["name"]


def get_state_population(state_populations, state_name):
    '''Loops through the population from each state'''
    state_name = "." + state_name
    state_ab = ""
    for i in range(len(state_populations)):
        for key in state_populations[i].keys():
            state_ab = key
        if state_name.lower() == state_ab.lower():
            return state_populations[i][state_ab]


def get_index_for_column_label(row, label):
    '''Returns the index position for that label'''
    count = row.index(label)
    return count


def answer_header(question_number, question_labels):
    '''returns the header string for each answer'''
    header = "\n" * 2
    header += "=" * 60 + "\n"
    header += "Question " + str(question_number) + "\n"
    header += question_labels[question_number] + "\n"
    header += "=" * 60 + "\n"
    return header


def main():

    question_labels = [
        "", "average taxable income per return across all groups",
        "average taxable income per return for each agi group",
        "average taxable income (per resident) per state",
        "average taxable income per return across all groups",
        "average taxable income per return for each agi group",
        "average dependents per return for each agi group",
        "percentage of returns with no taxable income per agi group",
        "average taxable income per resident",
        "percentage of returns for each agi_group",
        "percentage of taxable income for each agi_group"
    ]

    #get data
    returns_data = get_data_from_file("tax_return_data_2018.csv", "csv")
    state_names = get_data_from_file("states_titlecase.json", "json")
    populations = get_data_from_internet(
        "https://raw.githubusercontent.com/heymrhayes/class_files/main/state_populations_2018.txt"
    )

    row = returns_data[0]

    #index positions for relevant columns
    taxable_income_amt_idx = get_index_for_column_label(row, "A04800")
    taxable_returns_count_idx = get_index_for_column_label(row, "N04800")
    dependents_count_idx = get_index_for_column_label(row, "NUMDEP")
    total_returns_count_idx = get_index_for_column_label(row, "N1")
    agi_group_idx = get_index_for_column_label(row, "agi_stub")
    each_state = get_index_for_column_label(row, "STATE")
    # print(agi_group_idx)

    #### Question 1 ####
    total_returns = 0
    total_taxable_income = 0

    for i in range(1, len(returns_data)):
        '''For each column in the tax return csv file'''
        row = returns_data[i]
        total_returns += int(row[total_returns_count_idx])
        total_taxable_income += int(row[taxable_income_amt_idx])
        average_q1 = (1000 * total_taxable_income / total_returns)

    #### Question 2 ####
    lst_q2 = []
    answer2part = ''
    answer2 = ''
    avg_taxable_by_group = {}

    for i in range(1, len(returns_data)):
        row = returns_data[i]
        group_number = row[agi_group_idx]

        if group_number not in avg_taxable_by_group:
            avg_taxable_by_group[group_number] = {
                "total_returns": 0,
                "total_taxable_income": 0
            }

        avg_taxable_by_group[group_number]["total_returns"] += int(
            row[total_returns_count_idx])
        avg_taxable_by_group[group_number]["total_taxable_income"] += int(
            row[taxable_income_amt_idx])

    group_num = 0

    for key in avg_taxable_by_group:
        group_num += 1
        avg_taxable_by_group[key]["avg_taxable"] = avg_taxable_by_group[key][
            "total_taxable_income"] / avg_taxable_by_group[key]["total_returns"]

        lst_q2.append(avg_taxable_by_group[key]["avg_taxable"] * 1000)
        answer2part = "Group " + str(group_num) + ": ${:8.0f}".format(
            avg_taxable_by_group[key]["avg_taxable"] * 1000)
        answer2 += answer2part + "\n"

    # Question 3 - average taxable income (per resident) per state #
    states_tax_inc = {}
    lst_q3 = []
    answer3part = ''
    answer3 = ''
    for i in range(1, len(returns_data)):
        row = returns_data[i]
        state_code = row[each_state]

        if state_code not in states_tax_inc:
            '''add dictionary for that group'''
            states_tax_inc[state_code] = {"taxable_income": 0}
        states_tax_inc[state_code]["taxable_income"] += int(
            row[taxable_income_amt_idx])

    for state_code in states_tax_inc:
        state_name = get_state_name(state_names, state_code)
        state_population = get_state_population(populations, state_name)
        states_tax_inc[state_code]["average"] = 1000 * (
            states_tax_inc[state_code]["taxable_income"] / state_population)
        answer3part = state_code + ":  ${:8.0f}".format(
            (states_tax_inc[state_code]["average"]))
        answer3 += answer3part + '\n'

    ### Question 4 ####
    total_returns = 0
    total_taxable_income = 0
    random = 0
    answer4part = ''
    answer4 = ''
    x = input("Please enter a state code: ")
    '''Gets value from user's input'''
    print(x)
    for i in range(1, len(returns_data)):
        row = returns_data[i]
        if (x == row[1]):
            # print(total_returns)
            total_returns += int(row[total_returns_count_idx])
            total_taxable_income += int(row[taxable_income_amt_idx])

    answer4part = "${:8.0f}".format(
        (total_taxable_income / total_returns) * 1000)
    answer4 = answer4part + "\n"

    ### Question 5 ###
    lst_q5 = []
    for i in range(1, len(returns_data)):
        row = returns_data[i]
        group_number = row[agi_group_idx]
        if (x == row[1]):
            '''If the user's input equals one of the 50 state abbreviatons or DC'''
            total_returns = int(row[total_returns_count_idx])
            total_taxable_income = int(row[taxable_income_amt_idx])
            lst_q5.append((total_taxable_income / total_returns) * 1000)

    ### Question 6 ###
    lst_q6 = []

    for i in range(1, len(returns_data)):
        row = returns_data[i]
        group_number = row[agi_group_idx]
        if (x == row[1]):
            total_dependents = int(row[dependents_count_idx])
            total_returns = int(row[total_returns_count_idx])
            lst_q6.append("{:8.2f}".format((total_dependents / total_returns)))
            # print(lst_q6)

    ### Question 7 ###
    lst_q7 = []

    for i in range(1, len(returns_data)):
        row = returns_data[i]
        group_number = row[agi_group_idx]

        if (x == row[1]):
            total_returns = int(row[total_returns_count_idx])
            total_taxable_returns = int(row[taxable_returns_count_idx])
            avg_nontaxable_returns = 1 - (total_taxable_returns /
                                          total_returns)
            lst_q7.append("{:8.2f}%".format((avg_nontaxable_returns) * 100))

    ### Question 8 ###
    q8average = states_tax_inc[x]["average"]
    q8formattedavg = "${:8.0f}".format(q8average)

    ### Question 9 ###
    lst_q9 = []
    total_returns = 0
    total_taxable_returns = 0

    for i in range(0, len(returns_data)):
        row = returns_data[i]
        if (x == row[1]):
            total_returns += int(row[total_returns_count_idx])

    for i in range(0, len(returns_data)):
        row = returns_data[i]
        group_number = row[agi_group_idx]

        if (x == row[1]):
            total_taxable_returns = int(row[total_returns_count_idx])
            avg_taxable_returns = ((total_taxable_returns / total_returns) *
                                   100)
            lst_q9.append("Group " + group_number +
                          ": {:8.2f}%".format(avg_taxable_returns))

    ### Question 10 ###
    lst_q10 = []
    total_returns = 0
    total_taxable_returns = 0

    for i in range(0, len(returns_data)):
        row = returns_data[i]
        if (x == row[1]):
            total_returns += int(row[taxable_income_amt_idx])

    for i in range(0, len(returns_data)):
        row = returns_data[i]
        group_number = row[agi_group_idx]

        if (x == row[1]):
            total_taxable_returns = int(row[taxable_income_amt_idx])
            avg_taxable_returns = ((total_taxable_returns / total_returns) *
                                   100)
            lst_q10.append("Group " + group_number +
                           ": {:8.2f}%".format(avg_taxable_returns))

    file_name = "answers" + x + ".txt"
    f_ans = open(file_name, "w")

    f_ans.write(answer_header(1, question_labels))
    f_ans.write("${:8.0f}".format(average_q1))

    f_ans.write(answer_header(2, question_labels))
    index_group = 1
    for group_data in lst_q2:
        f_ans.write("Group " + str(index_group) +
                    ": ${:8.0f}".format(group_data) + "\n")
        index_group += 1

    f_ans.write(answer_header(3, question_labels))
    state_code = row[each_state]
    f_ans.write(answer3)

    f_ans.write(answer_header(4, question_labels))
    f_ans.write(answer4)

    f_ans.write(answer_header(5, question_labels))
    index_group = 1
    for group_data in lst_q5:
        f_ans.write("Group " + str(index_group) +
                    ": ${:8.0f}".format(group_data) + "\n")
        index_group += 1

    f_ans.write(answer_header(6, question_labels))
    index_group = 1
    for group_data in lst_q6:
        f_ans.write("Group " + str(index_group) + ": " + str(group_data) +
                    "\n")
        index_group += 1

    f_ans.write(answer_header(7, question_labels))
    index_group = 1
    for group_data in lst_q7:
        f_ans.write("Group " + str(index_group) + ": " + str(group_data) +
                    "\n")
        index_group += 1

    f_ans.write(answer_header(8, question_labels))
    index_group = 1
    f_ans.write(q8formattedavg)

    f_ans.write(answer_header(9, question_labels))
    index_group = 1
    for group_data in lst_q9:
        f_ans.write(str(group_data) + "\n")
        index_group += 1

    f_ans.write(answer_header(10, question_labels))
    index_group = 1
    for group_data in lst_q10:
        f_ans.write(str(group_data) + "\n")
        index_group += 1


main()
