import plotly.express as px

def retention_by_call_result(df):
    return px.bar(df.groupby('call_result')['retained'].mean().reset_index(),
                  x='call_result', y='retained', labels={'retained': 'Retention Rate'})
