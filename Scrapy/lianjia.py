import xiaoqu_menu
import config

for district in config.district_list:
    xq = xiaoqu_menu.xiaoqu_menu(config.xiaoqu_url,district)
    xq.parser()