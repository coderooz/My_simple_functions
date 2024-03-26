from typing import Dict, List, Optional, Union
import time, json, os, pytz, re
from dateutil.relativedelta import relativedelta
from datetime import datetime, time, timedelta
from collections.abc import KeysView, ValuesView

####  For Time Based Methods ####


def generate_time_intervals(start_time, duration_split:int=1, duration_format:str='d', output_format:str='human', datetime_format="%Y-%m-%d %H:%M:%S", end_time=None, excludeDate=None):
    """
        Generate a list of time intervals based on the provided parameters.

        Parameters:
        - start_time (str|datetime): The starting point for generating time intervals.
        - duration_split (int): The duration of each time interval, specified in a numerical value. Default value is `1`.
        - duration_format (str): A single-character code representing the format of the duration.
                                Options include 's' (seconds), 'm' (minutes), 'h' (hours),
                                'd' (days), 'M' (months), and 'y' (years).
                                Default value is `d`.
        - output_format (str): The desired output format for the time intervals. Options are 'unix' or 'human'. Default value is `human`.
        - datetime_format (str, optional): A string specifying the format for human-readable time intervals.
                                        Default is "%Y-%m-%d %H:%M:%S".
        - end_time (datetime, str, optional): The end point for generating time intervals.
                                        If not provided, the default is the current time.
        - excludeDate (str, datetime, list[str], optional): The date's that are to be excluded.

        Returns:
        - time_intervals (list): A list of generated time intervals based on the provided parameters.
    """
    formats = {'s': 'seconds', 'm': 'minutes', 'h': 'hours', 'd': 'days', 'M': 'months', 'y': 'years'}
    if isinstance(start_time, str):
        start_time = datetime.strptime(start_time, datetime_format)
    elif isinstance(start_time, (int, float, tuple, KeysView, ValuesView, dict, list)):
        raise ValueError('The given format of data is invalid. Only excepts the datetime format or a str(i.e. 20-02-2020) whose format should match with `datetime_format` param.')
    
    delta = relativedelta(months=duration_split) if duration_format == 'M' else timedelta(**{formats[duration_format]: duration_split})

    current_time, time_intervals = start_time, []
    if end_time is None:
        end_time = datetime.now()

    while current_time <= end_time:
        if output_format == 'unix':
            time_intervals.append(current_time.timestamp())
        elif output_format == 'human':
            time_intervals.append(current_time.strftime(datetime_format))
        else:
            raise ValueError("Invalid output format. Choose between 'unix' or 'human'.")
        current_time += delta

    if excludeDate!=None:
        if isinstance(excludeDate, str):
            excludeDate = [excludeDate]
        elif isinstance(excludeDate, datetime):
            excludeDate = [excludeDate.strftime(datetime_format)]
        time_intervals = [i for i in time_intervals if i not in excludeDate]
    return time_intervals

def timestamp(given_time, format= "%Y-%m-%d %H:%M:%S", time_zone=None, normalize:str='sec'):
    """
        timestamp()
        -----------
        Returns the date and time in the specified format.

        Args:
        
    """
    
    if isinstance(given_time, list):
        return [timestamp(i, format, time_zone, normalize) for i in given_time]
    elif isinstance(given_time, (int, float)):
        given_time = convert_timestamp(given_time, normalize)
        if time_zone is not None:
            os.environ['TZ'] = time_zone
            time.tzset()
        return time.strftime(format, time.localtime(given_time))
    else: raise ValueError('The parameter passed in given_time is invalid. Please provide a valid data')

def convert_timestamp(timestamp_ms, normalization='sec'):
    """ Converts the unix timestamp to the desired format like second, minute or hour."""
    ty = type(timestamp_ms)
    if ty == int or ty == float:
        normalization_levels = {'millisecond': 1,'second': 1000,'minute': 1000 * 60,'hour': 1000 * 60 * 60,'day': 1000 * 60 * 60 * 24}
        normalization_factor = normalization_levels.get(normalization, 1)
        return timestamp_ms / normalization_factor
    elif ty == list: return [convert_timestamp(i,normalization) for i in timestamp_ms]
    else: raise TypeError("Argument type passed is not valid.")

