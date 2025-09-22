# 🔧 Arreglar Google Places API

## 🚨 Problema Identificado
Tu API Key está configurada para la **API antigua (Legacy)** que ya no está disponible.

**Error actual:**
```
REQUEST_DENIED - You're calling a legacy API, which is not enabled for your project
```

## 🛠️ Solución: Migrar a Places API (New)

### Paso 1: Habilitar la Nueva API
1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Selecciona tu proyecto
3. Ve a **APIs & Services** > **Library**
4. Busca **"Places API (New)"**
5. Haz clic en **"ENABLE"**

### Paso 2: Verificar Configuración
En **APIs & Services** > **Enabled APIs**, debes ver:
- ✅ **Places API (New)** - ¡ESTA ES LA CORRECTA!
- ❌ **Places API** (Legacy) - Esta es la antigua

### Paso 3: Actualizar Restricciones (Opcional pero Recomendado)
1. Ve a **APIs & Services** > **Credentials**
2. Edita tu API Key
3. En **API restrictions**, selecciona:
   - **Places API (New)**
   - **Geocoding API** (opcional)

## 🔄 Alternativa: Crear Nueva API Key

Si sigues teniendo problemas:

1. **Crear nueva API Key:**
   - Ve a **APIs & Services** > **Credentials**
   - Click **"CREATE CREDENTIALS"** > **"API Key"**

2. **Configurar la nueva key:**
   - Restrict by API: **Places API (New)**
   - Agregar restricciones de HTTP referrers si es necesario

3. **Actualizar .env:**
   ```env
   GOOGLE_API_KEY=tu_nueva_api_key_aqui
   ```

## 🧪 Probar la API

Ejecuta este comando para verificar:
```bash
python test_simple.py
```

Debe mostrar:
```
=== PROBANDO GOOGLE PLACES API ===
EXITO: X sugerencias encontradas
```

## 💡 Notas Importantes

- La nueva API tiene **mejor rendimiento**
- **Más funcionalidades** disponibles
- **Mismos costos** que la API antigua
- **Compatible** con el código actual

## ❓ Si Aún No Funciona

1. **Espera 5-10 minutos** después de habilitar la API
2. **Verifica facturación** esté habilitada en el proyecto
3. **Revisa cuotas** en Cloud Console
4. **Prueba con una nueva API Key**

Una vez arreglado, el autocompletado funcionará automáticamente en los formularios de dirección.