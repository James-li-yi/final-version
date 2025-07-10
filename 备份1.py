import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import numpy as np

# 页面配置
st.set_page_config(page_title="保利物业拓展分析", layout="wide")

# 标题
st.title(" 保利物业2024-2025年市场拓展分析")
st.markdown(
    """
    <style>
    .stApp {
        background-color: black;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 侧边栏 - 文件上传
st.sidebar.header("📁 数据文件上传")
file_2024 = st.sidebar.file_uploader("上传2024年数据", type=['csv'])
file_2025 = st.sidebar.file_uploader("上传2025年数据", type=['csv'])

def load_data(file, year):
    """加载并处理数据"""
    if file is not None:
        try:
            # 首先尝试UTF-8编码
            df = pd.read_csv(file, encoding='utf-8')
        except UnicodeDecodeError:
            try:
                # 如果UTF-8失败，尝试GBK编码
                file.seek(0)  # 重置文件指针
                df = pd.read_csv(file, encoding='gbk')
            except UnicodeDecodeError:
                try:
                    # 如果GBK也失败，尝试GB2312编码
                    file.seek(0)  # 重置文件指针
                    df = pd.read_csv(file, encoding='gb2312')
                except UnicodeDecodeError:
                    # 最后尝试ISO-8859-1编码
                    file.seek(0)  # 重置文件指针
                    df = pd.read_csv(file, encoding='iso-8859-1')
        
        # 数据清洗：移除空行和无效行
        df = df.dropna(how='all')  # 删除完全空白的行
        df = df.dropna(subset=['业绩金额'])  # 删除业绩金额为空的行
        
        # 确保业绩金额为数值型
        df['业绩金额'] = pd.to_numeric(df['业绩金额'], errors='coerce')
        
        # 移除业绩金额转换失败的行
        df = df.dropna(subset=['业绩金额'])
        
        # 移除重复行（如果存在）
        df = df.drop_duplicates()
        
        # 重置索引
        df = df.reset_index(drop=True)
        
        # 添加年份列
        df['年份'] = year
        
        return df
    return None

# 加载数据
df_2024 = load_data(file_2024, 2024)
df_2025 = load_data(file_2025, 2025)

if df_2024 is not None and df_2025 is not None:
    # 合并数据
    df_all = pd.concat([df_2024, df_2025], ignore_index=True)
    
    # 数据概览
    st.header("数据概览")
    col1, col2, col3, col4,col5,col6 = st.columns(6)
    
    with col1:
        total_2024 = df_2024['业绩金额'].sum()
        st.metric("2024年总业绩", f"{total_2024:.0f}万元")
    
    with col2:
        total_2025 = df_2025['业绩金额'].sum()
        st.metric("2025年总业绩", f"{total_2025:.0f}万元")   
    with col3:
        growth_rate = ((total_2025 - total_2024) / total_2024 * 100) if total_2024 > 0 else 0
        st.metric("业绩增长率", f"{growth_rate:.1f}%")
    with col4:
        project_count = len(df_2024) 
        st.metric("2024年项目数", f"{project_count}")
    with col5:
        project_count =  len(df_2025)
        st.metric("2025年项目数", f"{project_count}")
    with col6:
        project_count = len(df_2024) + len(df_2025)
        st.metric("总项目数", f"{project_count}")
    
    # 主要分析
    st.header("核心分析")
    # 1. 年度业绩对比
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("年度业绩对比")
        # 重新计算年度数据，确保准确性
        yearly_performance = []
        yearly_performance.append({'年份': 2024, '总业绩': df_2024['业绩金额'].sum(), '项目数量': len(df_2024)})
        yearly_performance.append({'年份': 2025, '总业绩': df_2025['业绩金额'].sum(), '项目数量': len(df_2025)})
        yearly_data = pd.DataFrame(yearly_performance)
        yearly_data['年份'] = yearly_data['年份'].astype(str)
        fig1 = px.bar(yearly_data, x='年份', y='总业绩', 
                      title="上半年年度总业绩对比",
                    #   text='总业绩',width=800,  # 设置图片宽度
              height=500,  # 设置图片高度
              # 设置柱子颜色
              color='年份',  # 按年份分组颜色
              color_discrete_sequence=['#C0C0C0','#825D48'] 
              )
              
        # fig1.update_traces(texttemplate='%{text:.1f}万', textposition='outside')
        fig1.update_layout(xaxis=dict(tickmode='array', tickvals=[2024, 2025]))
        fig1.update_layout(plot_bgcolor='#E3EAF3', 
        paper_bgcolor='#E3EAF3',font=dict(color='#1B4965', size=12),  # 全局字体颜色
        title_font=dict(color='#1B4965', size=16),  # 标题单独设置
        xaxis=dict(tickfont=dict(color='#1B4965', size=12)),
        legend=dict(
        
        font=dict(color='#1B4965', size=12)  # 深色图例文字
        )
          # X轴刻度标签
        )
        fig1.update_yaxes(
        secondary_y=False,
        title_font=dict(color='#1B4965', size=14),  # 深色字体确保清晰
        tickfont=dict(color='#1B4965', size=12),
        gridcolor='#F6F8FA',  # 浅白色网格线
        zerolinecolor='#F6F8FA',  # 零轴线颜色与网格线一致
        dtick=5000,  # 固定刻度间隔为50000
        nticks=6,  # 限制刻度数量，只保留重要的
        
        )
        # fig1.update_layout(yaxis=dict(tickfont=dict(color='#1B4965', size=12)))
        
        st.plotly_chart(fig1, use_container_width=True)
        
        # 分析结果
        st.info(f"**业绩分析**：{'增长' if growth_rate > 0 else '下降'}{abs(growth_rate):.1f}%，总业绩差额{abs(total_2025-total_2024):.0f}万元")
    
    with col2:
        st.subheader("项目数量对比")
        yearly_data['年份'] = yearly_data['年份'].astype(str)
        fig2 = px.bar(yearly_data, x='年份', y='项目数量',
                      title="上半年年度项目数量对比",
                    #   text='项目数量',
                    width=800,  
              height=500,  # 设置图片高度
              # 设置柱子颜色
              color='年份',  # 按年份分组颜色
              color_discrete_sequence=['#C0C0C0','#825D48'] )
        # fig2.update_traces(texttemplate='%{text}个', textposition='outside')
        fig2.update_layout(xaxis=dict(tickmode='array', tickvals=[2024, 2025]))
        fig2.update_yaxes(
        secondary_y=False,
        title_font=dict(color='#1B4965', size=14),  # 深色字体确保清晰
        tickfont=dict(color='#1B4965', size=12),
        gridcolor='#F6F8FA',  # 浅白色网格线
        zerolinecolor='#F6F8FA',  # 零轴线颜色与网格线一致
        dtick=10,  # 固定刻度间隔为50000
        nticks=6,  # 限制刻度数量，只保留重要的
        
        )
        fig2.update_layout(plot_bgcolor='#E3EAF3', 
        paper_bgcolor='#E3EAF3',font=dict(color='#1B4965', size=12),  # 全局字体颜色
        title_font=dict(color='#1B4965', size=16),  # 标题单独设置
        xaxis=dict(tickfont=dict(color='#1B4965', size=12)),
        legend=dict(
        
        font=dict(color='#1B4965', size=12)  # 深色图例文字
        ))
        st.plotly_chart(fig2, use_container_width=True)
        
        # 分析结果
        project_change = len(df_2025) - len(df_2024)
        st.info(f"**项目分析**：项目数量{'增加' if project_change > 0 else '减少'}{abs(project_change)}个，平均项目业绩2024年{total_2024/len(df_2024):.1f}万元，2025年{total_2025/len(df_2025):.1f}万元")
    
    # 主要内容布局
    st.header("一.什么主要推动了总业绩的上升？")
    

    col1, col2 = st.columns([3, 2])

    with col1:
        st.subheader("1.业绩平台年度对比")
        
        # 准备绘图数据
        pivot_data = df_all.pivot_table(
            values='业绩金额', 
            index='年份', 
            columns='业绩平台', 
            aggfunc='sum',
            fill_value=0
        )
        
        # 计算百分比
        pivot_percentage = pivot_data.div(pivot_data.sum(axis=1), axis=0) * 100
        
        # 创建堆叠柱状图
        fig = go.Figure()
        
        # 定义简洁的颜色方案（与城市集中度分析保持一致）
        colors = ['#8B2635','#2E5984','#1E7E34','#7B68A6']
        
        # 为每个业绩平台添加数据
        for i, platform in enumerate(pivot_data.columns):
            fig.add_trace(go.Bar(
                name=platform,
                x=pivot_data.index,
                y=pivot_data[platform],
                marker_color=colors[i % len(colors)],
                
                customdata=[pivot_percentage.loc[year, platform] 
                        for year in pivot_data.index]
            ))
        
        # 更新图表布局
        fig.update_layout(
            barmode='stack',
            title='业绩平台年度业绩对比',
            xaxis_title='年份',
            yaxis_title='业绩金额 (万元)',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(color='#1B4965', size=12)  # 图例字体颜色
            ),
            height=635,
            showlegend=True,
            # 设置背景颜色和字体样式（参考代码的样式）
            plot_bgcolor='#E3EAF3',  # 图表背景色
            paper_bgcolor='#E3EAF3',  # 整体背景色
            font=dict(color='#1B4965', size=12),  # 全局字体颜色
            title_font=dict(color='#1B4965', size=16),  # 标题字体颜色
            # 设置x轴样式，确保只显示2024和2025
            xaxis=dict(
                tickmode='array', 
                tickvals=[2024, 2025],  # 明确指定x轴刻度值
                tickfont=dict(color='#1B4965', size=12),
                title_font=dict(color='#1B4965', size=14)
            ),
            # 设置y轴样式
            yaxis=dict(
                tickfont=dict(color='#1B4965', size=12),
                title_font=dict(color='#1B4965', size=14),
                gridcolor='#F6F8FA',  # 浅白色网格线
                zerolinecolor='#F6F8FA'  # 零轴线颜色与网格线一致
            )
        )
        
        # 添加总计标签
        total_2024 = pivot_data.loc[2024].sum()
        total_2025 = pivot_data.loc[2025].sum()
        
        fig.add_annotation(
            x=2024, y=total_2024,
            text=f"总计: {total_2024:.1f}万",
            showarrow=False,
            yshift=20,
            font=dict(size=12, color='#1B4965')  # 标注字体颜色
        )
        
        fig.add_annotation(
            x=2025, y=total_2025,
            text=f"总计: {total_2025:.1f}万",
            showarrow=False,
            yshift=20,
            font=dict(size=12, color='#1B4965')  # 标注字体颜色
        )
        
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("数据分析报告")
        
        # 计算增长数据
        growth_data = []
        for platform in pivot_data.columns:
            value_2024 = pivot_data.loc[2024, platform]
            value_2025 = pivot_data.loc[2025, platform]
            growth = value_2025 - value_2024
            growth_rate = (growth / value_2024 * 100) if value_2024 > 0 else 0
            
            growth_data.append({
                '业绩平台': platform,
                '2024年业绩': value_2024,
                '2025年业绩': value_2025,
                '增长量': growth,
                '增长率': growth_rate
            })
        
        growth_df = pd.DataFrame(growth_data)
        growth_df = growth_df.sort_values('增长量', ascending=False)
        
        # 总体增长分析
        total_growth = total_2025 - total_2024
        total_growth_rate = (total_growth / total_2024) * 100
        
        
        # 重点发现
        best_performer = growth_df.iloc[0]
        st.markdown("#### 重点发现")
        st.success(f"""
        **最大贡献平台：{best_performer['业绩平台']}**
        - 贡献了 {(best_performer['增长量']/total_growth)*100:.1f}% 的总增长
        - 增长量达到 {best_performer['增长量']:.1f}万元
        - 增长率为 {best_performer['增长率']:.1f}%
        """)
        # 各平台增长分析
        st.markdown("#### 各平台增长分析")
    
        # 创建2x2网格布局
        col1, col2 = st.columns(2)
        
        for i, row in growth_df.iterrows():
            contribution = (row['增长量'] / total_growth) * 100 if total_growth > 0 else 0
            
            if row['增长率'] > 0:
                growth_emoji = "📈"
                growth_color = "green"
            else:
                growth_emoji = "📉"
                growth_color = "red"
            
            # 根据索引决定显示在哪一列
            if i % 2 == 0:
                with col1:
                    st.markdown(f"""
                    **{growth_emoji} {row['业绩平台']}**
                    - 增长量: {row['增长量']:.1f}万元
                    - 增长率: {row['增长率']:.1f}%
                    - 贡献度: {contribution:.1f}%
                    """)
            else:
                with col2:
                    st.markdown(f"""
                    **{growth_emoji} {row['业绩平台']}**
                    - 增长量: {row['增长量']:.1f}万元
                    - 增长率: {row['增长率']:.1f}%
                    - 贡献度: {contribution:.1f}%
                    """)
    
    
    
    df_all = pd.concat([df_2024, df_2025], ignore_index=True)
    # 城市业绩增长分析


    # 城市业绩增长分析
    # 城市业绩增长分析
    st.subheader("2.1城市业绩增长分析")

    # 计算各城市24年和25年的业绩
    city_2024 = df_2024.groupby('城市')['业绩金额'].sum()
    city_2025 = df_2025.groupby('城市')['业绩金额'].sum()

    # 获取所有城市（包括只在一年出现的）
    all_cities = city_2024.index.union(city_2025.index)

    # 创建完整的数据框，缺失值填充为0
    city_2024_full = city_2024.reindex(all_cities, fill_value=0)
    city_2025_full = city_2025.reindex(all_cities, fill_value=0)

    # 计算增长值
    city_growth = city_2025_full - city_2024_full
    city_growth = city_growth.sort_values(ascending=False)

    # 设置阈值，使用绝对值的中位数或固定值
    threshold = max(city_growth.abs().median(), 500)  # 至少50000的阈值
    large_growth = city_growth[city_growth.abs() >= threshold]
    small_growth = city_growth[city_growth.abs() < threshold]

    # 图表1：较大的增长值
    if len(large_growth) > 0:
        fig1 = px.bar(
            x=large_growth.index.tolist(),
            y=large_growth.values.tolist(),
            title="主要城市业绩增长情况(业绩增长/减少绝对值>=500万元)",
            labels={'x': '城市', 'y': '增长金额'},
            color=large_growth.values.tolist(),
            color_continuous_scale='RdYlGn'
        )
        fig1.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig1, use_container_width=True)

    # 图表2：较小的增长值
    if len(small_growth) > 0:
        fig2 = px.bar(
            x=small_growth.index.tolist(),
            y=small_growth.values.tolist(),
            title="其他城市业绩增长情况(业绩增长/减少绝对值<500万元)",
            labels={'x': '城市', 'y': '增长金额'},
            color=small_growth.values.tolist(),
            color_continuous_scale='RdYlGn'
        )
        fig2.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    # 显示数据表
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("**增长最多的城市:**")
        top_growth = city_growth.head(5)
        for city, growth in top_growth.items():
            st.write(f"{city}: {growth:,.0f}")

    with col2:
        st.write("**新增业绩城市:**")
        new_cities = city_growth[(city_2024_full == 0) & (city_2025_full > 0)]
        for city, growth in new_cities.head(5).items():
            st.write(f"{city}: {growth:,.0f}")

    with col3:
        st.write("**业绩归零城市:**")
        zero_cities = city_growth[(city_2024_full > 0) & (city_2025_full == 0)]
        for city, growth in zero_cities.tail(5).items():
            st.write(f"{city}: {growth:,.0f}")
    

    # 重点城市业绩增长分析
    st.subheader("2.2重点城市业绩增长分析")

    # 重点城市列表
    key_cities = ['广州', '北京', '成都', '上海', '杭州', '重庆', '深圳', '珠海', '天津', '苏州']

    # 筛选重点城市数据
    key_cities_data = []
    no_data_cities = []

    for city in key_cities:
        if city in city_growth.index:
            key_cities_data.append({'城市': city, '增长额': city_growth[city]})
        else:
            no_data_cities.append(city)

    # 显示无数据的城市
    if no_data_cities:
        st.write(f"**上半年无业绩数据的重点城市:** {', '.join(no_data_cities)}")

    # 创建重点城市图表
    if key_cities_data:
        key_cities_df = pd.DataFrame(key_cities_data)
        key_cities_df = key_cities_df.sort_values('增长额', ascending=False)
        
        # 计算平均增长额
        avg_growth = key_cities_df['增长额'].mean()
        
        # 根据增长额正负设置颜色
        colors = []
        for value in key_cities_df['增长额']:
            if value >= 0:
                colors.append('#8B2635')  # 正增长用红色（与背景色搭配的深红色）
            else:
                colors.append('#1E7E34')  # 负增长用绿色（与背景色搭配的深绿色）
        
        # 创建图表
        fig3 = go.Figure()
        
        # 添加柱状图
        fig3.add_trace(go.Bar(
            x=key_cities_df['城市'].tolist(),
            y=key_cities_df['增长额'].tolist(),
            marker_color=colors,
            showlegend=False
        ))
        
        # 添加平均线
        fig3.add_hline(
            y=avg_growth, 
            line_dash="dash", 
            line_color="rgba(0,0,0,0.6)",  # 与背景色搭配的棕色线条
            line_width=2,
            annotation_text=f"平均增长额: {avg_growth:,.0f}",
            annotation_position="top left",
            annotation_font=dict(color='#1B4965', size=12)
        )
        
        # 更新图表布局（延续参考代码的配色）
        fig3.update_layout(
            title="重点城市业绩增长情况",
            xaxis_title="城市",
            yaxis_title="增长金额",
            height=400,
            showlegend=False,
            # 使用参考代码的背景和字体配色
            plot_bgcolor='#E3EAF3',  # 图表背景色
            paper_bgcolor='#E3EAF3',  # 整体背景色
            font=dict(color='#1B4965', size=12),  # 全局字体颜色
            title_font=dict(color='#1B4965', size=16),  # 标题字体颜色
            xaxis=dict(
                tickfont=dict(color='#1B4965', size=12),
                title_font=dict(color='#1B4965', size=14)
            ),
            yaxis=dict(
                tickfont=dict(color='#1B4965', size=12),
                title_font=dict(color='#1B4965', size=14),
                gridcolor='#F6F8FA',  # 浅白色网格线
                zerolinecolor='#F6F8FA'  # 零轴线颜色与网格线一致
            )
        )
        
        st.plotly_chart(fig3, use_container_width=True)
        
    else:
        st.write("重点城市均无业绩数据")
    

    # 一级业态分析
    # 一级业态分析
    st.subheader("3.1一级业态业绩增长分析")

    # 计算各业态24年和25年的业绩
    format_2024 = df_2024.groupby('一级业态')['业绩金额'].sum()
    format_2025 = df_2025.groupby('一级业态')['业绩金额'].sum()

    # 获取所有业态
    all_formats = format_2024.index.union(format_2025.index)

    # 创建完整的数据框
    format_2024_full = format_2024.reindex(all_formats, fill_value=0)
    format_2025_full = format_2025.reindex(all_formats, fill_value=0)

    # 计算增长量和增长率
    format_growth = format_2025_full - format_2024_full

    # 计算增长率（特别处理24年为0的情况）
    format_growth_rate = []
    for format_name in all_formats:
        if format_2024_full[format_name] == 0:
            # 24年没有业绩的情况，增长率设为0%
            format_growth_rate.append(0)
        else:
            # 正常计算增长率
            rate = ((format_2025_full[format_name] - format_2024_full[format_name]) / format_2024_full[format_name]) * 100
            format_growth_rate.append(rate)

    format_growth_rate = pd.Series(format_growth_rate, index=all_formats)

    # 按增长量排序
    format_growth_sorted = format_growth.sort_values(ascending=False)
    format_growth_rate_sorted = format_growth_rate.reindex(format_growth_sorted.index)

    # 创建组合图表
    fig4 = go.Figure()

    # 添加柱状图（增长量）- 正增长用红色，负增长用绿色
    colors = []
    for x in format_growth_sorted.values:
        if x >= 0:
            colors.append('#8B2635')  # 正增长用红色（与背景色搭配的深红色）
        else:
            colors.append('#1E7E34')  # 负增长用绿色（与背景色搭配的深绿色）

    fig4.add_trace(go.Bar(
        x=format_growth_sorted.index.tolist(),
        y=format_growth_sorted.values.tolist(),
        name='增长量',
        marker_color=colors,
        yaxis='y'
    ))

    # 分离增长率为0和非0的数据点
    zero_growth_indices = []
    zero_growth_values = []
    non_zero_growth_indices = []
    non_zero_growth_values = []
    non_zero_growth_rates = []

    for i, (index, rate) in enumerate(zip(format_growth_sorted.index, format_growth_rate_sorted.values)):
        if rate == 0:
            zero_growth_indices.append(index)
            zero_growth_values.append(rate)
        else:
            non_zero_growth_indices.append(index)
            non_zero_growth_values.append(rate)
            non_zero_growth_rates.append(rate)

    # 添加折线图（增长率非0的点）
    if non_zero_growth_indices:
        fig4.add_trace(go.Scatter(
            x=non_zero_growth_indices,
            y=non_zero_growth_values,
            mode='lines+markers+text',
            name='增长率(%)',
            line=dict(color='rgba(0,0,0,0.6)', width=3),
            marker=dict(size=8, color='rgba(0,0,0,0.6)', symbol='circle'),
            text=[f'{int(rate)}%' for rate in non_zero_growth_rates],  # 显示整数部分的增长率
            textposition='top center',
            textfont=dict(color='#1B4965', size=10),  # 文字颜色与背景搭配
            yaxis='y2',
            connectgaps=True  # 连接间隙
        ))

    # 添加新增业态的特殊标记（增长率为0的点）
    if zero_growth_indices:
        fig4.add_trace(go.Scatter(
            x=zero_growth_indices,
            y=zero_growth_values,
            mode='markers',
            name='新增业态',
            marker=dict(
                size=8, 
                color='rgba(0,0,0,0.6)', 
                symbol='triangle-up',  # 小三角形
                line=dict(width=2, color='rgba(0,0,0,0.6)')
            ),
            yaxis='y2',
            showlegend=True
        ))

    # 设置布局（延续参考代码的配色）
    fig4.update_layout(
        title="一级业态业绩增长量与增长率分析",
        xaxis_title="一级业态",
        yaxis=dict(
            title="增长量",
            side="left",
            tickfont=dict(color='#1B4965', size=12),
            title_font=dict(color='#1B4965', size=14),
            gridcolor='#F6F8FA',  # 浅白色网格线
            zerolinecolor='#F6F8FA'  # 零轴线颜色与网格线一致
        ),
        yaxis2=dict(
            title="增长率(%)",
            side="right",
            overlaying="y",
            tickfont=dict(color='#1B4965', size=12),
            title_font=dict(color='#1B4965', size=14),
            gridcolor='#F6F8FA',  # 浅白色网格线
            zerolinecolor='#F6F8FA'  # 零轴线颜色与网格线一致
        ),
        height=500,
        legend=dict(
            x=0.7, 
            y=1,
            font=dict(color='#1B4965', size=12)  # 图例字体颜色
        ),
        # 使用参考代码的背景和字体配色
        plot_bgcolor='#E3EAF3',  # 图表背景色
        paper_bgcolor='#E3EAF3',  # 整体背景色
        font=dict(color='#1B4965', size=12),  # 全局字体颜色
        title_font=dict(color='#1B4965', size=16),  # 标题字体颜色
        xaxis=dict(
            tickfont=dict(color='#1B4965', size=12),
            title_font=dict(color='#1B4965', size=14)
        )
    )

    st.plotly_chart(fig4, use_container_width=True)

    # 显示业态详细数据
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("**增长最多的业态:**")
        top_format_growth = format_growth_sorted.head(3)
        for format_name, growth in top_format_growth.items():
            rate = format_growth_rate_sorted[format_name]
            st.write(f"{format_name}: {growth:,.0f} ({rate:.1f}%)")

    with col2:
        st.write("**新增业态:**")
        new_formats = format_growth[(format_2024_full == 0) & (format_2025_full > 0)]
        for format_name, growth in new_formats.items():
            st.write(f"{format_name}: {growth:,.0f}")

    with col3:
        st.write("**业绩归零业态:**")
        zero_formats = format_growth[(format_2024_full > 0) & (format_2025_full == 0)]
        for format_name, growth in zero_formats.items():
            st.write(f"{format_name}: {growth:,.0f}")
    

    # 一级业态占比分析
    st.subheader("3.2一级业态占比分析")

    # 计算各年度占比
    format_2024_pct = (format_2024_full / format_2024_full.sum()) * 100
    format_2025_pct = (format_2025_full / format_2025_full.sum()) * 100

    # 计算占比变化
    format_pct_change = format_2025_pct - format_2024_pct

    # 按增长量排序（与上一个图表保持一致）
    format_pct_change_sorted = format_pct_change.reindex(format_growth_sorted.index)

    # 创建左右两列布局
    col1, col2 = st.columns(2)

    with col1:
        st.write("**堆叠柱状图：24年vs25年占比对比**")
        
        # 固定的"其他"业态
        other_formats = ['城镇景区', '居住物业', '教研物业']
        
        # 处理24年数据
        format_2024_display = format_2024_pct.copy()
        # 提取"其他"业态并合并
        other_2024_pct = sum([format_2024_display.get(fmt, 0) for fmt in other_formats])
        # 移除原始的"其他"业态
        for fmt in other_formats:
            if fmt in format_2024_display:
                format_2024_display.drop(fmt, inplace=True)
        # 添加合并后的"其他"
        if other_2024_pct > 0:
            format_2024_display['其他'] = other_2024_pct
        
        # 处理25年数据
        format_2025_display = format_2025_pct.copy()
        # 提取"其他"业态并合并
        other_2025_pct = sum([format_2025_display.get(fmt, 0) for fmt in other_formats])
        # 移除原始的"其他"业态
        for fmt in other_formats:
            if fmt in format_2025_display:
                format_2025_display.drop(fmt, inplace=True)
        # 添加合并后的"其他"
        if other_2025_pct > 0:
            format_2025_display['其他'] = other_2025_pct
        
        # 定义业态顺序和颜色
        format_order = ['产业园物业', '写字楼物业', '商业物业', '交通物业', '医疗物业', '公共物业', '其他']
        format_colors = {
            '产业园物业': '#8B2635',  # 红色
            '写字楼物业': '#2E5984',  # 蓝色
            '商业物业': '#1E7E34',    # 绿色
            '交通物业': '#D4A843',    # 黄色
            '医疗物业': '#6C757D',    # 紫色
            '公共物业': '#7B68A6',    # 灰色
            '其他': '#5F9EA0'         # 粉色
        }
        
        # 获取实际存在的业态（按指定顺序）
        all_display_formats = list(set(format_2024_display.index) | set(format_2025_display.index))
        ordered_formats = [fmt for fmt in format_order if fmt in all_display_formats]
        
        # 创建堆叠柱状图
        fig5 = go.Figure()
        
        # 按指定顺序为每个业态添加一个堆叠层
        for format_name in ordered_formats:
            pct_2024 = format_2024_display.get(format_name, 0)
            pct_2025 = format_2025_display.get(format_name, 0)
            
            fig5.add_trace(go.Bar(
                name=format_name,
                x=['2024年', '2025年'],
                y=[pct_2024, pct_2025],
                marker_color=format_colors.get(format_name, '#000000')
            ))
        
        fig5.update_layout(
            title="业态占比对比 (堆叠柱状图)",
            barmode='stack',
            yaxis_title="占比 (%)",
            height=500,
            legend=dict(
                orientation="v", 
                x=1.05, 
                y=1,
                font=dict(color='#1B4965', size=12)  # 图例字体颜色
            ),
            # 使用参考代码的背景和字体配色
            plot_bgcolor='#E3EAF3',  # 图表背景色
            paper_bgcolor='#E3EAF3',  # 整体背景色
            font=dict(color='#1B4965', size=12),  # 全局字体颜色
            title_font=dict(color='#1B4965', size=16),  # 标题字体颜色
            xaxis=dict(
                tickfont=dict(color='#1B4965', size=12),
                title_font=dict(color='#1B4965', size=14),
                tickmode='array',
                tickvals=[0, 1],  # 确保只显示两个年份
                ticktext=['2024年', '2025年']
            ),
            yaxis=dict(
                tickfont=dict(color='#1B4965', size=12),
                title_font=dict(color='#1B4965', size=14),
                gridcolor='#F6F8FA',  # 浅白色网格线
                zerolinecolor='#F6F8FA'  # 零轴线颜色与网格线一致
            )
        )
        
        st.plotly_chart(fig5, use_container_width=True)
        
        # 计算商业业态的占比和变化率
        commercial_formats = ['产业园物业', '写字楼物业', '商业物业']
        
        # 计算2024年商业业态总占比
        commercial_2024_total = sum([format_2024_display.get(fmt, 0) for fmt in commercial_formats])
        
        # 计算2025年商业业态总占比
        commercial_2025_total = sum([format_2025_display.get(fmt, 0) for fmt in commercial_formats])
        
        # 计算变化率
        if commercial_2024_total > 0:
            change_rate = ((commercial_2025_total - commercial_2024_total) / commercial_2024_total) * 100
        else:
            change_rate = 0
        
        # 显示商业业态分析
        st.write("**商业业态分析:**")
        st.write(f"• 2024年商业业态总占比: {commercial_2024_total:.1f}%")
        st.write(f"• 2025年商业业态总占比: {commercial_2025_total:.1f}%")
        
        if change_rate > 0:
            st.write(f"• 商业业态占比增长: +{change_rate:.1f}%")
        elif change_rate < 0:
            st.write(f"• 商业业态占比下降: {change_rate:.1f}%")
        else:
            st.write(f"• 商业业态占比保持稳定")
        
        
        
        # 说明"其他"的内容
        st.write("**'其他'业态详情:**")
        other_2024_details = []
        other_2025_details = []
        
        for fmt in other_formats:
            pct_2024 = format_2024_pct.get(fmt, 0)
            pct_2025 = format_2025_pct.get(fmt, 0)
            if pct_2024 > 0:
                other_2024_details.append(f"{fmt}({pct_2024:.1f}%)")
            if pct_2025 > 0:
                other_2025_details.append(f"{fmt}({pct_2025:.1f}%)")
        
        if other_2024_details:
            st.write(f"2024年 - 其他业态({other_2024_pct:.1f}%)：{', '.join(other_2024_details)}")
        if other_2025_details:
            st.write(f"2025年 - 其他业态({other_2025_pct:.1f}%)：{', '.join(other_2025_details)}")
    with col2:
        st.write("**折线图：占比变化趋势**")
        
        # 创建折线图
        fig6 = go.Figure()
        
        fig6.add_trace(go.Scatter(
            x=list(range(len(format_pct_change_sorted))),
            y=format_pct_change_sorted.values.tolist(),
            mode='lines+markers',
            name='占比变化',
            line=dict(color='blue', width=3),
            marker=dict(size=8, color=['green' if x >= 0 else 'red' for x in format_pct_change_sorted.values])
        ))
        
        # 添加零线
        fig6.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.7)
        
        fig6.update_layout(
            title="业态占比变化 (按增长量排序)",
            xaxis_title="业态 (按增长量排序)",
            yaxis_title="占比变化 (%)",
            height=500,
            xaxis=dict(
                tickmode='array',
                tickvals=list(range(len(format_pct_change_sorted))),
                ticktext=format_pct_change_sorted.index.tolist(),
                tickangle=45
            )
        )
        
        st.plotly_chart(fig6, use_container_width=True)

    # 显示占比变化详细数据
    # st.write("**占比变化详细数据:**")
    # change_data = []
    # for format_name in format_pct_change_sorted.index:
    #     pct_24 = format_2024_pct[format_name]
    #     pct_25 = format_2025_pct[format_name]
    #     change = format_pct_change_sorted[format_name]
    #     change_data.append(f"{format_name}: {pct_24:.1f}% → {pct_25:.1f}% (变化: {change:+.1f}%)")

    # for data in change_data:
    #     st.write(data)
    # 一级业态深度分析
    st.subheader("一级业态深度分析")

    # 基于四个维度的分析结果
    analysis_results = []

    for format_name in all_formats:
        growth_amount = format_growth[format_name]
        growth_rate = format_growth_rate[format_name]
        pct_2024 = format_2024_pct[format_name]
        pct_2025 = format_2025_pct[format_name]
        pct_change = format_pct_change[format_name]
        
        # 分析逻辑
        if growth_amount > 0 and pct_change > 0:
            if growth_rate > 20:
                status = "🚀 高速增长"
                analysis = "业绩增长强劲，市场份额扩大，发展势头良好"
            elif growth_rate > 0:
                status = "📈 稳健增长"
                analysis = "业绩稳步增长，市场地位稳固"
            elif growth_rate == 0 and pct_2024 == 0:
                status = "🆕 新兴业态"
                analysis = "2024年无业绩，2025年开始产生业绩，属于新兴业态"
            else:
                status = "⚠️ 虚假繁荣"
                analysis = "占比提升但增长率较低，可能是其他业态下滑导致的相对优势"
        elif growth_amount > 0 and pct_change < 0:
            status = "🔄 增长但占比下降"
            analysis = "业绩有所增长，但增长速度低于市场平均水平"
        elif growth_amount < 0 and pct_change > 0:
            status = "🤔 异常情况"
            analysis = "业绩下降但占比提升，可能存在数据异常或其他业态大幅下滑"
        elif growth_amount < 0 and pct_change < 0:
            status = "📉 双重下滑"
            analysis = "业绩和市场份额均下降，需要关注业态发展趋势"
        elif growth_amount == 0 and pct_2024 == 0:
            status = "🆕 新兴业态"
            analysis = "2025年新增业态，发展潜力待观察"
        elif growth_amount == 0 and pct_2025 == 0:
            status = "❌ 退出业态"
            analysis = "2025年业绩归零，业态可能面临退出"
        else:
            status = "➖ 无变化"
            analysis = "业绩和占比基本无变化，保持稳定"
        
        analysis_results.append({
            '业态': format_name,
            '状态': status,
            '分析': analysis,
            '增长量': growth_amount,
            '增长率': growth_rate,
            '占比变化': pct_change
        })

    # 按增长量排序展示分析结果
    analysis_df = pd.DataFrame(analysis_results)
    analysis_df = analysis_df.sort_values('增长量', ascending=False)

    # 使用左右两列布局
    col_left, col_right = st.columns(2)

    # 左列：业态发展态势分析
    with col_left:
        st.write("### 🎯 业态发展态势分析")
        
        # 优秀表现业态
        excellent_formats = analysis_df[analysis_df['状态'].str.contains('高速增长|稳健增长|新兴业态')]
        if len(excellent_formats) > 0:
            st.write("**🌟 表现优秀的业态:**")
            for _, row in excellent_formats.iterrows():
                with st.expander(f"**{row['业态']}** {row['状态']}", expanded=True):
                    st.write(f"📝 {row['分析']}")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("增长量", f"{row['增长量']:,.0f}")
                    with col2:
                        if row['增长率'] == 0 and row['增长量'] > 0:
                            st.metric("增长率", "新兴业态")
                        else:
                            st.metric("增长率", f"{row['增长率']:.1f}%")
                    with col3:
                        st.metric("占比变化", f"{row['占比变化']:+.1f}%")
        
        # 需要关注的业态
        concern_formats = analysis_df[analysis_df['状态'].str.contains('虚假繁荣|异常情况|双重下滑')]
        if len(concern_formats) > 0:
            st.write("**⚠️ 需要关注的业态:**")
            for _, row in concern_formats.iterrows():
                with st.expander(f"**{row['业态']}** {row['状态']}", expanded=False):
                    st.write(f"📝 {row['分析']}")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("增长量", f"{row['增长量']:,.0f}")
                    with col2:
                        st.metric("增长率", f"{row['增长率']:.1f}%")
                    with col3:
                        st.metric("占比变化", f"{row['占比变化']:+.1f}%")

    # 右列：整体市场分析和风险提示
    with col_right:
        st.write("### 📈 整体市场分析")
        
        total_growth = format_growth.sum()
        positive_growth_count = len(format_growth[format_growth > 0])
        negative_growth_count = len(format_growth[format_growth < 0])
        total_formats = len(all_formats)

        # 关键指标卡片
        st.write("**核心指标:**")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("总体增长量", f"{total_growth:,.0f}")
            st.metric("增长业态数", f"{positive_growth_count}/{total_formats}")
        with col2:
            st.metric("下降业态数", f"{negative_growth_count}/{total_formats}")
            growth_ratio = (positive_growth_count / total_formats * 100) if total_formats > 0 else 0
            st.metric("增长业态占比", f"{growth_ratio:.1f}%")

        # 市场集中度分析
        st.write("**市场集中度分析:**")
        top3_formats = analysis_df.head(3)
        top3_growth_sum = top3_formats['增长量'].sum()
        top3_contribution = (top3_growth_sum / total_growth * 100) if total_growth > 0 else 0
        
        st.info(f"前3大业态贡献了 **{top3_contribution:.1f}%** 的增长量")
        st.write("**主要增长驱动力:**")
        for i, (_, row) in enumerate(top3_formats.iterrows(), 1):
            st.write(f"{i}. {row['业态']} ({row['状态']})")
        
        # 风险提示
        risk_formats = analysis_df[analysis_df['状态'].str.contains('虚假繁荣|异常情况|双重下滑')]
        if len(risk_formats) > 0:
            st.write("**⚠️ 风险提示:**")
            st.error(f"共有 **{len(risk_formats)}** 个业态存在潜在风险")
            st.write("**建议重点关注:**")
            for _, row in risk_formats.iterrows():
                st.write(f"• {row['业态']} - {row['状态']}")
        
        # 新兴和退出业态（从需要关注的业态中移除新兴业态）
        new_exit_formats = analysis_df[analysis_df['状态'].str.contains('退出业态')]
        if len(new_exit_formats) > 0:
            st.write("**🔄 业态变化:**")
            for _, row in new_exit_formats.iterrows():
                st.warning(f"**{row['业态']}** {row['状态']} - {row['分析']}")

    # 底部：业态排名总览表格
    st.write("### 📋 业态排名总览")
    # 创建简洁的总览表格
    display_df = analysis_df[['业态', '状态', '增长量', '增长率', '占比变化']].copy()
    display_df['增长量'] = display_df['增长量'].apply(lambda x: f"{x:,.0f}")
    # 对于新兴业态，显示"新兴业态"而不是"0.0%"
    display_df['增长率_显示'] = display_df.apply(lambda row: "新兴业态" if row['增长率'] == 0 and "🆕 新兴业态" in row['状态'] else f"{row['增长率']:.1f}%", axis=1)
    display_df['占比变化'] = display_df['占比变化'].apply(lambda x: f"{x:+.1f}%")

    # 重新排列列顺序，用新的增长率显示列
    display_df = display_df[['业态', '状态', '增长量', '增长率_显示', '占比变化']].copy()
    display_df.rename(columns={'增长率_显示': '增长率'}, inplace=True)

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "业态": st.column_config.TextColumn("业态", width="medium"),
            "状态": st.column_config.TextColumn("发展状态", width="medium"),
            "增长量": st.column_config.TextColumn("增长量", width="small"),
            "增长率": st.column_config.TextColumn("增长率", width="small"),
            "占比变化": st.column_config.TextColumn("占比变化", width="small"),
        }
    )




    cities_with_2024_data = df_all[df_all['年份'] == 2024]['城市'].unique()
    filtered_cities_data = df_all[df_all['城市'].isin(cities_with_2024_data)]
    
    # 项目质量下降分析
    st.markdown("---")
    st.subheader("三.项目质量下降分析")

    # 筛选出在24年有业绩的城市
    cities_with_2024_data = df_all[df_all['年份'] == 2024]['城市'].unique()
    filtered_cities_data = df_all[df_all['城市'].isin(cities_with_2024_data)]

    # 计算每个城市每年的项目数量和总业绩
    city_stats = filtered_cities_data.groupby(['城市', '年份']).agg({
        '业绩金额': ['sum', 'count', 'mean']
    }).reset_index()

    city_stats.columns = ['城市', '年份', '总业绩', '项目数量', '平均项目业绩']

    # 计算每个城市的总业绩（用于排序）
    city_total_performance = city_stats.groupby('城市')['总业绩'].sum().reset_index()
    city_total_performance = city_total_performance.sort_values('总业绩', ascending=False)

    # 重新排序城市数据
    city_stats['城市'] = pd.Categorical(city_stats['城市'], categories=city_total_performance['城市'], ordered=True)
    city_stats = city_stats.sort_values(['城市', '年份'])

    # 计算平均项目业绩下降率
    decline_rates = {}
    for city in cities_with_2024_data:
        city_data = city_stats[city_stats['城市'] == city]
        avg_2024 = city_data[city_data['年份'] == 2024]['平均项目业绩'].values
        avg_2025 = city_data[city_data['年份'] == 2025]['平均项目业绩'].values
        
        if len(avg_2024) > 0 and len(avg_2025) > 0:
            decline_rate = ((avg_2025[0] - avg_2024[0]) / avg_2024[0]) * 100
            decline_rates[city] = decline_rate
        elif len(avg_2024) > 0:
            decline_rates[city] = -100  # 2025年无数据，视为完全下降

    # 创建两列布局
    col_chart, col_analysis = st.columns([2, 1])

    with col_chart:
        # 创建分组柱状图加折线图
        fig_quality = make_subplots(
            specs=[[{"secondary_y": True}]],
            # subplot_titles=("城市项目质量对比分析",）
        )
        
        # 添加分组柱状图
        cities_ordered = city_total_performance['城市'].tolist()
        
        # 2024年数据
        data_2024 = city_stats[city_stats['年份'] == 2024].set_index('城市').reindex(cities_ordered)
        fig_quality.add_trace(
            go.Bar(
                name='2024年平均项目业绩',
                x=cities_ordered,
                y=data_2024['平均项目业绩'].fillna(0),
                marker_color='#4ECDC4',
                text=[f'{val:.1f}万' for val in data_2024['平均项目业绩'].fillna(0)],
                textposition='outside',
                yaxis='y1'
            ),
            secondary_y=False
        )
        
        # 2025年数据
        data_2025 = city_stats[city_stats['年份'] == 2025].set_index('城市').reindex(cities_ordered)
        fig_quality.add_trace(
            go.Bar(
                name='2025年平均项目业绩',
                x=cities_ordered,
                y=data_2025['平均项目业绩'].fillna(0),
                marker_color='#FF8C94',
                text=[f'{val:.1f}万' for val in data_2025['平均项目业绩'].fillna(0)],
                textposition='outside',
                yaxis='y1'
            ),
            secondary_y=False
        )
        
        # 添加折线图（下降率）
        decline_values = [decline_rates.get(city, 0) for city in cities_ordered]
        fig_quality.add_trace(
            go.Scatter(
                name='平均项目业绩变化率',
                x=cities_ordered,
                y=decline_values,
                mode='lines+markers',
                line=dict(color='red', width=3),
                marker=dict(size=8, color='red'),
                text=[f'{val:.1f}%' for val in decline_values],
                textposition='top center',
                yaxis='y2'
            ),
            secondary_y=True
        )
        
        # 更新图表布局
        fig_quality.update_layout(
            
            xaxis_title='城市（按总业绩排序）',
            barmode='group',
            height=680,
            template='plotly_white',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        # 设置Y轴标签
        fig_quality.update_yaxes(title_text="平均项目业绩 (万元)", secondary_y=False)
        fig_quality.update_yaxes(title_text="变化率 (%)", secondary_y=True)
        
        st.plotly_chart(fig_quality, use_container_width=True)

    with col_analysis:
        st.markdown("#### 📊 项目质量分析")
        
        # 计算总体平均项目业绩
        total_avg_2024 = city_stats[city_stats['年份'] == 2024]['平均项目业绩'].mean()
        total_avg_2025 = city_stats[city_stats['年份'] == 2025]['平均项目业绩'].mean()
        overall_avg = city_stats['平均项目业绩'].mean()
        overall_decline = ((total_avg_2025 - total_avg_2024) / total_avg_2024) * 100 if total_avg_2024 > 0 else 0
        
        # st.markdown("**总体平均项目业绩对比：**")
        # st.info(f"""
        # - 总体平均: {overall_avg:.1f}万元
        # - 2024年平均: {total_avg_2024:.1f}万元  
        # - 2025年平均: {total_avg_2025:.1f}万元
        # - 总体变化率: {overall_decline:.1f}%
        # """)
        
        # 找出下降率最大的三个城市（排除-100%的城市）
        filtered_decline_rates = {city: rate for city, rate in decline_rates.items() if rate != -100 and rate < 0}
        decline_sorted = sorted(filtered_decline_rates.items(), key=lambda x: x[1])[:3]
        
        st.markdown("**平均项目业绩下降率最大的城市：**")
        for i, (city, decline_rate) in enumerate(decline_sorted, 1):
            city_2024_avg = city_stats[(city_stats['城市'] == city) & (city_stats['年份'] == 2024)]['平均项目业绩'].values
            city_2025_avg = city_stats[(city_stats['城市'] == city) & (city_stats['年份'] == 2025)]['平均项目业绩'].values
            
            avg_2024_str = f"{city_2024_avg[0]:.1f}万" if len(city_2024_avg) > 0 else "无数据"
            avg_2025_str = f"{city_2025_avg[0]:.1f}万" if len(city_2025_avg) > 0 else "无数据"
            
            st.markdown(f"""
            **{i}. {city}**
            - 下降率: {decline_rate:.1f}%
            - 2024年: {avg_2024_str}
            - 2025年: {avg_2025_str}
            """)

    
    
    st.subheader("四. 城市业绩分析")

    # 定义重点城市列表
    key_cities = ['广州', '北京', '成都', '上海', '杭州', '重庆', '深圳', '珠海', '天津', '苏州']

    # 基于您的数据结构计算重点城市业绩数据
    city_performance = []
    cities_without_data = []  # 记录没有业绩数据的城市

    for city in key_cities:
        # 分别从2024年和2025年数据集中获取该城市的业绩
        city_2024 = df_2024[df_2024['城市'] == city]['业绩金额'].sum()
        city_2025 = df_2025[df_2025['城市'] == city]['业绩金额'].sum()
        
        # 检查是否有业绩数据
        if city_2024 == 0 and city_2025 == 0:
            cities_without_data.append(city)
            continue  # 跳过没有数据的城市
        
        # 计算增长率
        if city_2024 > 0:
            growth_rate = ((city_2025 - city_2024) / city_2024) * 100
        else:
            growth_rate = 0 if city_2025 == 0 else 100  # 新兴城市设为100%
        
        # 计算总业绩
        total_performance = city_2024 + city_2025
        
        city_performance.append({
            '城市': city,
            '2024年业绩': city_2024,
            '2025年业绩': city_2025,
            '总业绩': total_performance,
            '增长率': growth_rate
        })

    # 转换为DataFrame并按总业绩排序
    city_df = pd.DataFrame(city_performance)
    city_df = city_df.sort_values('总业绩', ascending=False)

    # 显示没有业绩数据的重点城市
    if cities_without_data:
        st.warning(f"以下重点城市2024年和2025年上半年均无业绩数据：{', '.join(cities_without_data)}")

    # 检查是否有数据可以显示
    if len(city_df) == 0:
        st.warning("所有重点城市均无业绩数据")
    else:
        # 计算平均增长率
        avg_growth_rate = city_df['增长率'].mean()

        # 创建图表
        fig = go.Figure()

        # 添加2024年业绩柱状图
        fig.add_trace(go.Bar(
            name='2024年业绩',
            x=city_df['城市'],
            y=city_df['2024年业绩'],
            marker_color='#C0C0C0',
            # text=city_df['2024年业绩'].apply(lambda x: f'{x:,.0f}'),
            # textposition='outside',
            # textfont=dict(size=10, color='white'),
            yaxis='y'
        ))

        # 添加2025年业绩柱状图
        fig.add_trace(go.Bar(
            name='2025年业绩',
            x=city_df['城市'],
            y=city_df['2025年业绩'],
            marker_color='#825D48',
            # text=city_df['2025年业绩'].apply(lambda x: f'{x:,.0f}'),
            # textposition='outside',
            # textfont=dict(size=10, color='white'),
            yaxis='y'
        ))

        # 添加增长率折线图
        fig.add_trace(go.Scatter(
            name='增长率',
            x=city_df['城市'],
            y=city_df['增长率'],
            mode='lines+markers+text',
            
            marker=dict(size=8, color='rgba(0,0,0,0.6)'),
            line=dict(color='rgba(0,0,0,0.6)', width=3),
            text=city_df['增长率'].apply(lambda x: f'{int(x)}%'),  # 修改为显示整数部分
            textposition='top center',
            textfont=dict(size=12, color='#1B4965'),
            yaxis='y2'
        ))

        # 构建标题，包含没有数据的城市信息
        chart_title = '重点城市业绩分析'
        if cities_without_data:
            chart_title += f'<br><sub>上半年无业绩数据的重点城市：{", ".join(cities_without_data)}</sub>'
        # 更新布局 - 调整为深色主题
        # 更新布局 - 调整为深色主题
        fig.update_layout(
        title=chart_title,
        title_font=dict(color='#1B4965', size=16),  # 深色标题
        xaxis_title='城市',
        xaxis_title_font=dict(color='#1B4965', size=14),  # 深色x轴标题
        yaxis=dict(
            title='业绩金额',
            side='left',
            tickformat=',.',
            title_font=dict(color='#1B4965', size=14),  # 深色字体确保清晰
            tickfont=dict(color='#1B4965', size=12),
            gridcolor='#F6F8FA',  # 浅白色网格线
            zerolinecolor='#F6F8FA',
            dtick=5000  # 零轴线颜色与网格线一致
        ),
        yaxis2=dict(
            title='增长率 (%)',
            side='right',
            overlaying='y',
            tickformat='.1f',
            title_font=dict(color='#1B4965', size=14),  # 深色字体确保清晰
            tickfont=dict(color='#1B4965', size=12),
            gridcolor='#F6F8FA',  # 浅白色网格线
            zerolinecolor='#F6F8FA',  # 零轴线颜色与网格线一致
        ),
        xaxis=dict(
            title_font=dict(color='#1B4965', size=14),  # 深色字体确保清晰
            tickfont=dict(color='#1B4965', size=12),
            gridcolor='#F6F8FA',  # 浅白色网格线
            showgrid=False,  # 隐藏x轴网格线
            zerolinecolor='#F6F8FA'
        ),
        barmode='group',
        height=600,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color='#1B4965', size=12)  # 深色图例文字
        ),
        font=dict(size=12, color='#1B4965'),  # 深色字体
        plot_bgcolor='#E3EAF3',  # 与PPT背景协调的浅色背景
        paper_bgcolor='#E3EAF3'  # 与PPT背景完全一致
    )

       
        
        
       
        
        

        # 显示图表
        st.plotly_chart(fig, use_container_width=True)

        
        # 添加关键洞察
        st.write("### 🔍 关键洞察")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        top_city = city_df.iloc[0]
        st.metric("业绩最高城市", top_city['城市'], f"{top_city['总业绩']:,.0f}")

    with col2:
        max_growth_city = city_df.loc[city_df['增长率'].idxmax()]
        st.metric("增长率最高城市", max_growth_city['城市'], f"{max_growth_city['增长率']:.1f}%")

    with col3:
        positive_growth_cities = len(city_df[city_df['增长率'] > 0])
        st.metric("增长城市数量", f"{positive_growth_cities}/{len(city_df)}")

    with col4:
        st.metric("平均增长率", f"{avg_growth_rate:.1f}%")

    # 分析不同增长表现的城市
    st.write("### 📈 城市增长表现分析")

    high_growth_cities = city_df[city_df['增长率'] > avg_growth_rate]
    low_growth_cities = city_df[city_df['增长率'] <= avg_growth_rate]

    col1, col2 = st.columns(2)

    with col1:
        st.write("**🚀 高于平均增长率的城市:**")
        if len(high_growth_cities) > 0:
            for _, row in high_growth_cities.iterrows():
                st.write(f"• **{row['城市']}**: {row['增长率']:.1f}% (总业绩: {row['总业绩']:,.0f})")
        else:
            st.write("暂无城市高于平均增长率")

    with col2:
        st.write("**📊 低于平均增长率的城市:**")
        st.write("其余城市")
        # if len(low_growth_cities) > 0:
        #     for _, row in low_growth_cities.iterrows():
        #         st.write(f"• **{row['城市']}**: {row['增长率']:.1f}% (总业绩: {row['总业绩']:,.0f})")
        # else:
        #     st.write("所有城市均高于平均增长率")
    


    # 城市业绩排名变化分析
    # st.subheader("🎯 城市业绩排名变化分析")

    # import plotly.graph_objects as go
    # import numpy as np

    # # 计算2024年和2025年的排名
    # city_ranking_2024 = df_2024.groupby('城市')['业绩金额'].sum().sort_values(ascending=False)
    # city_ranking_2025 = df_2025.groupby('城市')['业绩金额'].sum().sort_values(ascending=False)

    # # 创建排名数据
    # ranking_data = []
    # for city in city_df['城市']:
    #     # 获取2024年排名
    #     if city in city_ranking_2024.index:
    #         rank_2024 = list(city_ranking_2024.index).index(city) + 1
    #         performance_2024 = city_ranking_2024[city]
    #     else:
    #         rank_2024 = len(city_ranking_2024) + 1  # 新城市排在最后
    #         performance_2024 = 0
        
    #     # 获取2025年排名
    #     if city in city_ranking_2025.index:
    #         rank_2025 = list(city_ranking_2025.index).index(city) + 1
    #         performance_2025 = city_ranking_2025[city]
    #     else:
    #         rank_2025 = len(city_ranking_2025) + 1
    #         performance_2025 = 0
        
    #     # 获取总业绩
    #     total_performance = city_df[city_df['城市'] == city]['总业绩'].iloc[0]
        
    #     ranking_data.append({
    #         '城市': city,
    #         '2024年排名': rank_2024,
    #         '2025年排名': rank_2025,
    #         '2024年业绩': performance_2024,
    #         '2025年业绩': performance_2025,
    #         '总业绩': total_performance,
    #         '排名变化': rank_2024 - rank_2025  # 正数表示排名上升
    #     })

    # # 转换为DataFrame并按总业绩排序
    # ranking_df = pd.DataFrame(ranking_data)
    # ranking_df = ranking_df.sort_values('总业绩', ascending=True)  # 从下到上排序

    # # 定义等级分区
    # total_cities = len(ranking_df)
    # s_threshold = max(1, total_cities // 4)  # S级：前25%
    # a_threshold = max(2, total_cities // 2)  # A级：前50%
    # b_threshold = max(3, total_cities * 3 // 4)  # B级：前75%
    # # C级：剩余的城市

    # # 为每个城市分配等级
    # def get_city_grade(rank, total):
    #     if rank <= s_threshold:
    #         return 'S'
    #     elif rank <= a_threshold:
    #         return 'A'
    #     elif rank <= b_threshold:
    #         return 'B'
    #     else:
    #         return 'C'

    # # 计算基于总业绩的等级
    # ranking_df_sorted = ranking_df.sort_values('总业绩', ascending=False)
    # for i, (idx, row) in enumerate(ranking_df_sorted.iterrows()):
    #     grade = get_city_grade(i + 1, total_cities)
    #     ranking_df.loc[idx, '等级'] = grade

    # # 创建哑铃图
    # fig = go.Figure()

    # # 为每个城市添加连接线
    # for i, row in ranking_df.iterrows():
    #     fig.add_trace(go.Scatter(
    #         x=[row['2024年排名'], row['2025年排名']],
    #         y=[row['城市'], row['城市']],
    #         mode='lines',
    #         line=dict(color='rgba(128, 128, 128, 0.5)', width=2),
    #         showlegend=False,
    #         hoverinfo='skip'
    #     ))

    # # 添加2024年数据点
    # fig.add_trace(go.Scatter(
    #     x=ranking_df['2024年排名'],
    #     y=ranking_df['城市'],
    #     mode='markers',
    #     marker=dict(
    #         color='#3498db',
    #         size=12,
    #         symbol='circle',
    #         line=dict(width=2, color='white')
    #     ),
    #     name='2024年排名',
    #     text=ranking_df.apply(lambda row: f"{row['城市']}<br>2024年排名: {row['2024年排名']}<br>业绩: {row['2024年业绩']:,.0f}", axis=1),
    #     hovertemplate='%{text}<extra></extra>'
    # ))

    # # 添加2025年数据点
    # fig.add_trace(go.Scatter(
    #     x=ranking_df['2025年排名'],
    #     y=ranking_df['城市'],
    #     mode='markers',
    #     marker=dict(
    #         color='#e74c3c',
    #         size=12,
    #         symbol='circle',
    #         line=dict(width=2, color='white')
    #     ),
    #     name='2025年排名',
    #     text=ranking_df.apply(lambda row: f"{row['城市']}<br>2025年排名: {row['2025年排名']}<br>业绩: {row['2025年业绩']:,.0f}", axis=1),
    #     hovertemplate='%{text}<extra></extra>'
    # ))

    # # 添加等级分区线
    # max_rank = max(ranking_df['2024年排名'].max(), ranking_df['2025年排名'].max())

    # # S/A分界线
    # fig.add_vline(x=s_threshold + 0.5, line_dash="dash", line_color="gold", line_width=2, 
    #             annotation_text="S级", annotation_position="top")

    # # A/B分界线
    # fig.add_vline(x=a_threshold + 0.5, line_dash="dash", line_color="silver", line_width=2,
    #             annotation_text="A级", annotation_position="top")

    # # B/C分界线
    # fig.add_vline(x=b_threshold + 0.5, line_dash="dash", line_color="#cd7f32", line_width=2,
    #             annotation_text="B级", annotation_position="top")

    # # 更新布局
    # fig.update_layout(
    #     title='城市业绩排名变化分析（哑铃图）',
    #     title_font=dict(color='white', size=16),
    #     xaxis_title='排名（数字越小排名越高）',
    #     yaxis_title='城市',
    #     xaxis=dict(
    #         title_font=dict(color='white'),
    #         tickfont=dict(color='white'),
    #         autorange='reversed',  # 反转x轴，使排名1在右侧
    #         showgrid=True,
    #         gridcolor='rgba(255,255,255,0.2)',
    #         dtick=1
    #     ),
    #     yaxis=dict(
    #         title_font=dict(color='white'),
    #         tickfont=dict(color='white'),
    #         showgrid=True,
    #         gridcolor='rgba(255,255,255,0.2)'
    #     ),
    #     height=max(400, len(ranking_df) * 30),  # 根据城市数量调整高度
    #     showlegend=True,
    #     legend=dict(
    #         orientation="h",
    #         yanchor="bottom",
    #         y=1.02,
    #         xanchor="right",
    #         x=1,
    #         font=dict(color='white')
    #     ),
    #     font=dict(size=12, color='white'),
    #     plot_bgcolor='rgba(0,0,0,0)',
    #     paper_bgcolor='rgba(0,0,0,0)'
    # )

    # st.plotly_chart(fig, use_container_width=True)

    # # 分析城市等级变化
    # st.write("### 🏆 城市等级分析")

    # # 显示等级分布
    # col1, col2, col3, col4 = st.columns(4)

    # grade_counts = ranking_df['等级'].value_counts()
    # with col1:
    #     st.metric("S级城市", grade_counts.get('S', 0), help="业绩排名前25%")
    # with col2:
    #     st.metric("A级城市", grade_counts.get('A', 0), help="业绩排名前50%")
    # with col3:
    #     st.metric("B级城市", grade_counts.get('B', 0), help="业绩排名前75%")
    # with col4:
    #     st.metric("C级城市", grade_counts.get('C', 0), help="业绩排名后25%")

    # # 分析排名变化最大的城市
    # st.write("### 📈 排名变化分析")

    # # 排名上升最多的城市
    # top_risers = ranking_df.nlargest(3, '排名变化')
    # # 排名下降最多的城市
    # top_fallers = ranking_df.nsmallest(3, '排名变化')

    # col1, col2 = st.columns(2)

    # with col1:
    #     st.write("**🚀 排名上升最多的城市:**")
    #     for _, row in top_risers.iterrows():
    #         if row['排名变化'] > 0:
    #             st.write(f"• **{row['城市']}** ({row['等级']}级): 上升 {row['排名变化']} 位")
    #             st.write(f"  📊 {row['2024年排名']}名 → {row['2025年排名']}名")
    #         else:
    #             st.write("暂无排名上升的城市")

    # with col2:
    #     st.write("**📉 排名下降最多的城市:**")
    #     for _, row in top_fallers.iterrows():
    #         if row['排名变化'] < 0:
    #             st.write(f"• **{row['城市']}** ({row['等级']}级): 下降 {abs(row['排名变化'])} 位")
    #             st.write(f"  📊 {row['2024年排名']}名 → {row['2025年排名']}名")
    #         else:
    #             st.write("暂无排名下降的城市")

    
    # # 关键洞察总结
    # st.write("### 💡 关键洞察")

    # # 计算一些关键指标
    # stable_cities = len(ranking_df[ranking_df['排名变化'] == 0])
    # rising_cities = len(ranking_df[ranking_df['排名变化'] > 0])
    # falling_cities = len(ranking_df[ranking_df['排名变化'] < 0])

    # avg_rank_change = ranking_df['排名变化'].mean()

    # st.write(f"""
    # - **排名稳定城市**: {stable_cities} 个城市排名保持不变
    # - **排名上升城市**: {rising_cities} 个城市排名上升
    # - **排名下降城市**: {falling_cities} 个城市排名下降
    # - **平均排名变化**: {avg_rank_change:.1f} 位
    # """)

    # if len(top_risers) > 0 and top_risers.iloc[0]['排名变化'] > 0:
    #     best_performer = top_risers.iloc[0]
    #     st.success(f"🏆 **最佳进步奖**: {best_performer['城市']} 排名上升 {best_performer['排名变化']} 位，"
    #             f"从第{best_performer['2024年排名']}名跃升至第{best_performer['2025年排名']}名！")

    # if len(top_fallers) > 0 and top_fallers.iloc[0]['排名变化'] < 0:
    #     needs_attention = top_fallers.iloc[0]
    #     st.warning(f"⚠️ **需要关注**: {needs_attention['城市']} 排名下降 {abs(needs_attention['排名变化'])} 位，"
    #             f"从第{needs_attention['2024年排名']}名降至第{needs_attention['2025年排名']}名，需要重点关注。")
    



    

        # 分析城市等级变化
        # 城市业绩排名变化分析
    # st.subheader("🎯 重点城市业绩排名变化分析")

    # import plotly.graph_objects as go
    # import numpy as np

    # # 定义重点城市列表
    # key_cities = ['广州', '北京', '成都', '上海', '杭州', '重庆', '深圳', '珠海', '天津', '苏州']

    # # 计算2024年和2025年的排名（基于所有城市）
    # city_ranking_2024 = df_2024.groupby('城市')['业绩金额'].sum().sort_values(ascending=False)
    # city_ranking_2025 = df_2025.groupby('城市')['业绩金额'].sum().sort_values(ascending=False)

    # # 创建排名数据
    # ranking_data = []
    # missing_cities = []  # 记录没有业绩的城市

    # for city in key_cities:
    #     # 获取2024年排名
    #     if city in city_ranking_2024.index:
    #         rank_2024 = list(city_ranking_2024.index).index(city) + 1
    #         performance_2024 = city_ranking_2024[city]
    #     else:
    #         rank_2024 = None
    #         performance_2024 = 0
        
    #     # 获取2025年排名
    #     if city in city_ranking_2025.index:
    #         rank_2025 = list(city_ranking_2025.index).index(city) + 1
    #         performance_2025 = city_ranking_2025[city]
    #     else:
    #         rank_2025 = None
    #         performance_2025 = 0
        
    #     # 如果该城市在任一年有业绩，则计算总业绩
    #     if rank_2024 is not None or rank_2025 is not None:
    #         total_performance = performance_2024 + performance_2025
            
    #         # 计算排名变化
    #         if rank_2024 is not None and rank_2025 is not None:
    #             rank_change = rank_2024 - rank_2025  # 正数表示排名上升
    #         else:
    #             rank_change = None
            
    #         ranking_data.append({
    #             '城市': city,
    #             '2024年排名': rank_2024,
    #             '2025年排名': rank_2025,
    #             '2024年业绩': performance_2024,
    #             '2025年业绩': performance_2025,
    #             '总业绩': total_performance,
    #             '排名变化': rank_change
    #         })
    #     else:
    #         # 记录没有业绩的城市
    #         missing_cities.append(city)

    # # 转换为DataFrame并按总业绩排序
    # ranking_df = pd.DataFrame(ranking_data)
    # ranking_df = ranking_df.sort_values('总业绩', ascending=True)  # 从下到上排序

    # # 定义等级分区（基于所有城市的总数）
    # total_cities = len(df_all['城市'].unique())
    # s_threshold = max(1, total_cities // 4)  # S级：前25%
    # a_threshold = max(2, total_cities // 2)  # A级：前50%
    # b_threshold = max(3, total_cities * 3 // 4)  # B级：前75%

    # # 为每个城市分配等级
    # def get_city_grade(rank, total):
    #     if rank is None:
    #         return 'N/A'
    #     elif rank <= s_threshold:
    #         return 'S'
    #     elif rank <= a_threshold:
    #         return 'A'
    #     elif rank <= b_threshold:
    #         return 'B'
    #     else:
    #         return 'C'

    # # 计算基于当前排名的等级
    # for i, row in ranking_df.iterrows():
    #     # 使用2025年排名来确定等级，如果没有2025年数据则使用2024年
    #     current_rank = row['2025年排名'] if row['2025年排名'] is not None else row['2024年排名']
    #     grade = get_city_grade(current_rank, total_cities)
    #     ranking_df.loc[i, '等级'] = grade

    # # 只显示有业绩数据的城市的哑铃图
    # if len(ranking_df) > 0:
    #     # 创建哑铃图
    #     fig = go.Figure()

    #     # 为每个城市添加连接线和数据点
    #     for i, row in ranking_df.iterrows():
    #         city_name = row['城市']
            
    #         # 检查是否有重叠（排名相同）
    #         rank_2024 = row['2024年排名']
    #         rank_2025 = row['2025年排名']
    #         is_overlap = (rank_2024 is not None and rank_2025 is not None and rank_2024 == rank_2025)
            
    #         if rank_2024 is not None and rank_2025 is not None:
    #             # 添加连接线
    #             fig.add_trace(go.Scatter(
    #                 x=[rank_2024, rank_2025],
    #                 y=[city_name, city_name],
    #                 mode='lines',
    #                 line=dict(
    #                     color='rgba(128, 128, 128, 0.5)' if not is_overlap else 'rgba(255, 215, 0, 0.8)',
    #                     width=3 if is_overlap else 2
    #                 ),
    #                 showlegend=False,
    #                 hoverinfo='skip'
    #             ))
                
    #             if is_overlap:
    #                 # 处理重叠情况：创建一个特殊的重叠标记
    #                 fig.add_trace(go.Scatter(
    #                     x=[rank_2024],
    #                     y=[city_name],
    #                     mode='markers',
    #                     marker=dict(
    #                         color='rgba(255, 215, 0, 0.3)',  # 半透明金色背景
    #                         size=24,
    #                         symbol='circle',
    #                         line=dict(width=3, color='gold')
    #                     ),
    #                     name='排名未变' if i == 0 else '',  # 只在第一个重叠点显示图例
    #                     showlegend=True if i == 0 and is_overlap else False,
    #                     text=f"{city_name}<br>排名未变: {rank_2024}<br>2024年业绩: {row['2024年业绩']:,.0f}<br>2025年业绩: {row['2025年业绩']:,.0f}",
    #                     hovertemplate='%{text}<extra></extra>'
    #                 ))
                    
    #                 # 在重叠点上添加双色标记
    #                 fig.add_trace(go.Scatter(
    #                     x=[rank_2024 - 0.1],
    #                     y=[city_name],
    #                     mode='markers',
    #                     marker=dict(
    #                         color='#3498db',
    #                         size=12,
    #                         symbol='circle',
    #                         line=dict(width=1, color='white')
    #                     ),
    #                     showlegend=False,
    #                     hoverinfo='skip'
    #                 ))
                    
    #                 fig.add_trace(go.Scatter(
    #                     x=[rank_2024 + 0.1],
    #                     y=[city_name],
    #                     mode='markers',
    #                     marker=dict(
    #                         color='#e74c3c',
    #                         size=12,
    #                         symbol='circle',
    #                         line=dict(width=1, color='white')
    #                     ),
    #                     showlegend=False,
    #                     hoverinfo='skip'
    #                 ))
    #             else:
    #                 # 添加2024年数据点
    #                 fig.add_trace(go.Scatter(
    #                     x=[rank_2024],
    #                     y=[city_name],
    #                     mode='markers',
    #                     marker=dict(
    #                         color='#3498db',
    #                         size=14,
    #                         symbol='circle',
    #                         line=dict(width=2, color='white')
    #                     ),
    #                     name='2024年排名' if i == 0 else '',
    #                     showlegend=True if i == 0 and not is_overlap else False,
    #                     text=f"{city_name}<br>2024年排名: {rank_2024}<br>业绩: {row['2024年业绩']:,.0f}",
    #                     hovertemplate='%{text}<extra></extra>'
    #                 ))
                    
    #                 # 添加2025年数据点
    #                 fig.add_trace(go.Scatter(
    #                     x=[rank_2025],
    #                     y=[city_name],
    #                     mode='markers',
    #                     marker=dict(
    #                         color='#e74c3c',
    #                         size=14,
    #                         symbol='circle',
    #                         line=dict(width=2, color='white')
    #                     ),
    #                     name='2025年排名' if i == 0 else '',
    #                     showlegend=True if i == 0 and not is_overlap else False,
    #                     text=f"{city_name}<br>2025年排名: {rank_2025}<br>业绩: {row['2025年业绩']:,.0f}",
    #                     hovertemplate='%{text}<extra></extra>'
    #                 ))
    #         else:
    #             # 处理只有一年数据的情况
    #             if rank_2024 is not None:
    #                 fig.add_trace(go.Scatter(
    #                     x=[rank_2024],
    #                     y=[city_name],
    #                     mode='markers',
    #                     marker=dict(
    #                         color='#3498db',
    #                         size=14,
    #                         symbol='circle',
    #                         line=dict(width=2, color='white')
    #                     ),
    #                     name='2024年排名' if i == 0 else '',
    #                     showlegend=True if i == 0 else False,
    #                     text=f"{city_name}<br>2024年排名: {rank_2024}<br>业绩: {row['2024年业绩']:,.0f}",
    #                     hovertemplate='%{text}<extra></extra>'
    #                 ))
                
    #             if rank_2025 is not None:
    #                 fig.add_trace(go.Scatter(
    #                     x=[rank_2025],
    #                     y=[city_name],
    #                     mode='markers',
    #                     marker=dict(
    #                         color='#e74c3c',
    #                         size=14,
    #                         symbol='circle',
    #                         line=dict(width=2, color='white')
    #                     ),
    #                     name='2025年排名' if i == 0 else '',
    #                     showlegend=True if i == 0 else False,
    #                     text=f"{city_name}<br>2025年排名: {rank_2025}<br>业绩: {row['2025年业绩']:,.0f}",
    #                     hovertemplate='%{text}<extra></extra>'
    #                 ))

    #     # 添加等级分区线
    #     max_rank = max(
    #         ranking_df['2024年排名'].max() if ranking_df['2024年排名'].notna().any() else 0,
    #         ranking_df['2025年排名'].max() if ranking_df['2025年排名'].notna().any() else 0
    #     )

    #     # S/A分界线
    #     fig.add_vline(x=s_threshold + 0.5, line_dash="dash", line_color="gold", line_width=2, 
    #                 annotation_text="S级", annotation_position="top")

    #     # A/B分界线
    #     fig.add_vline(x=a_threshold + 0.5, line_dash="dash", line_color="silver", line_width=2,
    #                 annotation_text="A级", annotation_position="top")

    #     # B/C分界线
    #     fig.add_vline(x=b_threshold + 0.5, line_dash="dash", line_color="#cd7f32", line_width=2,
    #                 annotation_text="B级", annotation_position="top")

    #     # 更新布局
    #     fig.update_layout(
    #         title='重点城市业绩排名变化分析（哑铃图）',
    #         title_font=dict(color='white', size=16),
    #         xaxis_title='排名（数字越小排名越高）',
    #         yaxis_title='城市',
    #         xaxis=dict(
    #             title_font=dict(color='white'),
    #             tickfont=dict(color='white'),
    #             autorange='reversed',  # 反转x轴，使排名1在右侧
    #             showgrid=True,
    #             gridcolor='rgba(255,255,255,0.2)',
    #             dtick=1
    #         ),
    #         yaxis=dict(
    #             title_font=dict(color='white'),
    #             tickfont=dict(color='white'),
    #             showgrid=True,
    #             gridcolor='rgba(255,255,255,0.2)'
    #         ),
    #         height=max(400, len(ranking_df) * 40),  # 根据城市数量调整高度
    #         showlegend=True,
    #         legend=dict(
    #             orientation="h",
    #             yanchor="bottom",
    #             y=1.02,
    #             xanchor="right",
    #             x=1,
    #             font=dict(color='white')
    #         ),
    #         font=dict(size=12, color='white'),
    #         plot_bgcolor='rgba(0,0,0,0)',
    #         paper_bgcolor='rgba(0,0,0,0)'
    #     )

    #     st.plotly_chart(fig, use_container_width=True)
    
        
        
        

    # # 显示没有业绩的城市
    # if missing_cities:
    #     st.warning(f"以下城市在两年内均无业绩数据：{', '.join(missing_cities)}")
    #     st.write("### 🏆 重点城市等级分析")

    #     # 显示等级分布
    #     col1, col2, col3, col4 = st.columns(4)

    #     grade_counts = ranking_df['等级'].value_counts()
    #     with col1:
    #         st.metric("S级城市", grade_counts.get('S', 0), help=f"业绩排名前{s_threshold}名")
    #     with col2:
    #         st.metric("A级城市", grade_counts.get('A', 0), help=f"业绩排名前{a_threshold}名")
    #     with col3:
    #         st.metric("B级城市", grade_counts.get('B', 0), help=f"业绩排名前{b_threshold}名")
    #     with col4:
    #         st.metric("C级城市", grade_counts.get('C', 0), help=f"业绩排名{b_threshold}名之后")

    #     # 分析排名变化
    #     st.write("### 📈 排名变化分析")

    #     # 有排名变化数据的城市
    #     cities_with_change = ranking_df[ranking_df['排名变化'].notna()]
        
    #     if len(cities_with_change) > 0:
    #         # 排名上升的城市
    #         rising_cities = cities_with_change[cities_with_change['排名变化'] > 0].sort_values('排名变化', ascending=False)
    #         # 排名下降的城市
    #         falling_cities = cities_with_change[cities_with_change['排名变化'] < 0].sort_values('排名变化', ascending=True)
    #         # 排名不变的城市
    #         stable_cities = cities_with_change[cities_with_change['排名变化'] == 0]

    #         col1, col2 = st.columns(2)

    #         with col1:
    #             st.write("**🚀 排名上升的城市:**")
    #             if len(rising_cities) > 0:
    #                 for _, row in rising_cities.iterrows():
    #                     st.write(f"• **{row['城市']}** ({row['等级']}级): 上升 {row['排名变化']} 位")
    #                     st.write(f"  📊 第{row['2024年排名']}名 → 第{row['2025年排名']}名")
    #             else:
    #                 st.write("暂无排名上升的城市")

    #         with col2:
    #             st.write("**📉 排名下降的城市:**")
    #             if len(falling_cities) > 0:
    #                 for _, row in falling_cities.iterrows():
    #                     st.write(f"• **{row['城市']}** ({row['等级']}级): 下降 {abs(row['排名变化'])} 位")
    #                     st.write(f"  📊 第{row['2024年排名']}名 → 第{row['2025年排名']}名")
    #             else:
    #                 st.write("暂无排名下降的城市")

    #         if len(stable_cities) > 0:
    #             st.write("**➡️ 排名稳定的城市:**")
    #             for _, row in stable_cities.iterrows():
    #                 st.write(f"• **{row['城市']}** ({row['等级']}级): 排名保持第{row['2024年排名']}名")

    #     # 只有单年数据的城市
    #     single_year_cities = ranking_df[ranking_df['排名变化'].isna()]
    #     if len(single_year_cities) > 0:
    #         st.write("**📊 单年数据城市:**")
    #         for _, row in single_year_cities.iterrows():
    #             if row['2024年排名'] is not None and row['2025年排名'] is None:
    #                 st.write(f"• **{row['城市']}**: 仅2024年有业绩，排名第{row['2024年排名']}名")
    #             elif row['2024年排名'] is None and row['2025年排名'] is not None:
    #                 st.write(f"• **{row['城市']}**: 仅2025年有业绩，排名第{row['2025年排名']}名")

    # else:
    #     st.write("### ⚠️ 暂无重点城市业绩数据")

    # # 显示没有业绩的城市
    # if len(missing_cities) > 0:
    #     st.write("### 📝 无业绩记录的重点城市")
    #     st.info(f"以下重点城市在2024年和2025年均无业绩记录：**{', '.join(missing_cities)}**")
    


    # 重点城市一级业态结构变化分析
    # 重点城市一级业态结构变化分析
    # st.subheader("重点城市一级业态结构变化")

    # # 重点城市列表（与上面保持一致）
    # key_cities = ['广州', '北京', '成都', '上海', '杭州', '重庆', '深圳', '珠海', '天津', '苏州']

    # # 筛选重点城市且有业绩数据的记录
    # df_key_cities = df_all[
    #     (df_all['城市'].isin(key_cities)) & 
    #     (df_all['业绩金额'] > 0)
    # ].copy()

    # # 提取年份信息（假设从df_2024和df_2025可以区分年份）
    # df_key_cities['年份'] = df_key_cities.apply(lambda x: 2024 if x.name < len(df_2024) else 2025, axis=1)

    # # 筛选有2024年业绩数据的城市
    # cities_with_2024 = df_key_cities[df_key_cities['年份'] == 2024]['城市'].unique()

    # if len(cities_with_2024) > 0:
    #     st.write(f"**有2024年业绩数据的重点城市:** {', '.join(cities_with_2024)}")
        
    #     # 按城市、年份、一级业态分组，计算业绩金额总和
    #     city_year_business = df_key_cities.groupby(['城市', '年份', '一级业态'])['业绩金额'].sum().reset_index()
        
    #     # 获取所有出现的业态类型
    #     all_business_types = city_year_business['一级业态'].unique()
        
    #     # 定义商业业态（放在底部，使用鲜艳颜色）
    #     commercial_types = ['产业园物业', '写字楼物业', '商业物业']
        
    #     # 重新排序业态，商业业态在前
    #     business_types_ordered = []
    #     other_types = []
        
    #     for business_type in all_business_types:
    #         if business_type in commercial_types:
    #             business_types_ordered.append(business_type)
    #         else:
    #             other_types.append(business_type)
        
    #     # 按照指定顺序排列商业业态
    #     commercial_ordered = [bt for bt in commercial_types if bt in business_types_ordered]
    #     business_types_ordered = commercial_ordered + other_types
        
    #     # 创建堆叠柱状图
    #     fig = go.Figure()
        
    #     # 定义颜色方案
    #     # 商业业态使用鲜艳颜色
    #     commercial_colors = {
    #         '产业园物业': '#E74C3C',    # 鲜艳红色
    #         '写字楼物业': '#3498DB',    # 鲜艳蓝色
    #         '商业物业': '#2ECC71'       # 鲜艳绿色
    #     }
        
    #     # 其他业态使用淡色但能明显区分
    #     other_colors = [
    #         '#BDC3C7',  # 淡灰色
    #         '#F39C12',  # 淡橙色
    #         '#9B59B6',  # 淡紫色
    #         "#383AA7",  # 淡青色
    #         "#F7D9E0",  # 淡橘色
    #         '#FAD5A5'
            
            
    #     ]
        
    #     # 为每个业态创建堆叠柱
    #     other_color_index = 0
    #     for business_type in business_types_ordered:
    #         # 选择颜色
    #         if business_type in commercial_colors:
    #             color = commercial_colors[business_type]
    #         else:
    #             color = other_colors[other_color_index % len(other_colors)]
    #             other_color_index += 1
            
    #         # 2024年数据
    #         data_2024 = []
    #         # 2025年数据
    #         data_2025 = []
            
    #         for city in cities_with_2024:
    #             # 获取该城市该业态的2024年数据
    #             city_business_2024 = city_year_business[
    #                 (city_year_business['城市'] == city) & 
    #                 (city_year_business['年份'] == 2024) & 
    #                 (city_year_business['一级业态'] == business_type)
    #             ]
    #             value_2024 = city_business_2024['业绩金额'].sum() if len(city_business_2024) > 0 else 0
    #             data_2024.append(value_2024)
                
    #             # 获取该城市该业态的2025年数据
    #             city_business_2025 = city_year_business[
    #                 (city_year_business['城市'] == city) & 
    #                 (city_year_business['年份'] == 2025) & 
    #                 (city_year_business['一级业态'] == business_type)
    #             ]
    #             value_2025 = city_business_2025['业绩金额'].sum() if len(city_business_2025) > 0 else 0
    #             data_2025.append(value_2025)
            
    #         # 创建x轴标签（城市-年份组合）
    #         x_labels_2024 = [f"{city}-2024" for city in cities_with_2024]
    #         x_labels_2025 = [f"{city}-2025" for city in cities_with_2024]
            
    #         # 添加2024年的堆叠柱
    #         fig.add_trace(go.Bar(
    #             name=business_type,
    #             x=x_labels_2024,
    #             y=data_2024,
    #             marker_color=color,
    #             legendgroup=business_type,
    #             hovertemplate=f'<b>{business_type}</b><br>' +
    #                         '城市: %{x}<br>' +
    #                         '业绩金额: %{y:,.0f}<br>' +
    #                         '<extra></extra>'
    #         ))
            
    #         # 添加2025年的堆叠柱（不使用透明度）
    #         fig.add_trace(go.Bar(
    #             name=business_type,
    #             x=x_labels_2025,
    #             y=data_2025,
    #             marker_color=color,
    #             legendgroup=business_type,
    #             showlegend=False,
    #             hovertemplate=f'<b>{business_type}</b><br>' +
    #                         '城市: %{x}<br>' +
    #                         '业绩金额: %{y:,.0f}<br>' +
    #                         '<extra></extra>'
    #         ))
        
    #     # 创建完整的x轴标签列表
    #     all_x_labels = []
    #     for city in cities_with_2024:
    #         all_x_labels.extend([f"{city}-2024", f"{city}-2025"])
        
    #     # 更新布局
    #     fig.update_layout(
    #     title={
    #         'text': '重点城市一级业态结构对比分析',
    #         'x': 0.5,
    #         'xanchor': 'center',
    #         'font': {'size': 20, 'color': '#1B4965'}  # 深色标题
    #     },
    #     xaxis={
    #         'title': {
    #             'text': '城市-年份',
    #             'font': {'size': 14, 'color': '#1B4965'}  # 深色x轴标题
    #         },
    #         'tickangle': -45,
    #         'tickfont': {'size': 12, 'color': '#1B4965'},  # 深色字体
    #         'categoryorder': 'array',
    #         'categoryarray': all_x_labels,
    #         'gridcolor': '#F6F8FA',  # 浅白色网格线
    #         'zerolinecolor': '#F6F8FA',  # 零轴线颜色与网格线一致
    #         'showgrid': False  # 隐藏x轴网格线
    #     },
    #     yaxis={
    #         'title': {
    #             'text': '业绩金额',
    #             'font': {'size': 14, 'color': '#1B4965'}  # 深色字体
    #         },
    #         'tickformat': ',.0f',
    #         'tickfont': {'size': 12, 'color': '#1B4965'},  # 深色字体
    #         'gridcolor': '#F6F8FA',  # 浅白色网格线
    #         'zerolinecolor': '#F6F8FA'  # 零轴线颜色与网格线一致
    #     },
    #     barmode='stack',
    #     height=600,
    #     legend={
    #         'orientation': 'h',
    #         'yanchor': 'bottom',
    #         'y': 1.02,
    #         'xanchor': 'right',
    #         'x': 1,
    #         'font': {'size': 12, 'color': '#1B4965'}  # 深色图例文字
    #     },
    #     font=dict(size=12, color='#1B4965'),  # 深色字体
    #     plot_bgcolor='#E3EAF3',  # 与PPT背景协调的浅色背景
    #     paper_bgcolor='#E3EAF3',  # 与PPT背景完全一致
    #     margin=dict(l=50, r=50, t=80, b=100),
    #     # 调整柱子间距，增加城市组之间的间隙
    #     bargap=0.6,  # 增加柱子组之间的间隙
    #     bargroupgap=0.04  # 保持同组内柱子的紧密间距
    # )
    
        
    #     # 添加网格线
    #     fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
    #     fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
        
    #     # 添加城市分组的分割线（调整位置以适应新的间距）
    #     for i in range(1, len(cities_with_2024)):
    #         fig.add_vline(
    #             x=i * 2 - 0.5,
    #             line_dash="dash",
    #             line_color="rgba(128,128,128,0.4)",
    #             line_width=1
    #         )
        
    #     st.plotly_chart(fig, use_container_width=True)
        
    #     # 添加数据摘要表格
    #     st.write("#### 📊 数据摘要")
        
    #     # 计算各城市总业绩和主要业态
    #     summary_data = []
    #     for city in cities_with_2024:
    #         # 2024年数据
    #         city_2024 = city_year_business[
    #             (city_year_business['城市'] == city) & 
    #             (city_year_business['年份'] == 2024)
    #         ]
    #         total_2024 = city_2024['业绩金额'].sum()
    #         main_business_2024 = city_2024.loc[city_2024['业绩金额'].idxmax(), '一级业态'] if len(city_2024) > 0 else "无"
            
    #         # 2025年数据
    #         city_2025 = city_year_business[
    #             (city_year_business['城市'] == city) & 
    #             (city_year_business['年份'] == 2025)
    #         ]
    #         total_2025 = city_2025['业绩金额'].sum()
    #         main_business_2025 = city_2025.loc[city_2025['业绩金额'].idxmax(), '一级业态'] if len(city_2025) > 0 else "无"
            
    #         # 计算增长率
    #         growth_rate = ((total_2025 - total_2024) / total_2024 * 100) if total_2024 > 0 else 0
            
    #         summary_data.append({
    #             '城市': city,
    #             '2024年总业绩': f"{total_2024:,.0f}",
    #             '2024年主要业态': main_business_2024,
    #             '2025年总业绩': f"{total_2025:,.0f}",
    #             '2025年主要业态': main_business_2025,
    #             '增长率': f"{growth_rate:+.1f}%"
    #         })
        
    #     summary_df = pd.DataFrame(summary_data)
    #     st.dataframe(summary_df, use_container_width=True, hide_index=True)
        
    #     # 添加关键洞察
    #     st.write("#### 💡 关键洞察")
        
    #     col1, col2 = st.columns(2)
        
    #     with col1:
    #         st.write("**🏆 业绩增长最快的城市:**")
    #         growth_analysis = []
    #         for city in cities_with_2024:
    #             city_2024_total = city_year_business[
    #                 (city_year_business['城市'] == city) & 
    #                 (city_year_business['年份'] == 2024)
    #             ]['业绩金额'].sum()
                
    #             city_2025_total = city_year_business[
    #                 (city_year_business['城市'] == city) & 
    #                 (city_year_business['年份'] == 2025)
    #             ]['业绩金额'].sum()
                
    #             if city_2024_total > 0:
    #                 growth = city_2025_total - city_2024_total
    #                 growth_analysis.append((city, growth))
            
    #         if growth_analysis:
    #             top_growth_city = max(growth_analysis, key=lambda x: x[1])
    #             st.write(f"- **{top_growth_city[0]}**: 增长 {top_growth_city[1]:,.0f}")
        
    #     with col2:
    #         st.write("**📈 主要业态分布:**")
    #         business_count = city_year_business['一级业态'].value_counts()
    #         for business, count in business_count.head(3).items():
    #             st.write(f"- **{business}**: {count} 个城市年份")

    # else:
    #     st.write("重点城市均无2024年业绩数据，无法进行业态结构对比分析")





    # 定义重点城市列表
    key_cities = ['广州', '北京', '成都', '上海', '杭州', '重庆', '深圳', '珠海', '天津', '苏州']

    # 分别获取2024年和2025年的数据
    df_2024_city = df_2024.groupby('城市')['业绩金额'].sum().reset_index()
    df_2025_city = df_2025.groupby('城市')['业绩金额'].sum().reset_index()

    # 计算2024年各城市业绩
    cities_2024 = set(df_2024_city['城市'].tolist())
    cities_2025 = set(df_2025_city['城市'].tolist())

    # 2024年重点城市业绩
    key_cities_2024 = [city for city in key_cities if city in cities_2024]
    key_cities_2024_amount = df_2024_city[df_2024_city['城市'].isin(key_cities_2024)]['业绩金额'].sum()
    other_cities_2024_amount = df_2024_city[~df_2024_city['城市'].isin(key_cities_2024)]['业绩金额'].sum()
    total_2024 = key_cities_2024_amount + other_cities_2024_amount

    # 2025年重点城市业绩
    key_cities_2025 = [city for city in key_cities if city in cities_2025]
    # 24年已有业绩的重点城市在25年的业绩
    existing_key_cities_2025 = [city for city in key_cities_2024 if city in cities_2025]
    existing_key_cities_2025_amount = df_2025_city[df_2025_city['城市'].isin(existing_key_cities_2025)]['业绩金额'].sum()
    # 新增重点城市在25年的业绩
    new_key_cities_2025 = [city for city in key_cities_2025 if city not in key_cities_2024]
    new_key_cities_2025_amount = df_2025_city[df_2025_city['城市'].isin(new_key_cities_2025)]['业绩金额'].sum()
    # 其他城市在25年的业绩
    other_cities_2025_amount = df_2025_city[~df_2025_city['城市'].isin(key_cities_2025)]['业绩金额'].sum()
    total_2025 = existing_key_cities_2025_amount + new_key_cities_2025_amount + other_cities_2025_amount

    # 找出24、25年都没有业绩的重点城市
    no_performance_cities = [city for city in key_cities if city not in cities_2024 and city not in cities_2025]

    # 创建子图
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('2024年上半年重点城市业绩占比图', '2025年上半年重点城市业绩占比图'),
        specs=[[{"type": "pie"}, {"type": "pie"}]]
    )

    # 2024年饼图
    fig.add_trace(
        go.Pie(
            labels=[f'重点城市<br>({", ".join(key_cities_2024)})', '其他城市'],
            values=[key_cities_2024_amount, other_cities_2024_amount],
            name="2024年",
            marker=dict(colors=['#e47158', '#3d5c6f']),
            textinfo='label+percent',
            textposition='inside',
            textfont=dict(color="black", size=15),
            hovertemplate='<b>%{label}</b><br>金额: %{value}<br>占比: %{percent}<extra></extra>'
        ),
        row=1, col=1
    )

    # 2025年饼图
    labels_2025 = []
    values_2025 = []
    colors_2025 = []

    if existing_key_cities_2025_amount > 0:
        labels_2025.append(f'重点城市<br>({", ".join(existing_key_cities_2025)})')
        values_2025.append(existing_key_cities_2025_amount)
        colors_2025.append('#e47158')

    if new_key_cities_2025_amount > 0:
        labels_2025.append(f'新增重点城市<br>({", ".join(new_key_cities_2025)})')
        values_2025.append(new_key_cities_2025_amount)
        colors_2025.append('#f9ae79')

    if other_cities_2025_amount > 0:
        labels_2025.append('其他城市')
        values_2025.append(other_cities_2025_amount)
        colors_2025.append('#3d5c6f')

    fig.add_trace(
        go.Pie(
            labels=labels_2025,
            values=values_2025,
            name="2025年",
            marker=dict(colors=colors_2025),
            textinfo='label+percent',
            textposition='inside',
            textfont=dict(color='black', size=15),
            hovertemplate='<b>%{label}</b><br>金额: %{value}<br>占比: %{percent}<extra></extra>'
        ),
        row=1, col=2
    )

    # 更新布局
    fig.update_layout(
        title_text="重点城市业绩金额占比变化对比",
        title_x=0.4,
        title_font=dict(color='#1B4965', size=16),
        showlegend=False,
        height=600,
        width=1200,
        font=dict(color='#1B4965', size=12),
        plot_bgcolor='#E3EAF3',
        paper_bgcolor='#E3EAF3'
    )

    # 显示图表
    st.plotly_chart(fig, use_container_width=True)

    # 输出没有业绩的重点城市
    if no_performance_cities:
        st.write(f"**注意：** 以下重点城市在2024年和2025年上半年都没有业绩记录：{', '.join(no_performance_cities)}")

    



    st.subheader("重点城市一级业态结构变化")

    # 重点城市列表（与上面保持一致）
    key_cities = ['广州', '北京', '成都', '上海', '杭州', '重庆', '深圳', '珠海', '天津', '苏州']

    # 筛选重点城市且有业绩数据的记录
    df_key_cities = df_all[
        (df_all['城市'].isin(key_cities)) & 
        (df_all['业绩金额'] > 0)
    ].copy()

    # 提取年份信息（假设从df_2024和df_2025可以区分年份）
    df_key_cities['年份'] = df_key_cities.apply(lambda x: 2024 if x.name < len(df_2024) else 2025, axis=1)

    # 筛选有2024年业绩数据的城市
    cities_with_2024 = df_key_cities[df_key_cities['年份'] == 2024]['城市'].unique()

    if len(cities_with_2024) > 0:
        st.write(f"**有2024年业绩数据的重点城市:** {', '.join(cities_with_2024)}")
        
        # 按城市、年份、一级业态分组，计算业绩金额总和
        city_year_business = df_key_cities.groupby(['城市', '年份', '一级业态'])['业绩金额'].sum().reset_index()
        
        # 获取所有出现的业态类型
        all_business_types = city_year_business['一级业态'].unique()
        
        # 定义商业业态（放在底部，使用鲜艳颜色）
        commercial_types = ['产业园物业', '写字楼物业', '商业物业']
        
        # 重新排序业态，商业业态在前
        business_types_ordered = []
        other_types = []
        
        for business_type in all_business_types:
            if business_type in commercial_types:
                business_types_ordered.append(business_type)
            else:
                other_types.append(business_type)
        
        # 按照指定顺序排列商业业态
        commercial_ordered = [bt for bt in commercial_types if bt in business_types_ordered]
        business_types_ordered = commercial_ordered + other_types
        
        # 定义与背景色协调的配色方案
        # 商业业态使用深色调，与浅蓝背景形成对比
        commercial_colors = {
            '产业园物业': '#8B2635',    # 深红色
            '写字楼物业': '#2E5984',    # 深蓝色
            '商业物业': '#1E7E34'       # 深绿色
        }
        
        # 其他业态使用中等饱和度的颜色，与背景协调且区分明显
        other_colors = [
            '#6C757D',  # 中灰色
            '#D4A843',  # 金黄色
            '#7B68A6',  # 深紫色
            '#A0522D',  # 深棕色
            '#CD853F',  # 秘鲁色
            '#5F9EA0'   # 青灰色
        ]
        
        # 创建绘图函数
        def create_business_chart(target_cities, chart_title, chart_height=600):
            # 创建堆叠柱状图
            fig = go.Figure()
            
            # 为每个业态创建堆叠柱
            other_color_index = 0
            for business_type in business_types_ordered:
                # 选择颜色
                if business_type in commercial_colors:
                    color = commercial_colors[business_type]
                else:
                    color = other_colors[other_color_index % len(other_colors)]
                    other_color_index += 1
                
                # 2024年数据
                data_2024 = []
                # 2025年数据
                data_2025 = []
                
                for city in target_cities:
                    # 获取该城市该业态的2024年数据
                    city_business_2024 = city_year_business[
                        (city_year_business['城市'] == city) & 
                        (city_year_business['年份'] == 2024) & 
                        (city_year_business['一级业态'] == business_type)
                    ]
                    value_2024 = city_business_2024['业绩金额'].sum() if len(city_business_2024) > 0 else 0
                    data_2024.append(value_2024)
                    
                    # 获取该城市该业态的2025年数据
                    city_business_2025 = city_year_business[
                        (city_year_business['城市'] == city) & 
                        (city_year_business['年份'] == 2025) & 
                        (city_year_business['一级业态'] == business_type)
                    ]
                    value_2025 = city_business_2025['业绩金额'].sum() if len(city_business_2025) > 0 else 0
                    data_2025.append(value_2025)
                
                # 创建x轴标签（城市-年份组合）
                x_labels_2024 = [f"{city}-2024" for city in target_cities]
                x_labels_2025 = [f"{city}-2025" for city in target_cities]
                
                # 添加2024年的堆叠柱
                fig.add_trace(go.Bar(
                    name=business_type,
                    x=x_labels_2024,
                    y=data_2024,
                    marker_color=color,
                    legendgroup=business_type,
                    hovertemplate=f'<b>{business_type}</b><br>' +
                                '城市: %{x}<br>' +
                                '业绩金额: %{y:,.0f}<br>' +
                                '<extra></extra>'
                ))
                
                # 添加2025年的堆叠柱
                fig.add_trace(go.Bar(
                    name=business_type,
                    x=x_labels_2025,
                    y=data_2025,
                    marker_color=color,
                    legendgroup=business_type,
                    showlegend=False,
                    hovertemplate=f'<b>{business_type}</b><br>' +
                                '城市: %{x}<br>' +
                                '业绩金额: %{y:,.0f}<br>' +
                                '<extra></extra>'
                ))
            
            # 创建完整的x轴标签列表
            all_x_labels = []
            for city in target_cities:
                all_x_labels.extend([f"{city}-2024", f"{city}-2025"])
            
            # 更新布局
            fig.update_layout(
                title={
                    'text': chart_title,
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 20, 'color': '#1B4965'}
                },
                xaxis={
                    'title': {
                        'text': '城市-年份',
                        'font': {'size': 14, 'color': '#1B4965'}
                    },
                    'tickangle': -45,
                    'tickfont': {'size': 12, 'color': '#1B4965'},
                    'categoryorder': 'array',
                    'categoryarray': all_x_labels,
                    'gridcolor': '#F6F8FA',
                    'zerolinecolor': '#F6F8FA',
                    'showgrid': False
                },
                yaxis={
                    'title': {
                        'text': '业绩金额',
                        'font': {'size': 14, 'color': '#1B4965'}
                    },
                    'tickformat': ',.0f',
                    'tickfont': {'size': 12, 'color': '#1B4965'},
                    'gridcolor': '#F6F8FA',
                    'zerolinecolor': '#F6F8FA'
                },
                barmode='stack',
                height=chart_height,
                legend={
                    'orientation': 'h',
                    'yanchor': 'bottom',
                    'y': 1.02,
                    'xanchor': 'right',
                    'x': 1,
                    'font': {'size': 12, 'color': '#1B4965'}
                },
                font=dict(size=12, color='#1B4965'),
                plot_bgcolor='#E3EAF3',
                paper_bgcolor='#E3EAF3',
                margin=dict(l=50, r=50, t=80, b=100),
                bargap=0.6,
                bargroupgap=0.3
            )
            
            # 添加网格线
            fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
            
            # 添加城市分组的分割线
            for i in range(1, len(target_cities)):
                fig.add_vline(
                    x=i * 2 - 0.5,
                    line_dash="dash",
                    line_color="rgba(0,0,0,0.6)",
                    line_width=1
                )
            # rgba(128,128,128,0.4)
            return fig
        
        # 分离北京和其他城市
        beijing_cities = [city for city in cities_with_2024 if city == '北京']
        other_cities = [city for city in cities_with_2024 if city != '北京']
        
        # 生成北京图表
        if beijing_cities:
            st.write("### 📊 北京业态结构分析")
            beijing_fig = create_business_chart(beijing_cities, '北京一级业态结构对比分析', 500)
            st.plotly_chart(beijing_fig, use_container_width=True)
            
            # 北京数据摘要
            st.write("#### 📋 北京数据摘要")
            beijing_summary = []
            for city in beijing_cities:
                # 2024年数据
                city_2024 = city_year_business[
                    (city_year_business['城市'] == city) & 
                    (city_year_business['年份'] == 2024)
                ]
                total_2024 = city_2024['业绩金额'].sum()
                main_business_2024 = city_2024.loc[city_2024['业绩金额'].idxmax(), '一级业态'] if len(city_2024) > 0 else "无"
                
                # 2025年数据
                city_2025 = city_year_business[
                    (city_year_business['城市'] == city) & 
                    (city_year_business['年份'] == 2025)
                ]
                total_2025 = city_2025['业绩金额'].sum()
                main_business_2025 = city_2025.loc[city_2025['业绩金额'].idxmax(), '一级业态'] if len(city_2025) > 0 else "无"
                
                # 计算增长率
                growth_rate = ((total_2025 - total_2024) / total_2024 * 100) if total_2024 > 0 else 0
                
                beijing_summary.append({
                    '城市': city,
                    '2024年总业绩': f"{total_2024:,.0f}",
                    '2024年主要业态': main_business_2024,
                    '2025年总业绩': f"{total_2025:,.0f}",
                    '2025年主要业态': main_business_2025,
                    '增长率': f"{growth_rate:+.1f}%"
                })
            
            beijing_summary_df = pd.DataFrame(beijing_summary)
            st.dataframe(beijing_summary_df, use_container_width=True, hide_index=True)
        
        # 生成其他城市图表
        if other_cities:
            st.write("### 📊 其他重点城市业态结构分析")
            other_fig = create_business_chart(other_cities, '其他重点城市一级业态结构对比分析', 600)
            st.plotly_chart(other_fig, use_container_width=True)
            
            # 其他城市数据摘要
            st.write("#### 📋 其他城市数据摘要")
            other_summary = []
            for city in other_cities:
                # 2024年数据
                city_2024 = city_year_business[
                    (city_year_business['城市'] == city) & 
                    (city_year_business['年份'] == 2024)
                ]
                total_2024 = city_2024['业绩金额'].sum()
                main_business_2024 = city_2024.loc[city_2024['业绩金额'].idxmax(), '一级业态'] if len(city_2024) > 0 else "无"
                
                # 2025年数据
                city_2025 = city_year_business[
                    (city_year_business['城市'] == city) & 
                    (city_year_business['年份'] == 2025)
                ]
                total_2025 = city_2025['业绩金额'].sum()
                main_business_2025 = city_2025.loc[city_2025['业绩金额'].idxmax(), '一级业态'] if len(city_2025) > 0 else "无"
                
                # 计算增长率
                growth_rate = ((total_2025 - total_2024) / total_2024 * 100) if total_2024 > 0 else 0
                
                other_summary.append({
                    '城市': city,
                    '2024年总业绩': f"{total_2024:,.0f}",
                    '2024年主要业态': main_business_2024,
                    '2025年总业绩': f"{total_2025:,.0f}",
                    '2025年主要业态': main_business_2025,
                    '增长率': f"{growth_rate:+.1f}%"
                })
            
            other_summary_df = pd.DataFrame(other_summary)
            st.dataframe(other_summary_df, use_container_width=True, hide_index=True)
        
        # 整体关键洞察
        st.write("#### 💡 整体关键洞察")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**🏆 业绩增长最快的城市:**")
            growth_analysis = []
            for city in cities_with_2024:
                city_2024_total = city_year_business[
                    (city_year_business['城市'] == city) & 
                    (city_year_business['年份'] == 2024)
                ]['业绩金额'].sum()
                
                city_2025_total = city_year_business[
                    (city_year_business['城市'] == city) & 
                    (city_year_business['年份'] == 2025)
                ]['业绩金额'].sum()
                
                if city_2024_total > 0:
                    growth = city_2025_total - city_2024_total
                    growth_analysis.append((city, growth))
            
            if growth_analysis:
                top_growth_city = max(growth_analysis, key=lambda x: x[1])
                st.write(f"- **{top_growth_city[0]}**: 增长 {top_growth_city[1]:,.0f}")
        
        with col2:
            st.write("**📈 主要业态分布:**")
            business_count = city_year_business['一级业态'].value_counts()
            for business, count in business_count.head(3).items():
                st.write(f"- **{business}**: {count} 个城市年份")

    else:
        st.write("重点城市均无2024年业绩数据，无法进行业态结构对比分析")

    # 业绩前三城市占比分析
    
