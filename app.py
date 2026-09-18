
import html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

def shell(name, title, subtitle, style):
    global PALETTE, INK, PANEL, BG, ACCENT
    themes = {
      'terminal': ('#091411','#10221d','#e7f5ee','#3fe0a0','#7e9c8d',4),
      'purple': ('#171625','#222137','#f5f1ff','#ba9bff','#9ca1c0',12),
      'indigo': ('#f4f5fb','#ffffff','#242746','#5149b9','#64708b',18),
      'coral': ('#faf7f2','#ffffff','#302a27','#c7543e','#796d65',20),
      'blue': ('#f2f6fa','#ffffff','#183348','#126bb5','#5d7486',8),
      'cyan': ('#07141d','#102330','#def5ff','#53d2ed','#8caab9',4),
      'ops': ('#0b1720','#132733','#e7f5f4','#4edbc4','#99b5bd',10),
      'editorial': ('#f8f7f3','#ffffff','#253b38','#317764','#6b7d77',6),
      'amber': ('#17212c','#223140','#f8f4e9','#efbc67','#a6b2bf',6),
    }
    BG,PANEL,INK,ACCENT,MUTED,RADIUS=themes[style]
    PALETTE=[ACCENT,'#4c9fd6','#d99455','#ae83c6','#6cae8b']
    px.defaults.color_discrete_sequence=PALETTE
    st.markdown(f"""<style>
    .stApp {{background:{BG};color:{INK}}}
    [data-testid="stHeader"] {{background:{BG};}}
    .block-container {{max-width:1480px;padding:2rem 2.5rem 4rem;}}
    [data-testid="stSidebar"] {{background:{PANEL};border-right:1px solid {MUTED}35;}}
    h1,h2,h3,p,label,[data-testid="stMarkdownContainer"], [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {{color:{INK};}}
    h1 {{font-size:2.55rem!important;letter-spacing:-.055em;line-height:1.12!important;font-weight:650!important;}}
    h2,h3 {{letter-spacing:-.025em;}}
    [data-testid="stCaptionContainer"] {{opacity:1!important;}}
    [data-testid="stCaptionContainer"] p {{color:{MUTED}!important;}}
    [data-tag] {{background:{ACCENT}25!important;color:{INK}!important;border:1px solid {ACCENT}50;}}
    [data-tag] span,[data-tag] button {{color:{INK}!important;}}
    [data-testid="stMetric"] {{background:{PANEL};border:1px solid {MUTED}30;border-top:2px solid {ACCENT};border-radius:{RADIUS}px;padding:18px 20px;}}
    [data-testid="stMetricValue"] {{font-variant-numeric:tabular-nums;font-size:1.8rem;}}
    [data-testid="stPlotlyChart"] {{background:{PANEL};border:1px solid {MUTED}30;border-radius:{RADIUS}px;overflow:hidden;}}
    [data-baseweb="select"] > div, [data-baseweb="input"], [data-baseweb="base-input"], textarea {{background:{PANEL}!important;color:{INK}!important;}}
    input,textarea {{color:{INK}!important;-webkit-text-fill-color:{INK}!important;}}
    [data-baseweb="tag"] {{background:{ACCENT}25!important;color:{INK}!important;}}
    [data-baseweb="tag"] span {{color:{INK}!important;}}
    button[kind="secondary"], [data-testid="stDownloadButton"] button {{background:{PANEL};color:{INK};border-color:{MUTED}65;}}
    [data-baseweb="tab"] {{color:{INK}!important;}}
    [data-testid="stAlert"] {{background:{PANEL};color:{INK};}}
    .eyebrow {{font:600 11px ui-monospace,monospace;letter-spacing:.15em;color:{ACCENT};margin-bottom:16px;}}
    .hero {{border-bottom:1px solid {MUTED}40;padding:12px 0 25px;margin-bottom:24px;}}
    .hero p {{max-width:850px;color:{MUTED};font-size:1rem;}}
    .brief {{border-left:3px solid {ACCENT};background:{PANEL};padding:16px 20px;margin:18px 0;color:{INK};}}
    @media(max-width:700px){{.block-container{{padding:1rem;}}h1{{font-size:1.8rem!important;}}}}
    </style>""",unsafe_allow_html=True)
    st.markdown(f'<div class="hero"><div class="eyebrow">MORRIS / {html.escape(name.upper())} · SYNTHETIC DEMO</div><h1>{html.escape(title)}</h1><p>{html.escape(subtitle)}</p></div>',unsafe_allow_html=True)
    st.sidebar.caption('MORRIS · PORTFOLIO LAB')
    st.sidebar.caption('Fictional data. Explore the workflow; no external systems are connected.')

