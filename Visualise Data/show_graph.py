"""show_graph is an application that     \
    takes in a json file and plots it   \
    onto a graph with the data:         \
    [{time(int) : speed(float)}]"""
import glob
import json
import os
import statistics
import sys
from datetime import datetime, timedelta
from matplotlib import dates
import matplotlib.pyplot as plt

# |===============|
# |   CONSTANTS   |
# |===============|

# variables and constants
MAX_ACCEPTABLE_VALUE = 100
MIN_ACCEPTABLE_VALUE = 0
IS_MUTLIPLE_FILES = len(sys.argv) > 2


# |================|
# |    CLASSES     |
# |================|

class DataPoint:
    """This Data Point ensures sure that we are working with one item"""
    def __init__(self, key, value):
        self.key = self.round_key(key)
        self.value = value

    def round_key(self, key):
        """This function rounds the key to a minute"""
        return datetime.fromtimestamp(datetime.timestamp(key) //60 * 60)

    def key_equals(self, key):
        """This function checks if the keys are equal when rounded"""
        return self.key == self.round_key(key)

class TimeSlicer:
    """TimeSlicer is meant to slice all data into individual minutes.
    If there is no data for that minute, add a 0.
    If there are 2 data points in that minute, add the average.
    This is not meant to add 2 data files,
    but create a standard between all of them."""
    def __init__(self, input_values, input_keys):
        self.values = input_values
        self.keys = input_keys
        self.data_points = self.create_data_points()
        self.minutes_per_day = 1440
        self.merge_data_points()
        self.data_points.sort(key=lambda x: x.key, reverse=False)

    def create_data_points(self):
        """This function splits up the data sets into data points"""
        data_points = []
        for key_index, key in enumerate(self.keys):
            data_points.append(DataPoint(key, self.values[key_index-1]))
        return data_points

    def merge_data_points(self):
        """We are merging data points!
        Unify the data points to make a better working dataset"""
        to_be_merged = {}
        for index_point, datapoint in enumerate(self.data_points):
            for index2, datapoint2 in enumerate(self.data_points):
                if index_point != index2 and datapoint.key_equals(datapoint2.key):
                    if datapoint.key in to_be_merged:
                        to_be_merged[datapoint.key].append(datapoint.value)
                    else:
                        to_be_merged[datapoint.key] = [datapoint.value]
                    to_be_merged[datapoint.key].append(datapoint2.value)

        # Create new Datapoint list without merge items
        self.data_points = [datapoint \
                            for datapoint in self.data_points \
                            if datapoint.key not in to_be_merged]

        for key, merge_values in to_be_merged.items():
            average_value = sum(merge_values) / len(merge_values)
            self.data_points.append(DataPoint(key, average_value))

    def get_tuppel_keys_and_values(self):
        """This is purely to get the cleaned up values from the TimeSlicer"""
        time_keys = [datapoint.key for datapoint in self.data_points]
        time_values = [datapoint.value for datapoint in self.data_points]
        return (time_keys, time_values)

class MathValues:
    """These Math Values information to help calculate the graph lines
    """
    def __init__(self, key_list, values_list, include_zero=False):
        self.keys = key_list
        self.include_zero = include_zero
        self.values = values_list
        self.get_ranges()
        self.average_value = self.get_average()

    def get_values_without_zero(self):
        """This function returns all the values but without the zeros"""
        return list(filter(lambda a: a != 0, self.values))

    def get_average(self):
        """Calculate the average of all values, based on the include_zero parameter!"""
        if self.include_zero:
            return self.get_with_zero_average()
        return self.get_no_zero_average()

    def get_with_zero_average(self):
        """Calculate the average of all values!"""
        return sum(self.values) / len(self.values)

    def get_no_zero_average(self):
        """Calculate the average of all values excluding the zero!"""
        non_zero_values = self.get_values_without_zero()
        return sum(non_zero_values)/len(non_zero_values)

    def get_ranges(self):
        """Return the ranges for both keys and values"""
        # What are the value ranges?
        max_value = max(self.values)
        min_value = min(self.values)

        self.max_value_range = max_value \
            if max_value > MAX_ACCEPTABLE_VALUE \
            else MAX_ACCEPTABLE_VALUE

        self.min_value_range = min_value \
            if min_value < MIN_ACCEPTABLE_VALUE \
            else MIN_ACCEPTABLE_VALUE

class StandardDeviation:
    """Standard Deviation is used to calculate the deviation of all values"""
    def __init__(self, math_values_array:list[MathValues], include_zero=False):
        self.math_values_array = math_values_array
        self.all_values = self.get_all_values(math_values_array)
        self.standard_deviation = self.get_standard_deviation(include_zero)
        self.std_half = self.standard_deviation / 2
        self.average_value = self.get_average()

    def get_average(self):
        """Get the average for all averages in the math_values"""
        average_array = [math_value.average_value for math_value in self.math_values_array]
        return sum(average_array) / len(average_array)

    def get_standard_deviation(self, include_zero=False):
        """This function takes all the values and calculates the STD Deviation"""
        if include_zero:
            return statistics.stdev(self.all_values)
        return statistics.stdev(self.get_values_without_zero())

    def get_all_values(self, math_values_array:list[MathValues]):
        """This function combines all math_values into one variable"""
        return_values = list()
        for math_value in math_values_array:
            return_values.extend(math_value.values)
        return return_values

    def get_values_without_zero(self):
        """This function returns all the values but without the zeros"""
        return list(filter(lambda a: a != 0, self.all_values))

# |================|
# |  CALCULATIONS  |
# |================|

def round_str(value):
    """Rounds the Float value and Converts it to String"""
    return str(round(value, 2))

def do_step(step):
    """Returns a step into standard deviations"""
    step_down = stdDeviation.average_value - stdDeviation.std_half * step
    step_up = stdDeviation.average_value + stdDeviation.std_half * step

    if step_up > MAX_ACCEPTABLE_VALUE:
        step_up = MAX_ACCEPTABLE_VALUE

    if step_down < MIN_ACCEPTABLE_VALUE:
        step_down = MIN_ACCEPTABLE_VALUE

    return (step_down, step_up)

def create_std_label(min_value, max_value, step):
    """create STD Label"""
    std_min = "S" + str(step) + " (Min): " + round_str(min_value) + " Mbps"
    std_max = "S" + str(step) + " (Max): " + round_str(max_value) + " Mbps"
    return (std_min, std_max)

def plot_standard_deviation(steps, key_range):
    """This function plots the standard deviation sections onto the graph"""
    if steps == 0:
        return

    std_color_min = "#ee7744"
    std_color_max = "#77ee44"
    line_style = ":"
    line_width = 1
    # Min Range
    for i in range(steps):
        (smin, smax) = do_step(i + 1)
        (smin_label, smax_label) = create_std_label(smin, smax, i + 1)
        plt.plot(key_range, [smin, smin], label=smin_label, \
            color=std_color_min, lw=line_width, ls=line_style, alpha=1/(i + 1))
        plt.plot(key_range, [smax, smax], label=smax_label, \
            color=std_color_max, lw=line_width, ls=line_style, alpha=1/(i + 1))

def plot_min_and_max_values(min_value_range, max_value_range, key_range):
    """Plot the minimum and max values on the grid."""
    plt.plot(key_range, [min_value_range, min_value_range], color="#aa0000", alpha=0.1, lw=1)
    plt.plot(key_range, [max_value_range, max_value_range], color="#00aa00", alpha=0.1, lw=1)

def load_data_from_files(files_input) -> list[dict]:
    """Load the data from the JSON file then return a tupel"""
    return_files = list[dict]()
    lowest_key = None
    highest_key = None

    for file in files_input:
        dict_data:dict = json.loads(file.read())
        return_files.append(dict_data)
        dict_keys = [float(tempKey) for tempKey in dict_data.keys()]
        if lowest_key is None or lowest_key > min(dict_keys):
            lowest_key = min(dict_keys)

    for file_data in return_files:
        for file_data_key in file_data.keys():
            new_file_data_key = datetime.fromtimestamp(\
                            float(file_data_key)).replace(\
                                year=datetime.fromtimestamp(lowest_key).year, \
                                month=datetime.fromtimestamp(lowest_key).month, \
                                day=datetime.fromtimestamp(lowest_key).day)
            if highest_key is None or datetime.timestamp(new_file_data_key) > highest_key:
                highest_key = datetime.timestamp(new_file_data_key)

    return (return_files, lowest_key, highest_key)

# |===================|
# | COMPILE RESOURCES |
# |===================|

# List of that file in the folder
list_of_files = glob.glob(os.getcwd()+'\\*.json')

# If you didn't populate the args
# check if there is a data filethat is available
if(len(list_of_files) == 0 and len(sys.argv) == 1):
    print("No JSON files found in this folder.")
    print("Please specify a file path in args.")
    sys.exit(1)

files = []

# When multiple arguments are being parsed through:
# Split the data up into minute intervals instead of seconds.
# The Standard Deviation calculations now needs to
#       be done for all values and not just one document.
# Plot the new data on a different color line for speeds.

if len(sys.argv) > 1:
    for arg in range(len(sys.argv)-1):
        files.append(open(sys.argv[arg+1], encoding="UTF-8"))
else:
    files.append(open(max(list_of_files, key=os.path.getctime), encoding="UTF-8"))

data_array_dict = [{}]
dataInDict = {}
MIN_KEY = None
MAX_KEY = None
Keys = list
Values = list
ROOT_DATE = None
Value_Array = list()
File_Dates = list()


MIN_KEY_TIMESTAMP = -1
MAX_KEY_TIMESTAMP = -1
data_array_dict, low_key, high_key = load_data_from_files(files)
if ROOT_DATE is None:
    ROOT_DATE = datetime.fromtimestamp(low_key)
for data_array_dict_value in data_array_dict:
    valuelist_temp = list(data_array_dict_value.values())
    keyslist_temp = list(datetime.fromtimestamp(int(key)) \
                        for key in data_array_dict_value.keys())
    Value_Array.append(([keys_temp.replace(year=ROOT_DATE.year, \
                        month=ROOT_DATE.month, day=ROOT_DATE.day) \
                        for keys_temp in keyslist_temp], valuelist_temp))
    File_Dates.append(str(keyslist_temp[0].strftime('%d %B %y')))

MIN_KEY = datetime.fromtimestamp(low_key)
MAX_KEY = datetime.fromtimestamp(high_key)


for file_arr in files:
    file_arr.close()

KEY_RANGE = (MIN_KEY, MAX_KEY)

mathValues_array:list[MathValues] = list()

time_slicer_array = [TimeSlicer(v_arr, k_arr) for k_arr, v_arr  in (Value_Array)]
for time_slice in time_slicer_array:
    mathValues_array.append(MathValues(time_slice.keys, time_slice.values))

MIN_ACCEPTABLE_VALUE = min([mathvalue.min_value_range for mathvalue in mathValues_array])
MAX_ACCEPTABLE_VALUE = max([mathvalue.max_value_range for mathvalue in mathValues_array])

stdDeviation = StandardDeviation(mathValues_array)

# ===============
#      LABELS
# ================

STANDARD_DEVIATION_LABEL = "STD Deviation: " + round_str(stdDeviation.standard_deviation)
AVERAGE_VALUE_LABEL = "Avg (Without Zero): " + round_str(stdDeviation.average_value) +  " Mbps"

# This is just incase we don't have enough data
# We want to see the graph within an hour range
EMPTY_RANGE_LEFT  = KEY_RANGE[0] + timedelta(hours=1)
EMPTY_RANGE_RIGHT = KEY_RANGE[0] - timedelta(hours=1)

# ================
#    PLOT GRAPH
# ================

# Standard Deviation

plot_min_and_max_values(MIN_ACCEPTABLE_VALUE, MAX_ACCEPTABLE_VALUE, KEY_RANGE)
plot_standard_deviation(3, KEY_RANGE)

# Plotting Speeds
for index, mathvalues_item in enumerate(mathValues_array):
    plt.plot(mathvalues_item.keys, mathvalues_item.values, \
        label="Speed (Mbps) " + File_Dates[index], lw=(0.5 if IS_MUTLIPLE_FILES else 1))
    if not IS_MUTLIPLE_FILES:
        plt.fill_between(mathvalues_item.keys, mathvalues_item.values, alpha=0.2)

# Average Values
plt.plot(KEY_RANGE, [stdDeviation.average_value, stdDeviation.average_value], \
    label=AVERAGE_VALUE_LABEL, color="Orange", lw=1, ls="-.")

# No plotting, but adding to legend
plt.plot([0,0], [0,0], label=STANDARD_DEVIATION_LABEL, color="white", lw=1)


plt.xlim([KEY_RANGE[0] if KEY_RANGE[0] != KEY_RANGE[1] else EMPTY_RANGE_RIGHT, \
                KEY_RANGE[1] if KEY_RANGE[0] != KEY_RANGE[1] else EMPTY_RANGE_LEFT])


plt.subplots_adjust(right=0.8)
plt.legend(loc='center left', ncol=1, bbox_to_anchor=(1.04, 0.5), fancybox=False, shadow=True)

plt.gca().xaxis.set_major_locator(dates.HourLocator())
plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%H:%M'))

plt.show()
