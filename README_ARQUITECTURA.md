# Documentación del Proyecto - Portal Mi Banco - Módulo Préstamos

## Introducción

Este proyecto es una API REST desarrollada con FastAPI para el módulo de préstamos del Portal Mi Banco. Permite simular cuotas de préstamo, enviar solicitudes de préstamo y gestionar solicitudes existentes. La aplicación sigue una arquitectura en capas para mantener la separación de responsabilidades y facilitar el mantenimiento.

## Arquitectura

La aplicación sigue una arquitectura en capas inspirada en patrones de diseño como MVC y Clean Architecture:

### Capas Principales

1. **Router (routers/)**: Define las rutas/endpoints de la API y delega las peticiones al Controller. Equivalente a rutas en Express.js o controladores en Laravel.

2. **Controller (controllers/)**: Recibe las peticiones del Router, valida datos y coordina con el Service. Devuelve respuestas HTTP.

3. **Service (services/)**: Contiene la lógica de negocio pura, como cálculos financieros y reglas de validación. No accede directamente a la base de datos.

4. **Repository (repositories/)**: Abstrae el acceso a la base de datos (Supabase). Maneja operaciones CRUD sin lógica de negocio.

5. **Models (models/)**: Define esquemas de datos usando Pydantic para validación de entrada/salida.

### Base de Datos
- **Tecnología**: Supabase (PostgreSQL como backend).
- **Tabla Principal**: `solicitudes_prestamo` con campos como user_id, monto, plazo_meses, tasa_anual, cuota_mensual, proposito, estado.

### Tecnologías Utilizadas
- **Framework**: FastAPI (Python).
- **Lenguaje**: Python 3.12.
- **Base de Datos**: Supabase.
- **Validación**: Pydantic.
- **Servidor**: Uvicorn.
- **Dependencias**: fastapi, uvicorn, pydantic, supabase, python-dotenv, etc.

## Instalación y Configuración

### Prerrequisitos
- Python 3.12 instalado.
- Cuenta en Supabase con proyecto configurado.

### Pasos de Instalación
1. Clonar el repositorio.
2. Crear entorno virtual:
   ```
   py -3.12 -m venv env
   ```
3. Activar entorno virtual:
   ```
   .\env\Scripts\activate  # Windows
   ```
4. Instalar dependencias:
   ```
   pip install -r requirements.txt
   ```
5. Configurar variables de entorno: Copiar `.example.env` a `.env` y completar SUPABASE_URL y SUPABASE_KEY.

### Ejecutar la Aplicación
```
python -m uvicorn main:app --reload
```
- API disponible en: http://localhost:8000
- Documentación automática en: http://localhost:8000/docs

## Endpoints

La API expone los siguientes endpoints bajo el prefijo `/api/prestamos`:

### Simulación de Préstamo
- **POST /api/prestamos/simular**
  - Descripción: Calcula la cuota mensual de un préstamo sin guardar en BD.
  - Request Body: `PrestamoSimularRequest` (monto, plazo_meses, tasa_anual).
  - Response: Detalles del cálculo incluyendo ITF e importe a recibir.

### Solicitud de Préstamo
- **POST /api/prestamos/solicitar**
  - Descripción: Calcula la cuota y guarda la solicitud en BD.
  - Request Body: `PrestamoSolicitudRequest` (user_id, monto, plazo_meses, tasa_anual, proposito, ingresos_mensuales).
  - Response: Confirmación de solicitud guardada.

### Gestión de Solicitudes
- **GET /api/prestamos/solicitudes/{user_id}**
  - Descripción: Lista todas las solicitudes de un usuario.
  - Response: Lista de solicitudes ordenadas por fecha descendente.

- **GET /api/prestamos/solicitudes/{user_id}/{solicitud_id}**
  - Descripción: Obtiene el detalle de una solicitud específica.
  - Response: Detalles completos de la solicitud.

- **DELETE /api/prestamos/solicitudes/{solicitud_id}**
  - Descripción: Cancela una solicitud pendiente.
  - Response: Confirmación de cancelación (solo si estado es 'pendiente').

## Procesos Core

### 1. Simulación de Préstamo
- **Descripción**: Permite a los usuarios calcular cuotas sin compromiso.
- **Flujo**:
  1. Usuario envía datos de simulación.
  2. Controller valida datos con Pydantic.
  3. Service calcula cuota usando fórmula de amortización con TEM e ITF.
  4. Devuelve resultado con desglose financiero.

### 2. Solicitud de Préstamo
- **Descripción**: Registra una solicitud formal en el sistema.
- **Flujo**:
  1. Usuario envía datos completos de solicitud.
  2. Controller valida y calcula cuota.
  3. Service guarda en BD vía Repository.
  4. Devuelve confirmación con ID de solicitud.

### 3. Gestión de Solicitudes
- **Descripción**: Permite consultar y cancelar solicitudes.
- **Flujo**:
  1. Usuario consulta lista o detalle.
  2. Repository recupera datos de Supabase.
  3. Service aplica lógica (ej. filtrado por estado).
  4. Controller devuelve datos formateados.

### Cálculo de Cuotas
- Utiliza Tasa Efectiva Mensual (TEM).
- Incluye ITF (0.005% del monto).
- Proporciona importe neto a recibir por el cliente.

## Modelos de Datos

### Esquemas Pydantic (models/schemas.py)
- **PrestamoSimularRequest**: Datos para simulación (monto, plazo, tasa).
- **PrestamoSolicitudRequest**: Datos para solicitud (incluye user_id, proposito, ingresos).
- **PrestamoSimularResponse**: Resultado de simulación (monto, tem_pct, cuota_mensual, total_intereses, itf, importe_a_recibir, total_a_pagar, plazo_meses, tasa_anual).

## Seguridad y Validaciones
- Validación automática con Pydantic.
- CORS habilitado para desarrollo.
- Autenticación vía Supabase (no implementada en este módulo).
- Validación de propósito en solicitudes (opciones limitadas).

## Próximos Pasos
- Implementar autenticación JWT.
- Agregar tests unitarios e integración.
- Desplegar en Azure o similar.
- Mejorar manejo de errores y logging.