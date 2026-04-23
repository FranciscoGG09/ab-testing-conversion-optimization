import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataManager:
    """
    Gestiona la ingesta, limpieza y validación de los datasets para el A/B Testing Framework.
    """
    def __init__(self, ab_path: str, bank_path: str):
        self.ab_path = ab_path
        self.bank_path = bank_path
        self.ab_data = None
        self.bank_data = None

    def load_data(self):
        """Carga los archivos CSV y normaliza nombres de columnas esenciales."""
        logging.info("Cargando datasets...")
        try:
            self.ab_data = pd.read_csv(self.ab_path)
            self.bank_data = pd.read_csv(self.bank_path)
        except Exception as e:
            logging.error(f"Error al cargar los datos: {e}")
            raise

        # Normalizar nombres de columnas en marketing_AB
        if 'user id' in self.ab_data.columns:
             self.ab_data.rename(columns={'user id': 'user_id'}, inplace=True)
        if 'test group' in self.ab_data.columns:
             self.ab_data.rename(columns={'test group': 'test_group'}, inplace=True)
             
        logging.info("Datasets cargados exitosamente.")
        
    def validate_and_clean(self):
        """Limpia los datos, maneja nulos y asegura tipos correctos."""
        logging.info("Validando y limpiando datos...")
        
        # Eliminar nulos
        initial_ab_len = len(self.ab_data)
        self.ab_data.dropna(inplace=True)
        dropped_ab = initial_ab_len - len(self.ab_data)
        if dropped_ab > 0:
            logging.info(f"Se eliminaron {dropped_ab} filas con valores nulos en el dataset A/B.")

        initial_bank_len = len(self.bank_data)
        self.bank_data.dropna(inplace=True)
        dropped_bank = initial_bank_len - len(self.bank_data)
        if dropped_bank > 0:
            logging.info(f"Se eliminaron {dropped_bank} filas con valores nulos en el dataset bank1.")
        
        # Asegurar tipo booleano en bank_data para medir conversiones base
        if 'deposit' in self.bank_data.columns:
             self.bank_data['converted_baseline'] = self.bank_data['deposit'].map({'yes': True, 'no': False})
             
    def check_unit_interference(self):
        """
        Realiza un Sanity Check para confirmar que ningún usuario
        (identificado por user_id) esté simultáneamente en ambos grupos.
        """
        logging.info("Chequeando interferencia de unidades (A/A Check)...")
        # Filtrar usuarios por grupo de test
        users_ad = set(self.ab_data[self.ab_data['test_group'] == 'ad']['user_id'])
        users_psa = set(self.ab_data[self.ab_data['test_group'] == 'psa']['user_id'])
        
        # Calcular intersección
        overlap = users_ad.intersection(users_psa)
        if len(overlap) > 0:
            logging.warning(f"¡Alerta! Se detectó interferencia: {len(overlap)} usuarios están en ambos grupos. Removiéndolos del dataset...")
            self.ab_data = self.ab_data[~self.ab_data['user_id'].isin(overlap)]
        else:
            logging.info("Validación exitosa: No hay interferencia de unidades ('Spillover') entre grupos.")

    def preprocess(self):
        """Ejecuta el pipeline completo de preprocesamiento."""
        self.load_data()
        self.validate_and_clean()
        self.check_unit_interference()
        return self.ab_data, self.bank_data
