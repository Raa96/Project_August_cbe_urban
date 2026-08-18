import streamlit as st
import pandas as pd
import plotly.express as px
import database as db
import styles as sy

# Page configuration
st.set_page_config(
    page_title="Coimbatore Urban Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

sy.inject_custom_css()
sy.page_header(
    "URBAN INTEL // Coimbatore",
    "> Real-time telemetry. Spatial intelligence. Cross-domain analytics.",
    badge="SYS.ONLINE — COIMBATORE"
)
sy.ticker()

# ─── Fetch KPI Data ────────────────────────────────────────────────────────────
kpis = db.get_overview_kpis()
df_areas = db.get_areas()
df_civic = db.get_civic_issues()
total_complaints = len(df_civic)
high_severity = len(df_civic[df_civic['severity'] == 'High'])
df_osm = db.get_osm_infrastructure()
total_osm = len(df_osm)
osm_hospitals = len(df_osm[df_osm['category'] == 'hospitals']) if total_osm else 0

# ─── KPI Cards ─────────────────────────────────────────────────────────────────
st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-card">
            <div class="kpi-value cyan">{kpis['total_areas']}</div>
            <div class="kpi-label">Active Wards</div>
            <div class="kpi-trend up">+0 // Static Grid</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-value">{kpis['total_records']:,}</div>
            <div class="kpi-label">Telemetry Records</div>
            <div class="kpi-trend up">All Modules Synced</div>
        </div>
        <div class="kpi-card amber">
            <div class="kpi-value amber">{kpis['avg_traffic']:,}</div>
            <div class="kpi-label">Avg Traffic / hr</div>
            <div class="kpi-trend warn">Peak: 06:30 PM</div>
        </div>
        <div class="kpi-card amber">
            <div class="kpi-value amber">{kpis['avg_aqi']}</div>
            <div class="kpi-label">Avg PM2.5 AQI</div>
            <div class="kpi-trend warn">Moderate Index</div>
        </div>
        <div class="kpi-card rose">
            <div class="kpi-value rose">{high_severity}</div>
            <div class="kpi-label">High Severity Issues</div>
            <div class="kpi-trend critical">CRITICAL</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-value">{total_complaints}</div>
            <div class="kpi-label">Total Civic Complaints</div>
            <div class="kpi-trend warn">Pending Review</div>
        </div>
        <div class="kpi-card lime">
            <div class="kpi-value lime">{total_osm}</div>
            <div class="kpi-label">OSM Open-Data POIs</div>
            <div class="kpi-trend up text-lime">Hospitals: {osm_hospitals}</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# ─── Cross-Domain Correlation ──────────────────────────────────────────────────
CHART_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(2,6,23,0.6)',
    font=dict(family='Fira Code, monospace', color='#94a3b8', size=11),
    margin=dict(l=12, r=12, t=36, b=12),
    xaxis=dict(gridcolor='#1e293b', linecolor='#1e293b', zerolinecolor='#1e293b'),
    yaxis=dict(gridcolor='#1e293b', linecolor='#1e293b', zerolinecolor='#1e293b'),
    legend=dict(bgcolor='rgba(15,23,42,0.6)', bordercolor='#334155', borderwidth=1),
)

st.markdown('<div class="section-label" style="margin-top:1rem;">Cross-Domain Correlation Matrix</div>', unsafe_allow_html=True)

df_traffic = db.get_traffic().groupby('area')['vehicle_count'].mean().reset_index()
df_aq = db.get_air_quality().groupby('area')['pm25'].mean().reset_index()
df_civic_counts = db.get_civic_issues().groupby('area').size().reset_index(name='complaints')
df_commercial = db.get_commercial_activity().groupby('area')['estimated_footfall'].mean().reset_index()

df_merged = (df_areas
             .merge(df_traffic, on='area', how='left')
             .merge(df_aq, on='area', how='left')
             .merge(df_civic_counts, on='area', how='left')
             .merge(df_commercial, on='area', how='left')
             .fillna(0))

col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="section-label">Traffic vs Air Quality</div>', unsafe_allow_html=True)
    fig = px.scatter(df_merged, x='vehicle_count', y='pm25', size='estimated_footfall', color='zone',
                     hover_name='area', size_max=40,
                     labels={'vehicle_count': 'Avg Traffic Volume', 'pm25': 'PM2.5 AQI', 'estimated_footfall': 'Est. Footfall'})
    fig.update_layout(**CHART_LAYOUT)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown('<div class="section-label">Commercial Activity vs Civic Complaints</div>', unsafe_allow_html=True)
    fig2 = px.scatter(df_merged, x='estimated_footfall', y='complaints', color='zone', hover_name='area',
                      labels={'estimated_footfall': 'Estimated Footfall', 'complaints': 'Total Complaints'})
    fig2.update_layout(**CHART_LAYOUT)
    st.plotly_chart(fig2, use_container_width=True)

st.markdown('<div class="section-label">Correlation Heatmap</div>', unsafe_allow_html=True)
corr = df_merged[['estimated_footfall', 'vehicle_count', 'pm25', 'complaints']].corr()
fig3 = px.imshow(corr, text_auto=True, aspect="auto",
                 color_continuous_scale=[[0, '#0f172a'], [0.5, '#3b82f6'], [1, '#22d3ee']])
fig3.update_layout(**CHART_LAYOUT)
st.plotly_chart(fig3, use_container_width=True)

# ─── Platform Subsystems Summary ──────────────────────────────────────────────
st.markdown('<div class="section-label" style="margin-top:2rem;">Platform Subsystems // Module Index</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
        <div class="info-card">
            <h4>Telemetry Hub</h4>
            <p>Traffic volume telemetry across 10 vital junctions and live meteorological vectors — vehicle density, peak-hour distribution, weather trends, and zone benchmarking.</p>
        </div>
        <div class="info-card">
            <h4>Spatial Explorer</h4>
            <p>Unified interactive map overlaying traffic nodes, AQI stations, civic hotspots, congestion heatmap, and 853 OpenStreetMap infrastructure POIs.</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="info-card">
            <h4>Air & Water Pollution</h4>
            <p>PM2.5/PM10 ambient air quality, pollutant distribution, IMD climate normals, rainfall wash-effect, and historical CPCB observations.</p>
        </div>
        <div class="info-card">
            <h4>Civic Governance</h4>
            <p>Grievance redressal tracking, severity matrix, data-driven insights, and actionable municipal recommendations.</p>
        </div>
    """, unsafe_allow_html=True)

sy.footer()