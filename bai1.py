from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
import pandas as pd 
import matplotlib.pyplot as plt

from selenium.webdriver.common.by import By
webdriver_path=r'C:\Windows\chromedriver.exe'
chrome_options=ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("disable-gpu")
service=ChromeService(executable_path=webdriver_path)
driver=webdriver.Chrome(service=service, options=chrome_options)

Url={
    'standard':'https://fbref.com/en/comps/9/stats/Premier-League-Stats#all_stats_standard',
    'goalkeeping': 'https://fbref.com/en/comps/9/keepers/Premier-League-Stats#all_stats_keeper',
    'shooting': 'https://fbref.com/en/comps/9/shooting/Premier-League-Stats#all_stats_shooting',
    'passing': 'https://fbref.com/en/comps/9/passing/Premier-League-Stats#all_stats_passing',
    'goal_and_shot_creation': 'https://fbref.com/en/comps/9/gca/Premier-League-Stats#all_stats_gsc',
    'defensive_action': 'https://fbref.com/en/comps/9/defense/Premier-League-Stats#all_stats_defense',
    'possession': 'https://fbref.com/en/comps/9/possession/Premier-League-Stats#all_stats_possession',
    'misc': 'https://fbref.com/en/comps/9/misc/Premier-League-Stats#all_stats_misc'
}

def extract_table(driver, url, table_id, columns_to_extract):
    result = []
    driver.get(url)
    soup = bs(driver.page_source, 'html.parser')
    
    table = soup.find('table', id=table_id)
    if not table:
        print(f"Không tìm thấy bảng với id: {table_id}")
        return pd.DataFrame()

    tbody = table.find('tbody')
    rows = tbody.find_all('tr')

    for row in rows:
        if row.get('class') and 'thead' in row['class']:
            continue  # Bỏ qua các hàng tiêu đề phụ

        record = {}
        for col_name, data_stat in columns_to_extract.items():
            cell = row.find('td', {'data-stat': data_stat})
            value = cell.text.strip() if cell and cell.text.strip() else 'N/a'
            record[col_name] = value

        result.append(record)

    return pd.DataFrame(result)

columns_to_extract_standard = {
    'Player': 'player',
    'Nation': 'nationality',
    'Team': 'team',
    'Position': 'position',
    'Age': 'age',
    'MP': 'games',
    'Starts': 'games_starts',
    'Min': 'minutes',
    'Gls': 'goals',
    'Ast': 'assists',
    'CrdY': 'cards_yellow',
    'CrdR': 'cards_red',
    'xG': 'xg',
    'xAG': 'xg_assist',
    'PrgC': 'progressive_carries',
    'PrgP': 'progressive_passes',
    'PrgR': 'progressive_passes_received',
    'Gls_per90':'goals_per90',
    'Ast_per90':'assists_per90',
    'xG_per90':'xg_per90',
    'xAG_per90':'xg_assist_per90'
}
df_standard = extract_table(driver, Url['standard'], 'stats_standard', columns_to_extract_standard)
df_standard.to_csv('players_standard.csv', index=False)

columns_to_extract_goalkeeping={
    'Player': 'player',
    'GA90':'gk_goals_against_per90',
    'Save%':'gk_save_pct',
    'CS%':'gk_clean_sheets_pct',
    'PenSave%':'gk_pens_save_pct'
}
df_goalkeeping= extract_table(driver, Url['goalkeeping'],'stats_keeper',columns_to_extract_goalkeeping)
df_goalkeeping.to_csv('keeper.csv',index=False)

columns_to_extract_shooting={
    'Player': 'player',
    'SoT%':'shots_on_target_pct',
    'SoT/90':'shots_on_target_pct',
    'G/sh':'goals_per_shot',
    'Dist':'average_shot_distance'
}
df_shooting = extract_table(driver,Url['shooting'],'stats_shooting',columns_to_extract_shooting)
df_shooting.to_csv('shooting.csv',index=False)