# 提取年份信息（假设你有年份列或者需要从其他地方获取）
# 如果没有年份列，需要先添加年份信息
    df_2024['年份'] = 2024
    df_2025['年份'] = 2025
    df_all = pd.concat([df_2024, df_2025], ignore_index=True)
    st.write("### 集中度分析")

    # 计算每年每个城市的业绩总和
    city_performance = df_all.groupby(['年份', '城市'])['业绩金额'].sum().reset_index()

    # 计算每年的总业绩
    yearly_total = df_all.groupby('年份')['业绩金额'].sum().reset_index()
    yearly_total.columns = ['年份', '年度总业绩']

    # 计算每年前三城市的集中度
    concentration_data = []

    for year in [2024, 2025]:
        # 获取该年份的城市业绩数据
        year_data = city_performance[city_performance['年份'] == year]
        
        # 按业绩金额排序，取前三
        top3_cities = year_data.nlargest(3, '业绩金额')
        
        # 计算前三城市业绩总和
        top3_sum = top3_cities['业绩金额'].sum()
        
        # 获取该年份总业绩
        year_total = yearly_total[yearly_total['年份'] == year]['年度总业绩'].iloc[0]
        
        # 计算集中度百分比
        concentration_pct = (top3_sum / year_total) * 100
        
        concentration_data.append({
            '年份': year,
            '前三城市集中度': concentration_pct,
            '前三城市': ', '.join(top3_cities['城市'].tolist())
        })

    # 转换为DataFrame
    concentration_df = pd.DataFrame(concentration_data)

    # 使用go.Figure创建柱状图（仿照参考代码）
    fig = go.Figure()

    # 添加柱状图
    fig.add_trace(go.Bar(
        x=['2024年', '2025年'],  # 修改x轴标签
        y=concentration_df['前三城市集中度'],
        marker_color=['#C0C0C0', '#825D48'],  # 设置指定颜色
        text=concentration_df['前三城市集中度'].apply(lambda x: f'{x:.1f}%'),
        textposition='outside',
        textfont=dict(size=12, color='#1B4965'),
        width=0.3
    ))

    # 添加80%参考线
    fig.add_hline(y=80, line_dash="dash", line_color="red", 
                annotation_text="80%集中度线", annotation_position="bottom right")

    # 更新布局 - 仿照参考代码样式
    fig.update_layout(
        title='城市维度集中度分析 - 前三城市业绩占比',
        title_font=dict(color='#1B4965', size=16),  # 深色标题
        xaxis_title='年份',
        xaxis_title_font=dict(color='#1B4965', size=14),  # 深色x轴标题
        yaxis=dict(
            title='集中度 (%)',
            range=[0, 100],
            title_font=dict(color='#1B4965', size=14),  # 深色字体
            tickfont=dict(color='#1B4965', size=12),
            gridcolor='#F6F8FA',  # 浅白色网格线
            zerolinecolor='#F6F8FA'
        ),
        xaxis=dict(
            title_font=dict(color='#1B4965', size=14),  # 深色字体
            tickfont=dict(color='#1B4965', size=12),
            gridcolor='#F6F8FA',  # 浅白色网格线
            showgrid=False,  # 隐藏x轴网格线
            zerolinecolor='#F6F8FA'
        ),
        showlegend=False,
        height=500,
        font=dict(size=12, color='#1B4965'),  # 深色字体
        plot_bgcolor='#E3EAF3',  # 与PPT背景协调的浅色背景
        paper_bgcolor='#E3EAF3'  # 与PPT背景完全一致
    )

    # 在Streamlit中显示
    st.plotly_chart(fig, use_container_width=True)

    # 显示前三城市详情
    st.write("**前三城市详情:**")
    for _, row in concentration_df.iterrows():
        st.write(f"• {int(row['年份'])}年: {row['前三城市']} (集中度: {row['前三城市集中度']:.1f}%)")



    

    # 数据准备
    df_2024['年份'] = 2024
    df_2025['年份'] = 2025
    df_all = pd.concat([df_2024, df_2025], ignore_index=True)
    st.subheader("五.行业业绩分析")

    # 计算每年每个行业的业绩总和
    industry_performance = df_all.groupby(['年份', '行业'])['业绩金额'].sum().reset_index()

    # 透视表，便于计算
    industry_pivot = industry_performance.pivot(index='行业', columns='年份', values='业绩金额').fillna(0)

    # 计算总业绩并排序
    industry_pivot['总业绩'] = industry_pivot[2024] + industry_pivot[2025]
    industry_pivot_sorted = industry_pivot.sort_values('总业绩', ascending=False)

    # 计算增长率
    industry_pivot_sorted['增长率'] = ((industry_pivot_sorted[2025] - industry_pivot_sorted[2024]) / industry_pivot_sorted[2024] * 100).replace([float('inf'), -float('inf')], 0)

    # 创建子图：左侧y轴为业绩金额，右侧y轴为增长率
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # 添加2024年柱状图
    fig.add_trace(
        go.Bar(
            name='2024年',
            x=industry_pivot_sorted.index,
            y=industry_pivot_sorted[2024],
            marker_color='#C0C0C0',
            # text=industry_pivot_sorted[2024],
            # texttemplate='%{text:.0f}',
            # textposition='outside',
            # textfont=dict(color='#000000')
        ),
        secondary_y=False,
    )

    # 添加2025年柱状图
    fig.add_trace(
        go.Bar(
            name='2025年',
            x=industry_pivot_sorted.index,
            y=industry_pivot_sorted[2025],
            marker_color='#825D48',
            # text=industry_pivot_sorted[2025],
            # texttemplate='%{text:.0f}',
            # textposition='outside',
            # textfont=dict(color='#000000')
        ),
        secondary_y=False,
    )

    # 分离增长率为0和非0的数据点
    zero_growth_data = industry_pivot_sorted[industry_pivot_sorted['增长率'] == 0]
    non_zero_growth_data = industry_pivot_sorted[industry_pivot_sorted['增长率'] != 0]

    # 添加增长率折线图（非0的点）
    if not non_zero_growth_data.empty:
        fig.add_trace(
            go.Scatter(
                name='增长率(%)',
                x=non_zero_growth_data.index,
                y=non_zero_growth_data['增长率'],
                mode='lines+markers+text',
                line=dict(color='rgba(0,0,0,0.6)', width=3),
                marker=dict(size=8, color='rgba(0,0,0,0.6)', symbol='circle'),
                text=[f'{int(rate)}%' for rate in non_zero_growth_data['增长率']],  # 显示整数部分
                textposition='top center',
                textfont=dict(size=12, color='#1B4965'),
                connectgaps=True  # 连接间隙
            ),
            secondary_y=True,
        )

    # 添加新增行业的特殊标记（增长率为0的点）- 放在-100%位置
    if not zero_growth_data.empty:
        fig.add_trace(
            go.Scatter(
                name='新增行业',
                x=zero_growth_data.index,
                y=[-100] * len(zero_growth_data),  # 固定在-100%位置
                mode='markers',
                marker=dict(
                    size=12,
                    color='rgba(0,0,0,0.6)',
                    symbol='triangle-up',  # 小三角形
                    line=dict(width=2, color='rgba(0,0,0,0.6)')
                ),
                showlegend=True
            ),
            secondary_y=True,
        )

    # 更新左侧y轴标题
    fig.update_yaxes(
        title_text="业绩金额",
        secondary_y=False,
        title_font=dict(color='#1B4965', size=14),  # 深色字体确保清晰
        tickfont=dict(color='#1B4965', size=12),
        gridcolor='#F6F8FA',  # 浅白色网格线
        zerolinecolor='#F6F8FA',  # 零轴线颜色与网格线一致
        dtick=4700,  # 固定刻度间隔为50000
        nticks=6,  # 限制刻度数量，只保留重要的
    )

    # 更新右侧y轴标题 - 确保包含-100%的范围
    fig.update_yaxes(
        title_text="增长率 (%)",
        secondary_y=True,
        title_font=dict(color='#1B4965', size=14),
        tickfont=dict(color='#1B4965', size=12),
        gridcolor='#F6F8FA',
        zerolinecolor='#F6F8FA',
        range=[-100, industry_pivot_sorted['增长率'].max() * 1.1],  # 确保包含-100%到最大增长率
        dtick=1000,
        nticks=6,
    )

    # 更新布局
    fig.update_layout(
        title='行业业绩分析',
        title_font=dict(color='#1B4965', size=16),  # 深色标题
        xaxis_title='行业',
        xaxis_title_font=dict(color='#1B4965', size=14),  # 深色x轴标题
        height=600,
        showlegend=True,
        plot_bgcolor='#E3EAF3',  # 与PPT背景协调的浅色背景
        paper_bgcolor='#E3EAF3',  # 与PPT背景完全一致
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color='#1B4965', size=12)  # 深色图例文字
        ),
        # 更新x轴刻度标签颜色
        xaxis=dict(
            tickfont=dict(color='#1B4965', size=12),
            gridcolor='#F6F8FA',  # 浅白色网格线
            showgrid=False,
            zerolinecolor='#F6F8FA'  # 隐藏x轴网格线，因为通常不需要
        )
    )

    # 在Streamlit中显示
    st.plotly_chart(fig, use_container_width=True)

    # 创建子图：左侧y轴为业绩金额，右侧y轴为增长率
    
