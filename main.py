import os
import logging
from src.data_manager import DataManager
from src.stats_engine import StatsEngine
from src.business_insights import BusinessInsights
from src.visualizer import Visualizer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    # 1. Rutas
    ab_path = "data/marketing_AB.csv"
    bank_path = "data/bank1.csv"
    
    # 2. Ingesta y Limpieza
    logging.info("--- FASE 1: Ingesta de Datos ---")
    data_manager = DataManager(ab_path, bank_path)
    ab_data, bank_data = data_manager.preprocess()
    
    # 3. Motor Estadístico
    logging.info("--- FASE 2: Diseño Experimental y Estadísticas ---")
    stats_engine = StatsEngine(ab_data, mde_absolute=0.02, alpha=0.05)
    
    # Power Analysis
    power_res = stats_engine.power_analysis()
    
    # Pruebas Z y Lift
    stats_res = stats_engine.run_statistics()
    
    # 4. Impacto de Negocios
    logging.info("--- FASE 3: Business Intelligence ---")
    empirical_lift = stats_res['absolute_lift']
    
    if empirical_lift <= 0:
        logging.warning("El Lift empírico es negativo o nulo. No hay impacto positivo para proyectar.")
        return
        
    business_insights = BusinessInsights(bank_data, experimental_lift=empirical_lift, ltv=500.0)
    
    # Impacto Global
    global_impact = business_insights.calculate_global_impact()
    
    # Segmentación
    segment_impact = business_insights.calculate_segment_impact()
    logging.info(f"\nTop 5 Segmentos más lucrativos:\n{segment_impact.head(5)}")
    
    # 5. Visualizaciones
    logging.info("--- FASE 4: Generación de Visualizaciones ---")
    os.makedirs('output', exist_ok=True)
    
    vis = Visualizer(ab_data, bank_data, stats_res)
    
    try:
        vis.plot_confidence_interval().write_html('output/confidence_interval.html')
        vis.plot_gauss_distributions().write_html('output/gauss_distribution.html')
        vis.plot_correlation_heatmap().write_html('output/financial_correlations.html')
        vis.plot_funnel().write_html('output/acquisition_funnel.html')
        
        summary_by_bucket = business_insights.get_summary_by_bucket()
        vis.plot_segment_revenue(summary_by_bucket).write_html('output/segment_revenue_lift.html')
        logging.info("Pipeline completado exitosamente. Gráficos guardados en el directorio 'output/'.")
    except Exception as e:
        logging.error(f"Error al generar visualizaciones: {e}")

if __name__ == "__main__":
    main()
