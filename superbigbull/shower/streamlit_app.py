import streamlit as st
import numpy as np
import pandas as pd
import time

# 初始化变量
variable1 = 0
variable2 = 0
variable3 = 0

# 创建一个函数用于更新变量值
def update_variables():
    global variable1, variable2, variable3
    variable1 += np.random.randint(1, 10)
    variable2 = np.random.uniform(0, 1)
    variable3 = np.random.choice(['A', 'B', 'C'])

# 在页面上实时显示变量
variable1_placeholder = st.empty()
variable2_placeholder = st.empty()
variable3_placeholder = st.empty()

while True:
    update_variables()
    variable1_placeholder.text(f'变量1: {variable1}')
    variable2_placeholder.text(f'变量2: {variable2}')
    variable3_placeholder.text(f'变量3: {variable3}')
    time.sleep(1)  # 每秒更新一次)  # 每秒更新一次