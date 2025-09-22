# 🚀 Configuración del Sistema

## 📋 Requisitos Previos

### 1. Base de Datos MySQL
1. **Instalar MySQL Server** (8.0 o superior)
2. **Crear la base de datos:**
   ```sql
   -- Ejecutar el archivo database_schema.sql
   mysql -u root -p < database_schema.sql
   ```

### 2. Google Places API (Opcional)
1. **Crear proyecto en Google Cloud Console:**
   - Ve a https://console.cloud.google.com/
   - Crea un nuevo proyecto o selecciona uno existente

2. **Habilitar Places API:**
   - En el menú, ve a "APIs & Services" > "Library"
   - Busca "Places API" y habilítala

3. **Crear API Key:**
   - Ve a "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "API Key"
   - Copia el API Key generado

## ⚙️ Configuración de la Aplicación

### 1. Variables de Entorno
1. **Copiar archivo de configuración:**
   ```bash
   cp .env.example .env
   ```

2. **Editar el archivo .env:**
   ```bash
   # Google Maps API Configuration
   GOOGLE_API_KEY=tu_api_key_de_google_aqui

   # MySQL Database Configuration
   DB_HOST=localhost
   DB_USER=tu_usuario_mysql
   DB_PASSWORD=tu_contraseña_mysql
   DB_NAME=label_generator_db
   DB_PORT=3306

   # Application Configuration
   SECRET_KEY=tu_clave_secreta_aqui
   DEBUG=False
   ```

### 2. Instalar Dependencias
```bash
pip install -r requirements.txt
```

## 🗄️ Configuración de Base de Datos

### 1. Ejecutar Schema
```bash
mysql -u tu_usuario -p < database_schema.sql
```

### 2. Verificar Instalación
El script creará automáticamente:
- ✅ Base de datos `label_generator_db`
- ✅ Tablas: `users`, `labels`, `app_settings`, `audit_log`
- ✅ Usuario administrador por defecto
- ✅ Configuraciones iniciales

## 🔑 Credenciales por Defecto

### Usuario Administrador
- **Usuario:** `admin`
- **Contraseña:** `123`

⚠️ **IMPORTANTE:** Cambiar la contraseña por defecto en producción.

## 🏃‍♂️ Ejecutar la Aplicación

### Aplicación Básica (Original)
```bash
python main.py
```

### Aplicación Completa (Con todas las funcionalidades)
```bash
python main_enhanced.py
```

## 🎯 Funcionalidades Disponibles

### 🏠 Inicio
- ✅ Formularios de remitente y destinatario
- ✅ Campo de tracking (opcional)
- ✅ Autocompletado de direcciones (con Google API)
- ✅ Guardado automático en base de datos

### ⚙️ Configuración
- ⏳ En desarrollo

### 👨‍💼 Administración (Requiere autenticación)
- ✅ Configuración de Google Places API
- ✅ Registro de nuevos usuarios
- ✅ Gestión de configuraciones

## 🔧 Configuración Avanzada

### Google Places API en Administración
1. Inicia sesión como administrador
2. Ve a la sección "Administración"
3. Configura el API Key de Google
4. Activa el autocompletado

### Registro de Usuarios
1. En el panel de administración
2. Click "Registrar Nuevo Usuario"
3. Los usuarios requieren aprobación del administrador

## 🐛 Solución de Problemas

### Error de Conexión a MySQL
```bash
# Verificar que MySQL esté corriendo
systemctl status mysql

# Verificar credenciales
mysql -u tu_usuario -p
```

### Error de Google API
- Verificar que el API Key sea válido
- Confirmar que Places API esté habilitada
- Revisar límites de uso en Google Cloud Console

### Error de Dependencias
```bash
# Reinstalar dependencias
pip install --upgrade -r requirements.txt
```

## 📊 Estructura de Base de Datos

### Tablas Principales
- **users:** Gestión de usuarios y administradores
- **labels:** Almacén de etiquetas generadas
- **app_settings:** Configuraciones de la aplicación
- **audit_log:** Registro de actividades

### Índices Optimizados
- Búsqueda por usuario
- Filtrado por fechas
- Búsqueda por tracking

## 🚀 Características Técnicas

### Dependencias Instaladas
- ✅ `mysql-connector-python` - Conexión MySQL
- ✅ `googlemaps` - Google Places API
- ✅ `sqlalchemy` - ORM para base de datos
- ✅ `bcrypt` - Encriptación de contraseñas
- ✅ `python-dotenv` - Variables de entorno

### Seguridad Implementada
- 🔐 Contraseñas hasheadas con bcrypt
- 🔑 Autenticación para panel de administración
- 📋 Validación de formularios
- 🛡️ Protección contra inyección SQL (SQLAlchemy)

¡La aplicación está lista para usar! 🎉