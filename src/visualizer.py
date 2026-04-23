import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from scipy.stats import norm
import logging

class Visualizer:
    def __init__(self, ab_data: pd.DataFrame, bank_data: pd.DataFrame, stats_results: dict):
        self.ab_data = ab_data
        self.bank_data = bank_data
        self.stats = stats_results

    def plot_confidence_interval(self) -> go.Figure:
        """Grafica el Lift de conversión con su Intervalo de Confianza."""
        lift = self.stats['absolute_lift']
        ci_lower, ci_upper = self.stats['ci_lift']
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=[lift],
            y=['Conversion Lift'],
            error_x=dict(type='data', symmetric=False, array=[ci_upper - lift], arrayminus=[lift - ci_lower], color='#2ecc71', thickness=2),
            mode='markers',
            marker=dict(color='#27ae60', size=15),
            name='Lift'
        ))
        
        # Referencia del 0%
        fig.add_vline(x=0, line_dash='dash', line_color='#e74c3c', annotation_text='0% Lift (Base)')
        
        fig.update_layout(
            title='Intervalo de Confianza del Lift (¿Cruza el Cero?)',
            xaxis_title='Absolute Lift',
            xaxis_tickformat='.2%',
            yaxis_title='',
            template='plotly_dark'
        )
        return fig
        
    def plot_gauss_distributions(self) -> go.Figure:
        """Visualización de Campana de Gauss (Densidad de la Muestra)"""
        p_c = self.stats['conv_rate_control']
        p_t = self.stats['conv_rate_treatment']
        se = self.stats['standard_error']
        
        x = np.linspace(min(p_c, p_t) - 4*se, max(p_c, p_t) + 4*se, 1000)
        
        n_c = len(self.ab_data[self.ab_data['test_group'] == 'psa'])
        n_t = len(self.ab_data[self.ab_data['test_group'] == 'ad'])
        
        se_c = np.sqrt(p_c * (1 - p_c) / n_c) if n_c > 0 else se
        se_t = np.sqrt(p_t * (1 - p_t) / n_t) if n_t > 0 else se
        
        y_c = norm.pdf(x, p_c, se_c)
        y_t = norm.pdf(x, p_t, se_t)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y_c, fill='tozeroy', name='Control (PSA)', line=dict(color='#e74c3c')))
        fig.add_trace(go.Scatter(x=x, y=y_t, fill='tozeroy', name='Tratamiento (AD)', line=dict(color='#3498db')))
        
        fig.update_layout(
            title='Distribución de Tasas de Conversión (Z-Test)',
            xaxis_title='Tasa de Conversión Estimada',
            xaxis_tickformat='.3%',
            yaxis_title='Densidad de Probabilidad',
            template='plotly_dark'
        )
        return fig

    def plot_correlation_heatmap(self) -> go.Figure:
        """Mapa de calor de correlaciones financieras en la base de datos."""
        numeric_cols = self.bank_data.select_dtypes(include=['int64', 'float64', 'bool']).columns
        corr = self.bank_data[numeric_cols].corr()
        
        fig = go.Figure(data=go.Heatmap(
                   z=corr.values,
                   x=corr.columns,
                   y=corr.index,
                   colorscale='Viridis'))
        
        fig.update_layout(
            title='Correlación de Variables Financieras',
            template='plotly_dark'
        )
        return fig

    def plot_funnel(self) -> go.Figure:
        """Funnel muy básico para marketing_AB: Total Usuarios -> Convertidos"""
        total_ad = len(self.ab_data[self.ab_data['test_group'] == 'ad'])
        converted_ad = self.ab_data[(self.ab_data['test_group'] == 'ad') & (self.ab_data['converted'])].shape[0]
        
        fig = go.Figure(go.Funnel(
            y=['Total Asignados a Tratam.', 'Usuarios Convertidos'],
            x=[total_ad, converted_ad],
            textinfo="value+percent initial"
        ))
        
        fig.update_layout(title="Funnel de Adquisición (Grupo Tratamiento)", template='plotly_dark')
        return fig

    def plot_segment_revenue(self, summary_by_bucket: pd.DataFrame) -> go.Figure:
        """Muestra el Revenue Lift esperado por Bucket de Balance."""
        fig = px.bar(
            summary_by_bucket, 
            x='balance_bucket', 
            y='revenue_lift',
            title='Revenue Lift Proyectado por Nivel de Saldo',
            labels={'revenue_lift': 'Revenue Lift Proyectado ($)', 'balance_bucket': 'Balance Bucket'},
            color='revenue_lift',
            color_continuous_scale='Mint'
        )
        fig.update_layout(template='plotly_dark')
        return fig