def future_timestamp(interval, unit, time_zone='UTC'):
    """
        Calculate a future Unix timestamp based on the provided interval and unit.

        This function calculates a Unix timestamp representing a point in the future
        by adding the specified interval of time to the current moment.

        Parameters:
        - interval (int): The duration of the interval in the specified time unit.
        - unit (str): A string representing the time unit of the interval.
                    Options include 's' (seconds), 'm' (minutes), 'h' (hours),
                    'd' (days), 'mo' (months), 'y' (years).
        - time_zone (str, optional): The time zone for the calculation. Default is 'UTC'.

        Returns:
        - future_timestamp (float): The Unix timestamp representing the future point in time.
    """
    units = {'s': 'seconds','m': 'minutes','h': 'hours','d': 'days','mo':'month', 'yrs':'year'}
    tz = pytz.timezone(time_zone)
    unit = units.get(unit, unit)  # default to the input value if not found
    future_timestamp = datetime.now(tz) + timedelta(**{unit: interval})
    return future_timestamp.timestamp()

def split_interval(interval):
    parts = re.findall(r'(\d+)([smhd])', str(interval))
    if parts:
        value, unit = parts[0]
        return int(value), unit
    else:
        raise ValueError(f'Invalid interval: {interval}')

def to_unix_timestamp(date_time, formattype='%Y-%m-%d %H:%M:%S', time_zone='UTC'):
    """Convert a human-readable date and time into the Unix timestamp in the specified time zone."""
    if isinstance(date_time,  str):
        dt =datetime.strptime(date_time,formattype)
        tz = pytz.timezone(time_zone)
        dt_localized = tz.localize(dt)
        unix_timestamp = dt_localized.timestamp()
        return unix_timestamp
    elif isinstance(date_time,  list):
        return [to_unix_timestamp(i, formattype, time_zone) for i in date_time]

def to_human_readable(unix_timestamp, formattype='%Y-%m-%d %H:%M:%S', time_zone='UTC'):
    """Convert a Unix timestamp into a human-readable date and time in the specified time zone and format."""
    if isinstance(unix_timestamp, (int, float)):
        dt_object = datetime.fromtimestamp(unix_timestamp)
        tz = pytz.timezone(time_zone)
        dt_localized = tz.localize(dt_object)
        human_readable_timestamp = dt_localized.strftime(formattype)
        return human_readable_timestamp
    elif isinstance(unix_timestamp, list):
        return [to_human_readable(i, formattype, time_zone) for i in unix_timestamp]

def get_previous_day(date:str='', format:str='%d-%m-%Y', numberof_days:int=1):
    """
        get_previous_day()
        -------------------

        This method is to get the previous date of the given date.

        Parameter:
        - date (str, optional): This param takes the date who's previous date is to be fetched. Default is '', and will take the current date.
        - format (str): This parameter takes the format of the date passed and will return the date inthe same format. Defaults to '%d-%m-%Y'.
        - numberof_days int: takes the number of days previous to the given date's date is to be fetched. Defaault is 1.

    """
    date = datetime.now() if date == '' else datetime.strptime(date, format)        
    date = date - timedelta(days=numberof_days) 
    return date.strftime(format)

def identify_date_format(date_str:str):
    """
        identify_date_format()
        ----------------------
        Identifties the date method.
    """
    formats = ['%Y-%m-%d','%m-%d-%Y','%d-%m-%Y','%Y/%m/%d','%m/%d/%Y','%d/%m/%Y','%Y.%m.%d','%m.%d.%Y','%d.%m.%Y','%Y %m %d','%m %d %Y','%d %m %Y']

    for fmt in formats:
        try:
            datetime.strptime(date_str, fmt)
            return fmt
        except ValueError:
            pass

    return None

def dateFormat(date:str, format1:str, format2:str = ''):
    """
        dateFormat()
        ------------
        Changes the date format.
    """
    try:
        date = datetime.strptime(date, format1)
    except:
        date = datetime.strptime(date, identify_date_format(date))
    return date if format2=='' else date.strftime(format2)


