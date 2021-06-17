import pandas as pd

df_school_type = pd.read_csv(
    '../lab3_datasets/college-salaries/salaries-by-college-type.csv')
df_school_region = pd.read_csv(
    '../lab3_datasets/college-salaries/salaries-by-region.csv')


# 数据处理，把数据中的'$'与','符号去除
def data_handle(df):
    ls = ['Starting Median Salary', 'Mid-Career Median Salary', 'Mid-Career 10th Percentile Salary',
          'Mid-Career 25th Percentile Salary', 'Mid-Career 75th Percentile Salary',
          'Mid-Career 90th Percentile Salary']
    for column in ls:
        for i in range(len(df[column])):
            if str(df[column][i]) != 'nan':
                df[column][i] = df[column][i][1:-1].replace(',', '').strip(" ")
    return df


def dataInit():
    global df_school_type, df_school_region
    df_school_type = data_handle(df_school_type)
    df_school_region = data_handle(df_school_region)


# 根据用户选择返回所需的数据
def get_data(school_type_or_region):
    if school_type_or_region == 'School Type':
        return df_school_type
    else:
        return df_school_region


# 获取工资类型
def get_salary_type():
    return df_school_type.columns.values[2:]


# 获取所有可能的学校类型
def get_school_types():
    return df_school_type['School Type'].unique()


# 获取所有可能的学校地区
def get_school_regions():
    return df_school_region['Region'].unique()


def adjust_array_data(arr):
    temp = arr[0]
    arr[0] = arr[1]
    arr[1] = arr[2]
    arr[2] = temp


# 图像start_mid_salary_compare_data的数据
def get_start_mid_salary_compare_data(school_type_or_region):
    if school_type_or_region == 'School Type':
        return {'x': get_school_types(),
                'Starting Median Salary': get_media_salary_by_school_type
                (df_school_type, 'Starting Median Salary'), 'Mid-Career Median Salary':
                    get_media_salary_by_school_type(df_school_type, 'Mid-Career Median Salary')}
    else:
        return {'x': get_school_regions(),
                'Starting Median Salary': get_media_salary_by_school_region
                (df_school_region, 'Starting Median Salary'), 'Mid-Career Median Salary':
                    get_media_salary_by_school_region(df_school_region, 'Mid-Career Median Salary')}


# 图像salary_box的数据
def get_salary_box_data(school_type_or_region, salary_type):
    if school_type_or_region == 'School Type':
        return {'x': get_school_types(),
                'y': [[df_school_type[df_school_type['School Type']
                                      == column][salary_type].values] for column in get_school_types()]}
    else:
        return {'x': get_school_regions(),
                'y': [[df_school_region[df_school_region['Region']
                                        == column][salary_type].values] for column in get_school_regions()]}


# 根据具体学校类型求各个阶段工资中位数
def get_media_salary_by_certain_school_type(df, school_type):
    available_school_type = get_salary_type()
    dff = df[df['School Type'] == school_type]
    salary = []
    for salary_type in available_school_type:
        if salary_type == 'Starting Median Salary':
            continue
        salary.append(dff[salary_type].median())
    return salary


# 根据具体学校地区求各个阶段工资中位数
def get_media_salary_by_certain_school_region(df, school_region):
    available_school_type = get_salary_type()
    dff = df[df['Region'] == school_region]
    salary = []
    for salary_type in available_school_type:
        if salary_type == 'Starting Median Salary':
            continue
        salary.append(dff[salary_type].median())
    return salary


# 根据学校类型求工资中位数
def get_media_salary_by_school_type(df, column):
    available_school_type = get_school_types()
    salary = []
    for school_type in available_school_type:
        salary.append(df[df['School Type'] == school_type][column].median())
    return salary


# 根据学校地区求工资中位数
def get_media_salary_by_school_region(df, column):
    available_school_region = get_school_regions()
    salary = []
    for school_region in available_school_region:
        salary.append(df[df['Region'] == school_region][column].median())
    return salary