#     # 创建子图：左侧y轴为业绩金额，右侧y轴为增长率
#     fig = make_subplots(specs=[[{"secondary_y": True}]])

#     # 添加2024年柱状图
#     fig.add_trace(
#         go.Bar(
#             name='2024年',
#             x=industry_pivot_sorted.index,
#             y=industry_pivot_sorted[2024],
#             marker_color='#C0C0C0',
#             # text=industry_pivot_sorted[2024],
#             # texttemplate='%{text:.0f}',
#             # textposition='outside',
#             # textfont=dict(color='#000000')
#         ),
#         secondary_y=False,
#     )

#     # 添加2025年柱状图
#     fig.add_trace(
#         go.Bar(
#             name='2025年',
#             x=industry_pivot_sorted.index,
#             y=industry_pivot_sorted[2025],
#             marker_color='#825D48',
#             # text=industry_pivot_sorted[2025],
#             # texttemplate='%{text:.0f}',
#             # textposition='outside',
#             # textfont=dict(color='#000000')
#         ),
#         secondary_y=False,
#     )

#     # 分离增长率为0和非0的数据点
#     zero_growth_data = industry_pivot_sorted[industry_pivot_sorted['增长率'] == 0]
#     non_zero_growth_data = industry_pivot_sorted[industry_pivot_sorted['增长率'] != 0]