####  For Dict Based Methods ####

def equalizer_dict(data:List[dict], value='')->list:
    """
        Make dictionaries equal by filling in missing keys and values.

        :param data: A list of dictionaries with varying keys and values.
        :type data: List[dict]

        :param value: The default value to fill in missing positions in the dictionaries.
                    Defaults to an empty string ('').
        :type value: Any, optional

        :return: A dictionary with keys present in all input dictionaries,
                and values filled or padded according to the specified default value.
        :rtype: list
    """
    data_len = len(data)
    data2 = {k:[] for k in data[0].keys()}
    for i in range(data_len):
        for k, v in data[i].items():
            ky = data2.keys()
            if k not in ky:
                if type(v) == type(value):
                    data2[k] = [value] * i
                elif isinstance(v, (list, dict)):
                    data2[k] = [[]] * i
                elif isinstance(v, str):
                    data2[k] = [''] * i
                elif isinstance(v, (int, float)):
                    data2[k] = [0] * i
            data2[k].append(v)

        for t in ky - set(data[i].keys()):
            lo = data2[t][i - 1]
            if type(lo) == type(value): data2[t].append(value)
            elif isinstance(lo, (list, dict)): data2[t].append([])
            elif isinstance(lo, str): data2[t].append('')
            elif isinstance(lo, (int, float)): data2[t].append(0)
    return dlist_dict(data2)

def dict_dimenstion_flatener(data:dict, catg):
    """
        dict_dimenstion_flatener()
        --------------------------
        This method is used to reducing a multi-dimention dict into a single dimention dict.

        Parameter:
        - data (dict): takes the dict that is to made into a single dimention.

    """
    pass

def dict_lister(data:list, opt:list=None)->dict:
    """
        Converts a list of dictionaries with list-type values into a dictionary with lists.

        :param data: A list of dictionaries where each dictionary contains keys with list values.
        :type data: list[dict]
        
        :param opt: An optional parameter specifying the keys to include in the resulting dictionary.
                    If not provided, it defaults to using all keys present in the first dictionary.
        :type opt: list, optional
        
        :return: A dictionary where keys are from the 'opt' parameter (or all keys if 'opt' is not provided),
                and values are lists containing corresponding values from the original dictionaries.
        :rtype: dict
    """
    t ={}
    if opt == None:
        opt = data[0].keys()
    for i in range(len(data)):
        for k,v in data[i].items():
            if k in opt:
                if (k not in t):
                    t[k] = [None for _ in range(i)] + [v] if i > 0 else [v]
                else: t[k].append(v)
    if len(opt) == 1 and len(opt)!=None: return t[opt[0]]
    return t

def dict_filter(data:dict, filter:list, catg=1):
    """
        This function checks if a parameter exists in the dictionay.
        :param data dict: This takes the dict that is to be checked for the data presence.
        :param filter list: This takes the list of values that is to be checked, if exists in the dict.
        :praram catg int: This param to to set where to check the values for. either it is in the calues section of in the keys secton.
    """
    dc = {}
    if catg == 1:
        dc = {key: val for key, val in data.items() if key in filter}
    elif catg == 0:
        dc = {key: val for key, val in data.items() if val not in filter}
    return dc

