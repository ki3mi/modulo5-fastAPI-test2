# Informe de Actualización de Lógica de Cálculo de Cuotas de Préstamo

## Resumen Ejecutivo

Este documento detalla la actualización de la lógica de cálculo de cuotas de préstamo en la aplicación FastAPI. La modificación se realizó en la capa de servicio (`PrestamoService`), incorporando el cálculo del Impuesto a las Transacciones Financieras (ITF) y nuevos campos de respuesta para mejorar la precisión financiera y el cumplimiento normativo. La lógica anterior, que se encuentra comentada en el código, no incluía estos elementos, lo que podía generar discrepancias en los cálculos y riesgos operativos en producción.

## Contexto del Problema

### Capa Afectada
El problema se ubicaba en la **capa de servicio** (`services/prestamo_service.py`), específicamente en el método `calcular_cuota`. Esta capa es responsable de la lógica de negocio pura, incluyendo cálculos financieros y reglas de validación. No delega directamente el acceso a la base de datos, sino que utiliza repositorios para persistencia.

### Descripción del Problema Anterior
La lógica original utilizaba la fórmula de amortización francesa estándar para calcular la cuota mensual de un préstamo:

```
C = P * [r(1+r)^n] / [(1+r)^n - 1]
```

Donde:
- P = monto del préstamo
- r = tasa mensual decimal (tasa_anual / 100 / 12)
- n = plazo en meses

Esta fórmula calculaba únicamente la cuota mensual, el total a pagar y los intereses totales, sin considerar impuestos adicionales como el ITF ni proporcionar un desglose detallado del monto neto a recibir por el cliente.

### Riesgos en Producción
La omisión del ITF y la falta de campos como `importe_a_recibir` podía ocasionar los siguientes problemas reales:

1. **Discrepancias Financieras**: Los cálculos no reflejaban el costo real del préstamo, incluyendo impuestos obligatorios, lo que podía llevar a errores en la facturación y reportes financieros.
2. **Incumplimiento Normativo**: En Perú, el ITF es un impuesto obligatorio (T.U.O. Ley N° 28194), y su no inclusión viola regulaciones fiscales, exponiendo a la institución a multas y sanciones.
3. **Pérdidas Operativas**: Clientes podrían recibir montos incorrectos, generando reclamos, disputas legales y daño a la reputación.
4. **Errores en Simulaciones**: Las simulaciones de préstamo no eran precisas, afectando la toma de decisiones de los usuarios y potencialmente llevando a sobreendeudamiento o insatisfacción.
5. **Escalabilidad y Mantenimiento**: Una lógica incompleta dificulta futuras expansiones, como la integración con sistemas bancarios o auditorías, aumentando costos de mantenimiento.

## Nueva Lógica Implementada

### Cambios Principales
La nueva implementación reemplaza la fórmula anterior por un cálculo más preciso que incluye:

1. **Cálculo de la Tasa Efectiva Mensual (TEM)**: Utiliza la fórmula `(1 + tasa_anual / 100) ** (1 / 12) - 1` para obtener la tasa mensual efectiva.
2. **Fórmula de Cuota Actualizada**: `cuota = monto * tem / (1 - (1 + tem) ** -plazo)`, que es equivalente a la amortización francesa pero expresada en términos de TEM.
3. **Incorporación del ITF**: Se calcula como `itf = round(monto * ITF_TASA, 2)`, donde `ITF_TASA = 0.00005` (0.005%).
4. **Nuevos Campos de Respuesta**:
   - `itf`: Monto del impuesto ITF.
   - `importe_a_recibir`: Monto neto que recibe el cliente después de deducir el ITF (`monto - itf`).

### Campos de Respuesta Actualizados
La clase `PrestamoSimularResponse` en `models/schemas.py` ahora incluye los siguientes campos marcados como NUEVO:

- `itf` (float): Impuesto a las Transacciones Financieras aplicado al monto del préstamo.
- `importe_a_recibir` (float): Monto efectivo que el cliente recibe, descontando el ITF.

Estos campos proporcionan transparencia en los cálculos, permitiendo a los usuarios entender el impacto fiscal del préstamo.

### Beneficios de la Actualización
- **Precisión Financiera**: Los cálculos ahora incluyen todos los costos asociados, asegurando simulaciones realistas.
- **Cumplimiento Legal**: Incorpora el ITF según la legislación peruana, mitigando riesgos regulatorios.
- **Mejor Experiencia del Usuario**: Proporciona información detallada sobre el monto neto y el ITF, mejorando la confianza y reduciendo consultas.
- **Robustez en Producción**: Reduce la probabilidad de errores operativos y facilita auditorías y reportes.

## Recomendaciones
- **Pruebas Exhaustivas**: Realizar pruebas unitarias y de integración para validar los cálculos con diversos escenarios.
- **Monitoreo Continuo**: Implementar logging en la capa de servicio para rastrear cálculos y detectar anomalías.
- **Actualización de Documentación**: Asegurar que toda la documentación técnica refleje estos cambios.
- **Capacitación del Equipo**: Entrenar a desarrolladores y analistas en la nueva lógica para mantener consistencia en futuras modificaciones.

Este informe destaca la importancia de mantener la lógica de negocio actualizada y precisa, especialmente en aplicaciones financieras donde los errores pueden tener consecuencias significativas.