import plotly.graph_objects as go

def risk_timeline_interactive(df):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['risk_score'],
        mode='lines',
        name='Risk Score',
        hovertemplate=
        'Date: %{x}<br>' +
        'Risk Score: %{y:.2f}<extra></extra>'
    ))

    fig.add_hline(y=30, line_dash="dash", annotation_text="Low / Medium")
    fig.add_hline(y=60, line_dash="dash", annotation_text="Medium / High")

    fig.update_layout(
        title="Market Risk Regime (Interactive)",
        xaxis_title="Date",
        yaxis_title="Risk Score",
        hovermode="x unified"
    )

    return fig
def price_risk_overlay_interactive(df):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['Close'],
        mode='lines',
        name='Index Price'
    ))

    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['Close'],
        mode='markers',
        marker=dict(
            color=df['risk_score'],
            colorscale='RdYlGn_r',
            size=6,
            showscale=True,
            colorbar=dict(title="Risk")
        ),
        name='Risk Points',
        hovertemplate=
        'Date: %{x}<br>' +
        'Price: %{y:.2f}<br>' +
        'Risk Score: %{marker.color:.2f}<extra></extra>'
    ))

    fig.update_layout(
        title="Price with Risk Overlay (Interactive)",
        xaxis_title="Date",
        yaxis_title="Index Level"
    )

    return fig
def tail_risk_interactive(returns, var_95, cvar_95):
    fig = go.Figure()

    fig.add_trace(go.Histogram(
        x=returns,
        nbinsx=100,
        name='Returns',
        opacity=0.7
    ))

    fig.add_vline(x=var_95, line_color="orange",line_dash="dash", annotation_text="VaR 95%")
    fig.add_vline(x=cvar_95, line_color="red",line_dash="dash", annotation_text="CVaR 95%")

    fig.update_layout(
        title="Tail Risk Distribution (Interactive)",
        xaxis_title="Returns",
        yaxis_title="Frequency"
    )

    return fig
