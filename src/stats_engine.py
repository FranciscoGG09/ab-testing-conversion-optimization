import numpy as np
import pandas as pd
import logging
from statsmodels.stats.proportion import proportions_ztest, proportion_confint
from statsmodels.stats.power import NormalIndPower
from typing import Dict, Any

class StatsEngine:
    """
    Motor estadístico para realizar Power Analysis,
    Z-test, y cálculo de Intervalos de Confianza.
    """
    def __init__(self, ab_data: pd.DataFrame, mde_absolute: float = 0.02, alpha: float = 0.05):
        self.ab_data = ab_data
        self.mde = mde_absolute
        self.alpha = alpha
        
        # Control ('psa') y Tratamiento ('ad')
        self.control_data = self.ab_data[self.ab_data['test_group'] == 'psa']
        self.treatment_data = self.ab_data[self.ab_data['test_group'] == 'ad']

    def power_analysis(self) -> Dict[str, Any]:
        """
        Estima si el tamaño de la muestra actual es suficiente para detectar el MDE,
        calculando el poder estadístico.
        """
        logging.info("Ejecutando Power Analysis...")
        
        n_control = len(self.control_data)
        n_treatment = len(self.treatment_data)
        
        if n_control == 0 or n_treatment == 0:
             raise ValueError("Datos insuficientes para el análisis de poder estadístico. Grupos vacíos.")
             
        p_control = float(self.control_data['converted'].mean())
        
        # Effect size (Cohen's h para proporciones)
        p_treatment_mde = p_control + self.mde
        
        if p_treatment_mde >= 1.0:
            logging.warning("MDE produce proporciones >= 1.0. Ajustando a 0.999")
            p_treatment_mde = 0.999
            
        h = 2 * np.arcsin(np.sqrt(p_treatment_mde)) - 2 * np.arcsin(np.sqrt(p_control))
        
        ratio = n_treatment / n_control
        
        power_analysis = NormalIndPower()
        actual_power = power_analysis.solve_power(
            effect_size=h, 
            nobs1=n_control, 
            alpha=self.alpha, 
            ratio=ratio, 
            alternative='two-sided'
        )
        
        required_n_control = power_analysis.solve_power(
            effect_size=h,
            power=0.8,
            alpha=self.alpha,
            ratio=ratio,
            alternative='two-sided'
        )
        
        logging.info(f"Poder estadístico actual: {actual_power:.2%}")
        
        return {
            'actual_power': actual_power,
            'is_sufficient': actual_power >= 0.8,
            'required_n_control': required_n_control,
            'current_n_control': n_control
        }

    def run_statistics(self) -> Dict[str, Any]:
        """
        Ejecuta el Z-test para proporciones e incluye Z-Score, p-value y SE.
        """
        logging.info("Calculando métricas estadísticas...")
        
        conv_control = int(self.control_data['converted'].sum())
        n_control = len(self.control_data)
        
        conv_treatment = int(self.treatment_data['converted'].sum())
        n_treatment = len(self.treatment_data)
        
        successes = np.array([conv_treatment, conv_control])
        nobs = np.array([n_treatment, n_control])
        
        # Z-test
        z_score, p_value = proportions_ztest(count=successes, nobs=nobs, alternative='two-sided')
        
        # Tasas de conversión base
        p_c = conv_control / n_control
        p_t = conv_treatment / n_treatment
        lift = p_t - p_c
        
        # Standard Error del Lift
        se = np.sqrt( (p_t * (1 - p_t) / n_treatment) + (p_c * (1 - p_c) / n_control) )
        
        # Confidence Interval (método normal asintótico de Wald)
        moe = 1.96 * se  # Margin of Error
        ci_lift_low = lift - moe
        ci_lift_upp = lift + moe

        results = {
            'conv_rate_control': p_c,
            'conv_rate_treatment': p_t,
            'absolute_lift': lift,
            'z_score': z_score,
            'p_value': p_value,
            'standard_error': se,
            'ci_lift': (ci_lift_low, ci_lift_upp),
            'statistically_significant': p_value < self.alpha
        }
        
        logging.info(f"Lift Absoluto: {lift:.4f} | Z-Score: {z_score:.2f} | P-value: {p_value:.4f}")
        return results