#     # 添加增长率折线图（非0的点）
#     if not non_zero_growth_data.empty:
#         fig.add_trace(
#             go.Scatter(
#                 name='增长率(%)',
#                 x=non_zero_growth_data.index,
#                 y=non_zero_growth_data['增长率'],
#                 mode='lines+markers+text',
#                 line=dict(color='rgba(0,0,0,0.6)', width=3),
#                 marker=dict(size=8, color='rgba(0,0,0,0.6)', symbol='circle'),
#                 text=[f'{int(rate)}%' for rate in non_zero_growth_data['增长率']],  # 显示整数部分
#                 textposition='top center',
#                 textfont=dict(size=12, color='#1B4965'),
#                 connectgaps=True  # 连接间隙
#             ),
#             secondary_y=True,
#         )

#     # 添加新增行业的特殊标记（增长率为0的点）
#     if not zero_growth_data.empty:
#         fig.add_trace(
#             go.Scatter(
#                 name='新增行业',
#                 x=zero_growth_data.index,
#                 y=zero_growth_data['增长率'],
#                 mode='markers',
#                 marker=dict(
#                     size=10, 
#                     color='rgba(0,0,0,0.6)', 
#                     symbol='triangle-up',  # 小三角形
#                     line=dict(width=1, color='rgba(0,0,0,0.6)')
#                 ),
#                 showlegend=True
#             ),
#             secondary_y=True,
#         )