def chart(fig, height=340):
    for axis in [fig.layout.xaxis,fig.layout.yaxis]:
        if axis.title.text:axis.title.text=axis.title.text.replace('_',' ').title()
    for trace in fig.data:
        if trace.name:trace.name=trace.name.replace('_',' ').title()
    fig.update_layout(template='plotly_white',paper_bgcolor=PANEL,plot_bgcolor=PANEL,font=dict(color=INK,size=12),colorway=PALETTE,height=height,margin=dict(l=55,r=25,t=55,b=55),legend=dict(orientation='h',y=-.24,x=0),hoverlabel=dict(bgcolor=PANEL,font_color=INK))
    fig.update_xaxes(automargin=True,gridcolor='rgba(128,145,155,.14)',zerolinecolor='rgba(128,145,155,.3)')
    fig.update_yaxes(automargin=True,gridcolor='rgba(128,145,155,.14)',zerolinecolor='rgba(128,145,155,.3)')
    st.plotly_chart(fig,use_container_width=True,theme=None)

def brief(text):
    st.markdown('<div class="brief">'+html.escape(text)+'</div>',unsafe_allow_html=True)

def money(value):
    sign='−' if value<0 else ''
    return f'{sign}${abs(value)/1e6:,.2f}M' if abs(value)>=1e6 else f'{sign}${abs(value):,.0f}'

def metrics(items):
    for col,(label,value) in zip(st.columns(len(items)),items):col.metric(label,value)

def table(df, name='detail', height=360):
    config={}
    for col in df.columns:
        label=str(col).replace('_',' ').title()
        if pd.api.types.is_numeric_dtype(df[col]) and not pd.api.types.is_bool_dtype(df[col]):
            if any(x in str(col) for x in ['pct','margin','confidence','attainment','probability','achievement']):
                config[col]=st.column_config.NumberColumn(label,format='%.3f')
            elif any(x in str(col) for x in ['amount','revenue','arr','acv','cost','expense','cash','earned','capitalized','amortization','balance','asset','budget','forecast','variance','value','backlog','receipts','payroll','subcontractor','materials','labor']):
                config[col]=st.column_config.NumberColumn(label,format='$%.2f')
            else:config[col]=st.column_config.NumberColumn(label)
        else:config[col]=st.column_config.Column(label)
    st.dataframe(df,use_container_width=True,hide_index=True,height=height,column_config=config)
    st.download_button('Download '+name.replace('_',' ')+' CSV',df.to_csv(index=False),name+'.csv','text/csv',key='export_'+name)

def nonempty(df):
    if df.empty:
        st.info('No records in this selection. Choose at least one filter value to continue.')
        st.stop()

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from core import CommissionInputs, top_down, bottom_up, payline_table, scenario_table

st.set_page_config(page_title="Sales Commission Forecasting Engine", layout="wide")
shell('COMPENSATION LAB','Model the payout. Explain the expense.','Compare independent forecast methods, stress the plan, and trace earned commissions into expense and cash.','purple')