columns_to_extract_passing = {
    'Player': 'player',
    'Cmp': 'passes_completed',                         
    'Cmp%': 'passes_pct',                              
    'TotDist': 'passes_total_distance',               
    'ShortCmp%': 'passes_pct_short',                  
    'MedCmp%': 'passes_pct_medium',                    
    'LongCmp%': 'passes_pct_long',                     
    'KP': 'passes_into_final_third',                   
    '1/3': 'passes_into_final_third',                  
    'PPA': 'passes_into_penalty_area',                 
    'CrsPA': 'crosses_into_penalty_area',             
    'PrgP': 'progressive_passes'                       
}
df_passing=extract_table(driver,Url['passing'],'stats_passing',columns_to_extract_passing)
df_passing.to_csv('pass.csv')

columns_to_extract_gsc = {
    'Player': 'player',
    'SCA': 'sca',
    'SCA90': 'sca_per90',
    'GCA': 'gca',
    'GCA90': 'gca_per90'
}
df_gsc=extract_table(driver,Url['goal_and_shot_creation'],'stats_gca',columns_to_extract_gsc)
df_gsc.to_csv('gsc.csv')

columns_to_extract_defense = {
    'Player': 'player',
    'Tkl': 'tackles',
    'TklW': 'tackles_won',
    'Att': 'challenges',
    'Lost': 'challenges_lost',
    'Blocks': 'blocks',
    'Sh': 'blocked_shots',
    'Pass': 'blocked_passes',
    'Int': 'interceptions'
}
df_defense=extract_table(driver,Url['defensive_action'],'stats_defense',columns_to_extract_defense)
df_defense.to_csv('defense.csv')

columns_to_extract_possession = {
    'Player': 'player',
    'Touches': 'touches',
    'Def Pen': 'touches_def_pen_area',
    'Def 3rd': 'touches_def_3rd',
    'Mid 3rd': 'touches_mid_3rd',
    'Att 3rd': 'touches_att_3rd',
    'Att Pen': 'touches_att_pen_area',
    'Att': 'take_ons',
    'Succ%': 'take_ons_won_pct',
    'Tkld%': 'take_ons_tackled_pct',
    'Carries': 'carries',
    'TotDist': 'carries_distance',
    'PrgDist': 'carries_progressive_distance',
    '1/3': 'carries_into_final_third',
    'CPA': 'carries_into_penalty_area',
    'Mis': 'miscontrols',
    'Dis': 'dispossessed',
    'Rec': 'passes_received',
    'PrgR': 'progressive_passes_received'
}
df_possession=extract_table(driver,Url['possession'],'stats_possession',columns_to_extract_possession)
df_possession.to_csv('possession.csv')

columns_to_extract_misc = {
    'Player': 'player',
    'Fls': 'fouls',
    'Fld': 'fouled',
    'Off': 'offsides',
    'Crs': 'crosses',
    'Recov': 'ball_recoveries',
    'Won': 'aerials_won',
    'Lost': 'aerials_lost',
    'Won%': 'aerials_won_pct'
}
df_misc=extract_table(driver,Url['misc'],'stats_misc',columns_to_extract_misc)
df_misc.to_csv('misc.csv',index=False)

from functools import reduce

# Kết hợp tất cả các DataFrame lại với nhau
dfs = [df_standard, df_goalkeeping, df_shooting, df_passing, df_gsc, df_defense, df_possession, df_misc]
merged_df = reduce(lambda left, right: pd.merge(left, right, on='Player', how='outer'), dfs)

# Thay thế các giá trị NaN bằng "N/a"
merged_df.fillna("N/a", inplace=True)

# Loại bỏ các hàng trùng lặp với cùng một 'Player' và 'Team', giữ nguyên thứ tự ban đầu
merged_df = merged_df.drop_duplicates(subset=['Player', 'Team'], keep='first')

merged_df['Player'] = merged_df['Player'].str.title()
merged_df['Min'] = pd.to_numeric(merged_df['Min'], errors='coerce')
merged_df = merged_df[merged_df['Min'] >= 90]
# Lưu kết quả vào file CSV
merged_df.to_csv('results.csv', index=False) 