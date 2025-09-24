# 🔐 Gobernanza de Datos

Este documento establece lineamientos mínimos de gobernanza para el laboratorio, abarcando **origen, linaje, validaciones, seguridad y roles**.

---

## 1. Origen y Linaje de Datos
- **Origen:** archivos CSV heterogéneos cargados en la capa *raw*.  
- **Linaje:**  
  - `raw` → datos sin procesar.  
  - `bronze` → ingesta organizada, sin modificaciones sustanciales.  
  - `silver` → datos validados y normalizados con esquema canónico.  
  - `gold` → cálculos de KPIs y métricas derivadas.  
- Cada transformación debe estar documentada en el código (comentarios + logs).

---

## 2. Validaciones Mínimas
- Formato de fechas (`YYYY-MM-DD`).  
- Tipos correctos en columnas (`date`, `string`, `float`).  
- No permitir valores nulos en `date` o `partner`.  
- `amount` debe ser numérico y no negativo.  
- Rechazar filas duplicadas exactas.

---

## 3. Política de Mínimos Privilegios
- Los accesos a carpetas/datasets deben otorgarse únicamente a quienes lo requieran.  
- Lectura y escritura diferenciadas:  
  - **Raw/Bronze:** solo equipo de ingesta.  
  - **Silver/Gold:** analistas y científicos de datos.  
- No almacenar credenciales en el repositorio.  

---

## 4. Trazabilidad
- Mantener logs de ingesta y transformaciones.  
- Versionado de datasets (por ejemplo, incluir timestamp o control de versiones en los archivos).  
- Documentar claramente los mapeos origen → canónico en el diccionario.  

---

## 5. Roles
- **Data Engineer:** diseña e implementa el pipeline (ingesta, validaciones, almacenamiento).  
- **Data Steward:** asegura calidad de datos, mantiene diccionario y reglas de validación.  
- **Data Analyst:** consume la capa *silver* y genera KPIs en la capa *gold*.  
- **Administrador:** controla accesos y cumplimiento de la política de mínimos privilegios.  
