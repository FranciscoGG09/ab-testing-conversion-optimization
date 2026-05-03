# 📊 A/B Testing – Optimización de Conversión para Créditos

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Jupyter-F37626?style=flat&logo=jupyter&logoColor=white" alt="Jupyter">
  <img src="https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white" alt="Pandas">
  <img src="https://img.shields.io/badge/NumPy-013243?style=flat&logo=numpy&logoColor=white" alt="NumPy">
  <img src="https://img.shields.io/badge/Scipy-8CAAE6?style=flat&logo=scipy&logoColor=white" alt="Scipy">
  <img src="https://img.shields.io/badge/Statsmodels-1E3A8A?style=flat&logo=python&logoColor=white" alt="Statsmodels">
</p>

**Marco de trabajo experimental** aplicado a una plataforma de servicios financieros para **optimizar la tasa de conversión (CRO)**.  
El proyecto documenta el proceso científico completo: desde la **formulación de la hipótesis** hasta la **validación estadística** de resultados, enfocado en la adquisición de nuevos clientes de crédito.

---

## 🎯 Objetivo del Proyecto

Identificar si un **cambio en el flujo de solicitud de crédito** (por ejemplo, en el diseño del formulario, los textos o el orden de los pasos) produce un **incremento estadísticamente significativo** en la tasa de conversión, comparado con la versión actual (control).

### Preguntas clave que responde:
- ¿El nuevo diseño **aumenta el porcentaje de usuarios** que completan la solicitud?
- ¿El efecto observado es real o producto del **azar**?
- ¿Qué **tamaño de muestra** se necesita para detectar una mejora mínima relevante?
- ¿Los resultados son **válidos y reproducibles** para tomar decisiones de negocio?

---

## 🧪 Metodología Experimental

Sigue el riguroso proceso de un **A/B Testing** aplicado a productos financieros:

1. **Hipótesis**  
   - H₀: No hay diferencia entre la versión control y la variante.  
   - H₁: La variante mejora la tasa de conversión.

2. **Diseño del experimento**  
   - Asignación aleatoria de usuarios a dos grupos.  
   - Cálculo de tamaño muestral (potencia estadística, nivel de significancia α = 0.05, MDE definido).  
   - Duración del test (evitar sesgos estacionales o de día de la semana).

3. **Recolección de datos**  
   - Métricas clave: `# visitantes`, `# conversiones`, `tasa de conversión`.  
   - Registro de variables secundarias (dispositivo, hora, segmento de cliente).

4. **Análisis estadístico**  
   - Prueba de hipótesis: **test de proporciones** (z-test o chi-cuadrado).  
   - Intervalos de confianza para la diferencia de conversión.  
   - Verificación de supuestos (independencia, tamaño de muestra suficiente).  
   - Análisis de sensibilidad y **resultados por segmentos**.

5. **Conclusiones y recomendaciones**  
   - Si p-valor < α → se rechaza H₀ → la variante es mejor.  
   - Interpretación del **lift** (incremento relativo).  
   - Recomendación de implementación global o iteración del test.

---

## 🛠️ Stack Tecnológico

| Área               | Herramientas / Librerías                        |
|--------------------|-------------------------------------------------|
| **Lenguaje**       | Python 3.10+                                    |
| **Entorno**        | Jupyter Notebook, Google Colab                  |
| **Manipulación**   | Pandas, NumPy                                   |
| **Estadística**    | SciPy (stats), Statsmodels, Pingouin            |
| **Visualización**  | Matplotlib, Seaborn, Plotly                     |
| **Control de pruebas**| `scipy.stats.proportions_ztest`, `ttest_ind` |

---

## 📂 Estructura del Repositorio
ab-testing-conversion-optimization/
│
├── notebooks/
│ ├── 01_diseno_experimento.ipynb # Cálculo de muestra, aleatorización
│ ├── 02_analisis_exploratorio.ipynb # EDA de los datos recolectados
│ ├── 03_prueba_hipotesis.ipynb # Test estadístico, intervalos
│ └── 04_segmentos_y_sensibilidad.ipynb# Análisis por subgrupos
│
├── data/
│ ├── raw/ # Datos sin procesar (anonimizados)
│ └── processed/ # Datos limpios y agregados
│
├── reports/
│ ├── informe_final.pdf # Conclusiones ejecutivas
│ └── graficos/ # Visualizaciones clave
│
├── src/
│ ├── experiment_design.py # Funciones para diseño del test
│ └── statistical_tests.py # Pruebas paramétricas y no paramétricas
│
├── requirements.txt
└── README.md

---

## 📊 Ejemplo de Resultados

Suponiendo un test con 10.000 usuarios por grupo:
Grupo	Visitantes	Conversiones	Tasa conversión
Control	10,000	980	9.80%
Variante	10,000	1,150	11.50%

    Diferencia absoluta: +1.70 puntos porcentuales

    Lift (incremento relativo): +17.35%

    p-valor: 0.0001 → Significativo

    Intervalo de confianza 95%: [0.8%, 2.6%]

👉 Conclusión: Implementar la variante conlleva un aumento estadísticamente significativo en la conversión de solicitudes de crédito.

---
## ❓ Preguntas Frecuentes (FAQ)

¿Por qué es importante el cálculo de tamaño de muestra antes del experimento?
Evita terminar el test sin suficiente potencia para detectar la mejora mínima que consideras relevante. También impide peeking (mirar los datos antes de tiempo) que infla la tasa de error tipo I.

¿Se realizó alguna segmentación posterior?
Sí, en el notebook 04_segmentos_y_sensibilidad.ipynb se analizan subgrupos como dispositivo (móvil vs. escritorio) y horario de visita, para asegurar que el efecto no esté ocultando desigualdades.

¿Los datos son reales o simulados?
El repositorio utiliza datos anonimizados o generados sintéticamente para demostrar la metodología. Los principios se aplican directamente a datos reales de la plataforma financiera.

---
## 👨‍💻 Autor

Desarrollado por **Francisco González**.

* **LinkedIn:** [linkedin.com/in/francisco-gonzalez](https://linkedin.com/in/francisco-javi-gonzalez-garcia)
* **GitHub:** [@FranciscoGG09](https://github.com/FranciscoGG09)
---
## 📄 Licencia

Este proyecto está bajo la licencia MIT – consulta el archivo LICENSE para más detalles.
text
