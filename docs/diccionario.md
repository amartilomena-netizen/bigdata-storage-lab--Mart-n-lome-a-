# 📖 Diccionario de Datos

Este documento describe el **esquema canónico** utilizado en la capa *silver* del laboratorio.  
El objetivo es homogenizar datos heterogéneos de distintas fuentes CSV hacia un formato confiable y trazable.

---

## Esquema Canónico

| Campo   | Descripción                          | Tipo   | Formato/Ejemplo       |
|---------|--------------------------------------|--------|-----------------------|
| `date`  | Fecha del registro                   | Date   | `2025-09-24` (YYYY-MM-DD) |
| `partner` | Nombre del socio/cliente/proveedor | String | `"ACME Corp"`         |
| `amount`  | Valor monetario en euros           | Float  | `1234.56`             |

---

## Mapeos Origen → Canónico

Ejemplos de correspondencia desde archivos CSV heterogéneos hacia el esquema estándar:

| Origen (columna)   | Canónico (`date`) | Canónico (`partner`) | Canónico (`amount`) |
|--------------------|------------------|----------------------|----------------------|
| `fecha`            | `date`           | –                    | –                    |
| `customer_name`    | –                | `partner`            | –                    |
| `importe`          | –                | –                    | `amount`             |
| `transactionDate`  | `date`           | –                    | –                    |
| `vendor`           | –                | `partner`            | –                    |
| `value_eur`        | –                | –                    | `amount`             |

*(El símbolo “–” indica que no aplica en ese mapeo.)*