#     # 更新左侧y轴标题
#     fig.update_yaxes(
#     title_text="业绩金额", 
#     secondary_y=False,
#     title_font=dict(color='#1B4965', size=14),  # 深色字体确保清晰
#     tickfont=dict(color='#1B4965', size=12),
#     gridcolor='#F6F8FA',  # 浅白色网格线
#     zerolinecolor='#F6F8FA',  # 零轴线颜色与网格线一致
#     dtick=4700,  # 固定刻度间隔为50000
#     nticks=6,  # 限制刻度数量，只保留重要的
    
#     )


#     # 更新右侧y轴标题
#     fig.update_yaxes(
#         title_text="增长率 (%)", 
#         secondary_y=True,
#         title_font=dict(color='#1B4965', size=14),  # 深色字体确保清晰
#         tickfont=dict(color='#1B4965', size=12),
#         gridcolor='#F6F8FA',
#         zerolinecolor='#F6F8FA',
#         dtick=100,  # 让系统自动选择合适的刻度间隔
#         nticks=6 #
#     )

#     # 更新布局
#     fig.update_layout(
#     title='行业业绩分析 - 双柱状图与增长率折线图',
#     title_font=dict(color='#1B4965', size=16),  # 深色标题
#     xaxis_title='行业',
#     xaxis_title_font=dict(color='#1B4965', size=14),  # 深色x轴标题
#     height=600,
#     showlegend=True,
#     plot_bgcolor='#E3EAF3',  # 与PPT背景协调的浅色背景
#     paper_bgcolor='#E3EAF3',  # 与PPT背景完全一致
#     legend=dict(
#         orientation="h", 
#         yanchor="bottom", 
#         y=1.02, 
#         xanchor="right", 
#         x=1,
#         font=dict(color='#1B4965', size=12)  # 深色图例文字
#     ),
#     # 更新x轴刻度标签颜色
#     xaxis=dict(
#         tickfont=dict(color='#1B4965', size=12),
#         gridcolor='#F6F8FA',  # 浅白色网格线
#         showgrid=False,
#         zerolinecolor='#F6F8FA'  # 隐藏x轴网格线，因为通常不需要
#     )
# )