def flatten_dict(d, parent_key='', sep='_', catg:int=0):
    """
        This function flatens the dictionary into 1d i.e convertes the dictionay like {'a':{'b':'c'}} to {'a_b':'c'}.
        :param d dict: This parameter takes the dict.

    """
    items = []
    if catg == 0:
        for k, v in d.items():
            new_key = f'{parent_key}{sep}{k}' if parent_key else k
            if isinstance(v, dict):
                items.extend(flatten_dict(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                for i in v:
                    if isinstance(i, dict):
                        items.extend(flatten_dict(i, new_key, sep=sep).items())
                    else:
                        items.append((new_key, i))
            else:
                items.append((new_key, v))
        return dict(items)
    elif catg == 1:
        pass
    else: raise ValueError('The value passed into the parameter `catg` is not accepted. The only value accepted are `0` & `1`.')
    
def dict_reoganize(data, pattern:list):
    """
        dict_reoganize()
        ----------------

        This method is to reorganze the keys of the given dict.

        Args:
            data (dict|list): This patameter either takes the dict or a list of dict with similar keys.
            pattern (list): This parameter takes the pattern in which the dict keys are to be arranged.

        Raises:
            ValueError: The data passed in the data parameter is invalid. The paramerter only accepts either dict or a list of dict.
            ValueError: _description_

        Returns:
            dict|list: This method either return the reorganized dict or the list of dict reoganized.
    """
    if isinstance(data, list):
        return [dict_reoganize(i, pattern) for i in data if isinstance(i, dict)]
    elif isinstance(data, dict):
        return {key: data[key] for key in pattern}
    else:
        raise ValueError('The data passed in the data parameter is invalid. The paramerter only accepts either dict or a list of dict.')

####  For List Based Methods ####

def dlist_dict(my_dict:dict, keys:list=[]) -> list:
    """

        Convert a dictionary into a list of dictionaries.

        This function takes a dictionary and converts it into a list of dictionaries. Each dictionary in the resulting list corresponds to a set of values for selected keys from the original dictionary.

        Parameters:
        -----------
        my_dict : dict
            The dictionary to be converted into a list of dictionaries.
            Example: {'a': ['a_v1', 'a_v2'], 'b': ['b_v1', 'b_v2']}

        keys : list, optional
            Optional parameter to select specific keys to include in the resulting list.
            Defaults to an empty list ([]).

        Returns:
        --------
        list
            A list of dictionaries where each dictionary corresponds to a set of values for selected keys.

        Example:
        --------
        >>> my_dict = {'a': ['a_v1', 'a_v2'], 'b': ['b_v1', 'b_v2']}
        >>> result = dlist_dict(my_dict)
        >>> print(result)
        # Output: [{'a': 'a_v1', 'b': 'b_v1'}, {'a': 'a_v2', 'b': 'b_v2'}]

        >>> selected_keys = ['a']
        >>> result_selected_keys = dlist_dict(my_dict, keys=selected_keys)
        >>> print(result_selected_keys)
        # Output: [{'a': 'a_v1'}, {'a': 'a_v2'}]

        Notes:
        ------
        - If `keys` parameter is not provided, all keys from the original dictionary will be included in the resulting list of dictionaries.
        - The order of dictionaries in the resulting list is determined by the order of values for the first key in the original dictionary.
    """

    keys = my_dict.keys() if keys==[] else keys
    result_list = [{k: v[i] for k, v in my_dict.items() if k in keys} for i in range(len(list(my_dict.values())[0]))]
    return result_list

def list_dlist(data, keys):
    """
        This method list_dlist arranged the list list i.e.([['a','n'],['b','o']) into {key1:['a','b'], key2:['n','o']}
        Note:- The inter list length and the length of strings list given must be equal.
        :param list data: Takes the list that is to be arranged int the dict list format.
        :param list keys: Thakes the list of strings that are to be used as the dictionary keys for the arrangement.
        :return [dict]
    """
    dict_key = {}
    if isinstance(data[0], list) and len(keys) == len(data[0]):
        for quote in data:
            for i, value in enumerate(quote):
                dict_key.setdefault(keys[i], []).append(value)
    return dict_key

####  For other Methods ####

def get_unique(data:list, preserve:bool=False):
    """Gets the unique data of the given list. It also has the festure fo arranging the data in a assendng ordre or sorting the given data out."""
    if preserve:
        r = []
        for d in data:
            if d not in r:
                r.append(d)
        return r
    else: return sorted(list(set(data)))

def add_index(data, index_id:int=0, index_name:str='index'):
    """
    The `add_index` method is to add an id/index to the list data.
    Parameter:-
    - data(list): Takes the list of data which is to be indexed. The data in the list must be in a `dict` format.
    - index_id (int|None): This param is note from where the indexing number should start after. Default value: 0, No will start from 1.
    - index_name (str): The name of the key used to assign the index value.
    """
    if len(data) <= index_id: raise ValueError('The value given in param index_id is invalid.')
    for i in range(index_id+1, len(data)+1):
        data[i-1][index_name] = i
    return data

def remove_empty_strings(data):
    """Removes empty strings from a list or tuple."""
    return [string for string in data if string != '']

def decode_json(data):
    """Attempts to decode a string as JSON."""
    try:
        return json.loads(data)
    except:
        return None

def json_parser(data, pathway):
    """
        This function is designed to parse data in a JSON/dictionary structure based on a specified pathway.

        Parameters:
            - data (dict): The input JSON/dictionary data.
            - pathway (str): The pathway specifying the keys to navigate the data.

        Returns:
            The value at the specified pathway in the input data.

        Usage Examples:
            1. Simple pathway:
            ```python
            data = {'name': 'Alex', 'info': {'email': 'alex@gmail.com', 'age': 25}}
            pathway = 'info > email'
            result = json_parser(data, pathway)
            print(result)  # Output: 'alex@gmail.com'
            ```

            2. Pathway with nested keys:
            ```python
            data = {'person': {'name': 'John', 'details': {'age': 30, 'city': 'New York'}}}
            pathway = 'person > details > city'
            result = json_parser(data, pathway)
            print(result)  # Output: 'New York'
            ```

            3. Pathway with list indices:
            ```python
            data = {'people': [{'name': 'Alice'}, {'name': 'Bob'}]}
            pathway = 'people > 1 > name'
            result = json_parser(data, pathway)
            print(result)  # Output: 'Bob'
            ```

            4. Using a list of pathways to extract multiple values:
            ```python
            data = {'user': {'name': 'Alex', 'email': 'alex@gmail.com', 'age': 25}}
            pathways = ['user > name', 'user > email']
            result = json_parser(data, pathways)
            print(result)  # Output: {'name': 'Alex', 'email': 'alex@gmail.com'}
            ```
            5. Using Special keys:
            ```python
            data = {'user': {
                    'profile': {'name': 'John','address': {'city': 'New York', 'country': 'USA'},},
                    'preferences': {'theme': 'dark', 'notifications': True},
                }
            }

            pathway = {
                '__pathway__': {
                    'path': 'user > profile',
                    'data': ['name', 'address > country'],
                },'preferences': 'user > preferences',
            }

            result = json_parser(data, pathway)
            print(result) # {'name': 'John','address > country': 'USA','preferences': {'theme': 'dark', 'notifications': True}}
            ```
    """

    if isinstance(pathway, list):
        return {i.split('>')[0]:json_parser(data, i) for i in pathway}
    elif isinstance(pathway, str) and '>' in pathway:
        k = data
        path = pathway.split('>')
        for le in range(len(path)):
            i = setNum(path[le].strip())
            if i == '`list`' and isinstance(k, list):
                k = [json_parser(k, f"{str(n)} > {' > '.join(path[le + 1:])}") for n in range(len(k))]
                break
            elif (isinstance(k, list) and isinstance(i, int) and len(k)-1 >= i) or (isinstance(k, dict) and i in k.keys()):
                k = k[i]  
            else:
                k = None
                break
        return k
    elif isinstance(pathway, dict):
        n = {}
        for k,v in pathway.items():
            if k == '__pathway__':
                if isinstance(v, dict):
                    if isinstance(v['data'], dict):
                        n = {**n, **{h:json_parser(data, str(v['path'] + f' > {i}')) for h,i in v['data'].items()}}
                    elif isinstance(v['data'], list):
                        n = {**n, **{i.split('>')[-1].strip():json_parser(data, v['path'] + f' > {i}') for i in v['data']}}
                    elif isinstance(v['data'], str):
                        n[k] = json_parser(data, v['data'])
                elif isinstance(v, list):
                    n = {**n, **{i['path'].split('>')[-1].strip():json_parser(data, {'__pathway__': i}) for i in v}}
            else:
                n[k] = json_parser(data, v)
        return n
    else: raise ValueError('The pathway given is not acceptable/invalid. Please check the pathway.')

def round_values(data):
    """Rounds the values in a list, tuple, or dictionary if they are integers or floats."""
    data_type = type(data)
    if data_type == list:
        return [round(i) for i in data if isinstance(i, (float, int))]
    elif data_type == dict:
        return {key: round_values(value) for key, value in data.items()}
    elif isinstance(data, (float, int)):
        return round(data)
    else:
        print(f'The value passed is not compatible with the method. The type of value passed is {data_type}.\nPlease try again.')

def check_difference(*lists, time_period= None):
    max_length = max([len(list) for list in lists])
    time_period = time_period if (time_period!= None) else min([len(list) for list in lists])
    lists = [list + [0] * (max_length - len(list)) for list in lists]
    direction = []
    for i in range(1, time_period):
        diff = sum([list[i] for list in lists])
        prev_diff = sum([list[i-1] for list in lists])
        if diff > prev_diff:
            direction.append(1)
        elif diff < prev_diff:
            direction.append(-1)
        else:
            direction.append(0)
    return direction[:-time_period]

def get_differences(list1, list2):
    """ This function is used to get the differences beteween the two list of numbers of a list individually at the specific positions."""
    differences = []
    for i in range(len(list1)):
        diff = list1[i] - list2[i]
        differences.append(diff)
    return differences

def calculate_difference_percentage(num1, num2):
    """This function calculates the difference in percentage between two given numbers."""
    per = []
    for i in range(len(num1)):
        difference = num1[i] - num2[i]
        per.append(difference / min(num1[i], num2[i]) * 100)
    return per

def check_value_exists(value, param):
    """This method/function is used to determine wether a certan value exists or not in the value/data."""
    if isinstance(param, dict): return value in param.values()
    elif isinstance(param, (set, str)): return value in param
    else: return value in list(param)

def valreplace(data, target:str, replace:str, keyTy:bool=False):
    """
        This method/function is used for replaceing certain or wanted values in the given subject data.

        Paramerters:
        -----------
        - data (str|list|dict): This 
        - target (str): This parameter takes the target that has to be changed.
        - replace (str): This parameter takes the value that is to be replaced by the target.
        - keyTy (bool): If the data provided is a key then this value, if set to `True` then will also check look into the keys of the dict and change it accordingly.  

        Return:
        -------
        - str | list | dict : This method will not change the value type given and will retuen the data in same type.
    """
    if isinstance(data, dict):
        data = {(replace if k == target else k): v for k, v in data.items()} if keyTy else {k:valreplace(v, target, replace) for k,v in data.items()}
        return data
    elif isinstance(data, (list, KeysView, ValuesView)):
        return [valreplace(x, target, replace, keyTy) for x in data]
    elif isinstance(data, str):
        if keyTy: return ' '.join([word.replace(target, replace) if word == target else word for word in data.split()])
        else: return data.replace(target, replace)
    else: raise ValueError(f'This method only expects list, dict or a string. Not {type(data)}')

def space_remover(data):
    """
        This method is usd for removing any spaces in a string that is in front or behind the string. 
        This method can work on strings , dicts and lists of string.
    """
    if isinstance(data, dict):
        return {k.strip(): space_remover(v) for k,v in data.items()}
    elif isinstance(data, list):
        return [space_remover(i) for i in data]
    elif isinstance(data, str):
        return data.strip()
    else: return data

def setNum(data):
    """
        This metod is used for making any possible number or float that is in a string format turn into one. 
    """
    if isinstance(data, dict): return {k.strip(): setNum(v) for k,v in data.items()}
    elif isinstance(data, list): return [setNum(i) for i in data]
    elif isinstance(data, str):
        try:
            return int(data)
        except ValueError:
            try:
                return float(data)
            except ValueError:
                return data
    else:
        return data

def get_similarities(list1, list2):
    """
        This function returns the similarity between two lists and returns the simialar.
    """
    return list(set(list1).intersection(set(list2)))

