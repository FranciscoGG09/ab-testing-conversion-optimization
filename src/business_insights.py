import pandas as pd
import logging
from typing import Dict, Any

class BusinessInsights:
    """
    Inteligencia de negocios y proyecciones financieras
    basadas en el Lift del experimento.
    """
    def __init__(self, bank_data: pd.DataFrame, experimental_lift: float, ltv: float = 500.0):
        self.data = bank_data.copy()
        self.lift = experimental_lift
        self.ltv = ltv
        self._create_buckets()

    def _create_buckets(self):
        """Segmenta los datos iniciales mediante cuantiles de saldo (balance)."""
        logging.info("Creando balance_buckets...")
        try:
            self.data['balance_bucket'] = pd.qcut(
                self.data['balance'], 
                q=3, 
                labels=['Bajo', 'Medio', 'Alto']
            )
        except Exception as e:
            logging.error(f"Error creando buckets: {e}")
            self.data['balance_bucket'] = 'No Definido'

    def calculate_global_impact(self) -> Dict[str, Any]:
        """Calcula el impacto monetario proyectado sobre toda la base."""
        total_users = len(self.data)
        baseline_conversions = self.data['converted_baseline'].sum()
        
        incremental_conversions = total_users * self.lift
        revenue_lift = incremental_conversions * self.ltv
        
        logging.info(f"Impacto Global Calculado: ${revenue_lift:,.2f}")
        return {
            'total_users': total_users,
            'baseline_conversions': int(baseline_conversions),
            'incremental_conversions': incremental_conversions,
            'revenue_lift': revenue_lift
        }

    def calculate_segment_impact(self) -> pd.DataFrame:
        """
        Calcula el Revenue Lift segmentado por balance_bucket y job,
        permitiendo identificar los segmentos más lucrativos.
        """
        logging.info("Calculando impacto por segmento...")
        grouped = self.data.groupby(['balance_bucket', 'job'], observed=True).agg(
            total_users=('age', 'count'),
            baseline_conversions=('converted_baseline', 'sum')
        ).reset_index()
        
        # Filtramos segmentos vacíos
        grouped = grouped[grouped['total_users'] > 0].copy()
        
        # Aplicamos la matemática del Lift
        grouped['incremental_conversions'] = grouped['total_users'] * self.lift
        grouped['revenue_lift'] = grouped['incremental_conversions'] * self.ltv
        
        # Ordenamos por mayor revenue_lift
        grouped.sort_values(by='revenue_lift', ascending=False, inplace=True)
        return grouped

    def get_summary_by_bucket(self) -> pd.DataFrame:
        """Agrega solo por bucket para las visualizaciones."""
        summary = self.data.groupby('balance_bucket', observed=True).agg(
            total_users=('age', 'count')
        ).reset_index()
        summary['revenue_lift'] = summary['total_users'] * self.lift * self.ltv
        return summary
