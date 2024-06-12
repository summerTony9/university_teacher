import pandas as pd

df = pd.read_csv('teacher_detail.csv')

# replace na with empty string
df.fillna('', inplace=True)


def merge_columns(columns, new_column_name, df):
    temp_col = df[columns].apply(lambda x: ' '.join(x), axis=1)
    df.drop(columns, axis=1, inplace=True)
    df[new_column_name] = temp_col
    return df


df = merge_columns(["姓名", "姓名(Name)"], "姓名", df)
df = merge_columns(["性别(Gender)", "性别"], "性别", df)
df = merge_columns(["办公电话", "电话", "移动电话", "固定电话"], "电话", df)
df = merge_columns(["研究方向", "究方向"], "研究方向", df)

cols = ['姓名', '职称', '性别', '链接', '政治面貌', '院系', '电子邮件', '毕业院校', '毕业专业',
        '最高学位', '职务', '电话', '籍贯', '通讯地址', '办公地点', '最高学历', '电子邮箱',
        '研究方向', '研究兴趣', '研究领域与主要成果', '指导研究生获奖', '学科方向', '导师类型', 'extra_info']
df = df[cols]
df.to_csv('teacher_detail-tidy.csv', index=False, encoding='utf-8-sig')