with st.sidebar:
    st.header("Scenario levers")
    achievement = st.slider("Plan achievement", 0.70, 1.05, 0.90, 0.01)
    baseline = st.number_input("Baseline variable potential ($M)", 10.0, 40.0, 22.4, 0.1) * 1_000_000
    merit = st.number_input("Merit increase ($M)", 0.0, 5.0, 0.62, 0.05) * 1_000_000
    investment = st.number_input("Investment potential ($M)", 0.0, 8.0, 1.05, 0.05) * 1_000_000
    accel_pool = st.number_input("Accelerator pool ($M)", 0.0, 10.0, 2.85, 0.05) * 1_000_000
    cap_rate = st.slider("Capitalization rate", 0.30, 0.65, 0.48, 0.01)
    amort = st.number_input("Prior-cohort amortization ($M)", 0.0, 15.0, 8.2, 0.1) * 1_000_000
    cash_ratio = st.slider("Cash / earned ratio", 0.85, 1.25, 1.07, 0.01)

inp = CommissionInputs(
    baseline_potential=baseline,
    merit_increase=merit,
    investment_potential=investment,
    accelerator_pool=accel_pool,
    achievement=achievement,
    capitalization_rate=cap_rate,
    prior_cohort_amortization=amort,
    cash_to_earned=cash_ratio,
)

td = top_down(inp)
bu = bottom_up(inp)


metrics([('Earned commissions',money(td['earned'])),('P&L expense',money(td['expense'])),('Cash requirement',money(td['cash'])),('Method gap',money(td['earned']-bu['earned']))])
brief(f"At {achievement:.0%} achievement, {cap_rate:.0%} of earned commissions are capitalized. Cash is modeled separately at {cash_ratio:.2f}× earned; this is a scenario assumption, not a reconciled payable balance.")
bridge_tab,drivers_tab,scenario_tab=st.tabs(['01 / Expense bridge','02 / Method comparison','03 / Scenario range'])
with bridge_tab:
    from core import bridge
    b=bridge(inp)
    fig=go.Figure(go.Waterfall(x=b.line,y=b.value,measure=['total' if x=='total' else 'relative' for x in b.type],increasing=dict(marker_color=ACCENT),decreasing=dict(marker_color='#e7977f'),totals=dict(marker_color='#679ed1')))
    fig.update_layout(title='Variable potential → earned → P&L expense',yaxis_tickprefix='$',yaxis_tickformat='.2s')
    chart(fig,460)
    st.caption('Negative capitalization removes the asset portion from current expense. Prior-cohort amortization then adds expense back.')
with drivers_tab:
    a,b=st.columns([1.4,1])
    compare=pd.DataFrame({'Method':['Top-down','Bottom-up'],'Earned':[td['earned'],bu['earned']],'Expense':[td['expense'],bu['expense']],'Cash':[td['cash'],bu['cash']]})
    with a:chart(px.bar(compare,x='Method',y=['Earned','Expense','Cash'],barmode='group',title='Independent methods'))
    with b:
        st.subheader('Bottom-up assumptions')
        st.write('Revenue, service commissions, early renewals, and net accelerators form an independent estimate. Sidebar achievement changes the top-down model only.')
        for label,v in [('Revenue commissions',bu['revenue_component']),('Services',bu['services_component']),('Early renewals',bu['early_renewal_bonus']),('Net accelerators',bu['net_accelerators'])]:st.write(f'{label}: **{money(v)}**')
    pay=payline_table()
    chart(px.line(pay,x='attainment',y='target_incentive_earned',markers=True,title='Illustrative accelerator curve',labels={'attainment':'Quota attainment','target_incentive_earned':'Target incentive earned'}))
    st.caption('Fictional policy: 1× through quota; 2.5× incremental rate from 100–150%; 1.25× above 150%.')
with scenario_tab:
    sc=scenario_table(inp)
    chart(px.bar(sc,x='scenario',y=['earned','expense','cash'],barmode='group',title='Scenario comparison'))
    table(sc,'commission_scenarios')