#     # 在Streamlit中显示
#     st.plotly_chart(fig, use_container_width=True)





    
    st.subheader("六.重点客户分析")

    # 筛选选项
    year_filter = st.selectbox("选择年份", [2024, 2025, "全部"])

    # 获取客户与行业的对应关系
    def get_client_industry_mapping(df):
        """获取客户与行业的映射关系"""
        return df.groupby('客户')['行业'].first().to_dict()

    # 根据年份筛选数据并计算业绩
    if year_filter == "全部":
        client_data = df_all.groupby('客户')['业绩金额'].sum().sort_values(ascending=False).head(10)
        industry_mapping = get_client_industry_mapping(df_all)
    else:
        if year_filter == 2024:
            client_data = df_2024.groupby('客户')['业绩金额'].sum().sort_values(ascending=False).head(10)
            industry_mapping = get_client_industry_mapping(df_2024)
        else:
            client_data = df_2025.groupby('客户')['业绩金额'].sum().sort_values(ascending=False).head(10)
            industry_mapping = get_client_industry_mapping(df_2025)

    # 创建带行业前缀的客户名称
    client_with_industry = [f"{industry_mapping.get(client, '未知行业')}-{client}" for client in client_data.index]

    # 获取每个客户对应的行业
    client_industries = [industry_mapping.get(client, '未知行业') for client in client_data.index]

    # 定义颜色列表（更柔和的色调）
    colors = [
        '#A8DADC',  '#E9C46A', '#F4A261', '#E76F51',
        '#D4A5A5', '#C8B6E2', '#A3C4F3', '#90DBF4', '#8FCACA',
        '#F7D794', '#DDA0DD', '#F0B7A1', '#C9E4CA', '#FFE5D9',
        '#B4E7CE', '#D1C4E9', '#FFECB3', '#E1F5FE', '#F8BBD9'
    ]

    # 获取数据中的唯一行业并按顺序分配颜色
    unique_industries = list(set(client_industries))
    industry_color_map = {industry: colors[i % len(colors)] for i, industry in enumerate(unique_industries)}

    # 为每个客户分配颜色
    bar_colors = [industry_color_map[industry] for industry in client_industries]

    # 绘制图表
    fig8 = px.bar(x=client_data.values, y=client_with_industry, orientation='h',
                title=f"前10大客户业绩排名 ({year_filter}年)",
                text=client_data.values)  # 添加文本显示数值
    fig8.update_traces(
        marker_color=bar_colors,
        texttemplate='%{text:,.0f}',  # 格式化数值显示，添加千位分隔符
        textposition='inside',  # 文本位置在柱子内部
        textfont=dict(color='white', size=12)  # 设置文本颜色和大小
    )
    fig8.update_layout(
        yaxis={'categoryorder':'total ascending', 'tickfont':dict(color='#1B4965', size=12)},
        plot_bgcolor='#E3EAF3', 
        paper_bgcolor='#E3EAF3',
        font=dict(color='#1B4965', size=12),  # 全局字体颜色
        title_font=dict(color='#1B4965', size=16),  # 标题单独设置
        xaxis=dict(tickfont=dict(color='#1B4965', size=12))  # X轴刻度标签
    )
    st.plotly_chart(fig8, use_container_width=True)

    # 客户分析结果
    if year_filter == "全部":
        top_client = df_all.groupby('客户')['业绩金额'].sum().idxmax()
        top_client_industry = df_all[df_all['客户'] == top_client]['行业'].iloc[0]
        client_count = len(df_all['客户'].unique())
    elif year_filter == 2024:
        top_client = df_2024.groupby('客户')['业绩金额'].sum().idxmax()
        top_client_industry = df_2024[df_2024['客户'] == top_client]['行业'].iloc[0]
        client_count = len(df_2024['客户'].unique())
    else:
        top_client = df_2025.groupby('客户')['业绩金额'].sum().idxmax()
        top_client_industry = df_2025[df_2025['客户'] == top_client]['行业'].iloc[0]
        client_count = len(df_2025['客户'].unique())

    st.info(f"**客户分析**：{year_filter}年最重要客户为{top_client_industry}-{top_client}，共服务{client_count}个客户")

    # 定义重点城市列表
    key_cities = ['广州', '北京', '成都', '上海', '杭州', '重庆', '深圳', '珠海', '天津', '苏州']

    # 分别获取2024年和2025年的数据
    df_2024_city = df_2024.groupby('城市')['业绩金额'].sum().reset_index()
    df_2025_city = df_2025.groupby('城市')['业绩金额'].sum().reset_index()

    # 计算2024年各城市业绩
    cities_2024 = set(df_2024_city['城市'].tolist())
    cities_2025 = set(df_2025_city['城市'].tolist())

    # 2024年重点城市业绩
    key_cities_2024 = [city for city in key_cities if city in cities_2024]
    key_cities_2024_amount = df_2024_city[df_2024_city['城市'].isin(key_cities_2024)]['业绩金额'].sum()
    other_cities_2024_amount = df_2024_city[~df_2024_city['城市'].isin(key_cities_2024)]['业绩金额'].sum()
    total_2024 = key_cities_2024_amount + other_cities_2024_amount

    # 2025年重点城市业绩
    key_cities_2025 = [city for city in key_cities if city in cities_2025]
    # 24年已有业绩的重点城市在25年的业绩
    existing_key_cities_2025 = [city for city in key_cities_2024 if city in cities_2025]
    existing_key_cities_2025_amount = df_2025_city[df_2025_city['城市'].isin(existing_key_cities_2025)]['业绩金额'].sum()
    # 新增重点城市在25年的业绩
    new_key_cities_2025 = [city for city in key_cities_2025 if city not in key_cities_2024]
    new_key_cities_2025_amount = df_2025_city[df_2025_city['城市'].isin(new_key_cities_2025)]['业绩金额'].sum()
    # 其他城市在25年的业绩
    other_cities_2025_amount = df_2025_city[~df_2025_city['城市'].isin(key_cities_2025)]['业绩金额'].sum()
    total_2025 = existing_key_cities_2025_amount + new_key_cities_2025_amount + other_cities_2025_amount

    # 找出24、25年都没有业绩的重点城市
    no_performance_cities = [city for city in key_cities if city not in cities_2024 and city not in cities_2025]

    # 创建子图
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('2024年上半年重点城市业绩占比', '2025年上半年重点城市业绩占比'),
        specs=[[{"type": "pie"}, {"type": "pie"}]]
    )

    # 2024年饼图
    fig.add_trace(
        go.Pie(
            labels=['重点城市', '其他城市'],
            values=[key_cities_2024_amount, other_cities_2024_amount],
            name="2024年",
            marker=dict(colors=['#825D48', '#C0C0C0']),
            textinfo='label+percent',
            textposition='inside',
            textfont=dict(color='#1B4965', size=12),
            hovertemplate='<b>%{label}</b><br>金额: %{value}<br>占比: %{percent}<extra></extra>'
        ),
        row=1, col=1
    )

    # 2025年饼图 - 合并重点城市
    total_key_cities_2025_amount = existing_key_cities_2025_amount + new_key_cities_2025_amount

    labels_2025 = []
    values_2025 = []
    colors_2025 = []

    if total_key_cities_2025_amount > 0:
        labels_2025.append('重点城市')
        values_2025.append(total_key_cities_2025_amount)
        colors_2025.append('#825D48')

    if other_cities_2025_amount > 0:
        labels_2025.append('其他城市')
        values_2025.append(other_cities_2025_amount)
        colors_2025.append('#C0C0C0')

    fig.add_trace(
        go.Pie(
            labels=labels_2025,
            values=values_2025,
            name="2025年",
            marker=dict(colors=colors_2025),
            textinfo='label+percent',
            textposition='inside',
            textfont=dict(color='#1B4965', size=12),
            hovertemplate='<b>%{label}</b><br>金额: %{value}<br>占比: %{percent}<extra></extra>'
        ),
        row=1, col=2
    )

    # 更新布局
    fig.update_layout(
        title_text="重点城市业绩金额占比变化对比",
        title_x=0.4,
        title_font=dict(color='#1B4965', size=16),
        showlegend=False,
        height=600,
        width=1200,
        font=dict(color='#1B4965', size=12),
        plot_bgcolor='#E3EAF3',
        paper_bgcolor='#E3EAF3'
    )

    # 显示图表
    st.plotly_chart(fig, use_container_width=True)

    # 输出没有业绩的重点城市
    if no_performance_cities:
        st.write(f"**注意：** 以下重点城市在2024年和2025年都没有业绩记录：{', '.join(no_performance_cities)}")

    # 输出统计信息
    st.write("### 统计信息")
    col1, col2 = st.columns(2)

    with col1:
        st.write("**2024年:**")
        st.write(f"- 重点城市总业绩: {key_cities_2024_amount:,.0f}")
        st.write(f"- 其他城市总业绩: {other_cities_2024_amount:,.0f}")
        st.write(f"- 总业绩: {total_2024:,.0f}")
        st.write(f"- 有业绩的重点城市: {', '.join(key_cities_2024) if key_cities_2024 else '无'}")

    with col2:
        st.write("**2025年:**")
        st.write(f"- 24年已有重点城市业绩: {existing_key_cities_2025_amount:,.0f}")
        st.write(f"- 新增重点城市业绩: {new_key_cities_2025_amount:,.0f}")
        st.write(f"- 其他城市业绩: {other_cities_2025_amount:,.0f}")
        st.write(f"- 总业绩: {total_2025:,.0f}")
        st.write(f"- 新增重点城市: {', '.join(new_key_cities_2025) if new_key_cities_2025 else '无'}")