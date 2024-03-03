import pandas as pd
# from app.src.database.menu import MenuDatabase

def run_df(df):
    for index, row in df.iterrows():
        print(row)

    print(df.columns)

if __name__ == "__main__":

    main_df = pd.read_excel('base.xlsx', sheet_name='Prato Principal Input')
    side_df = pd.read_excel('base.xlsx', sheet_name='Acompanhamentos Input')
    salad_df = pd.read_excel('base.xlsx', sheet_name='Saladas Input')
    garnish_df = pd.read_excel('base.xlsx', sheet_name='Guarnição Input')

    # print(main_df, side_df, salad_df, garnish_df)
    run_df(main_df)

    # menu_db = MenuDatabase()
    