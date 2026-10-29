# Anillos de Hábitos

App móvil (PWA) para trackear hábitos con anillos de cumplimiento. Funciona sin servidor: se publica en GitHub Pages y guarda los datos en tu celular.

## Publicar en GitHub Pages

1. Crea un repositorio nuevo en GitHub (por ejemplo `habitos`).
2. Sube estos archivos a la raíz: `index.html`, `foods.js`, `manifest.json`, `sw.js`, los tres `icon-*.png` y la carpeta `.github/`. (La carpeta `data/` es solo el material fuente de la base de alimentos; no hace falta subirla.)
3. En el repositorio: **Settings → Pages → Build and deployment → Source: Deploy from a branch**, rama `main`, carpeta `/ (root)`.
4. Espera un minuto. Tu app queda en `https://TU-USUARIO.github.io/habitos/`.
5. Ábrela en el celular y agrégala a la pantalla de inicio:
   - **iPhone (Safari):** Compartir → Agregar a pantalla de inicio.
   - **Android (Chrome):** menú ⋮ → Instalar aplicación.

## Secciones

- **Inicio:** anillos de cumplimiento (día, semana, mes, año), calorías y macros de hoy, y lo que te falta.
- **Registro:** detalle diario de cada hábito, con navegación entre fechas.
- **To-Do:** tareas por día, pendientes atrasadas y seguimiento.
- **Métricas:** barras por semana, mes y año, rachas, promedios y mapa de calor.
- **Ajustes:** metas, recordatorios, alimentos personalizados y respaldo.

El seguimiento **empieza mañana** respecto al día en que abres la app por primera vez (puedes cambiar la fecha en Ajustes → Fecha de inicio). En Métricas, «No fap» muestra los **días acumulados** desde la última recaída, la mejor racha y el total de recaídas.

## Cómo se registra cada hábito

| Hábito | Cómo se registra | Se cumple cuando |
|---|---|---|
| Agradecer | Un toque. **Solo hasta las 12:00 del mismo día.** | Lo marcaste dentro de la ventana |
| Comer saludable | Desayuno, almuerzo, cena y snack, alimento por alimento | Las calorías estimadas del día están en tu rango |
| Entrenar | Eliges el tipo de ejercicio (y opcional minutos y detalle) | Elegiste un ejercicio |
| Leer | Registras las páginas leídas del día; ves el avance semanal contra tu meta | Leíste al menos 1 página |
| Pantalla | Horas de uso. **Se habilita desde las 9:00 PM.** | Menos de tu límite (4 h por defecto) |
| Planificar | To-Do del día siguiente | Dejaste al menos una tarea para mañana |
| No fap | Se da por cumplido **por defecto**; solo registras una recaída si ocurrió | No registraste recaída ese día |

### Alimentación

La base incluye más de 1400 alimentos (comida peruana, pastas, arroces, panes, carnes, pescados, postres, bebidas, comida rápida, snacks, etc.) con calorías, proteína, grasas y carbohidratos **por 100 g**. Cada alimento trae una porción típica; puedes registrar por porciones o por gramos.

Los platos peruanos están separados por componentes para que no se cuente doble: por ejemplo «Ají de gallina (solo crema con pollo, sin arroz ni papa)» y aparte el arroz, la papa y el huevo. También hay versiones «completo» para registrar rápido.

Si no encuentras algo, crea un **alimento personalizado** (por 100 g o con los totales del plato). Los valores son estimados y varían según marca y preparación.

## Recordatorios durante el día

Los avisos usan **ntfy** (gratis, sin cuenta) y un GitHub Action con cron.

1. Instala la app **ntfy** (iOS / Android).
2. Inventa un tema privado difícil de adivinar, por ejemplo `habitos-tunombre-8f3k29`, y suscríbete a él en la app ntfy.
3. En el repositorio: **Settings → Secrets and variables → Actions**
   - Pestaña *Secrets* → New repository secret: `NTFY_TOPIC` = tu tema.
   - Pestaña *Variables* → New repository variable: `APP_URL` = la URL de tu app (al tocar la notificación se abrirá).
4. En la app, ve a **Ajustes → Recordatorios**, escribe el mismo tema y pulsa *Enviar notificación de prueba*.
5. También puedes probar el workflow desde **Actions → Recordatorios de hábitos → Run workflow**.

Horarios por defecto (hora de Lima):

| Hora | Aviso |
|---|---|
| 07:30 | Agradecer por el día |
| 08:00 | Revisar el To-Do |
| 09:30 | Registrar desayuno |
| 11:15 | Última llamada para agradecer |
| 14:30 | Registrar almuerzo |
| 17:00 | Entrenar |
| 20:00 | Leer y registrar cena |
| 21:00 | Se habilita la pantalla; cierre del día |
| 22:30 | Último aviso |

Para cambiar horarios, edita los `cron` en `.github/workflows/recordatorios.yml` (están en UTC; Lima = UTC-5).

Notas:
- GitHub puede retrasar los cron unos minutos.
- Si el repositorio no tiene actividad durante 60 días, GitHub pausa los workflows programados. Reactívalos desde la pestaña Actions.
- Los recordatorios son fijos: el servidor no conoce tus datos, que viven solo en tu celular.

## Datos

Todo se guarda en `localStorage` del celular. Haz un respaldo desde **Ajustes → Exportar respaldo** de vez en cuando; si cambias de teléfono, lo importas ahí mismo.

## Ampliar la base de alimentos

Los archivos de `data/` tienen una línea por alimento: `Nombre|proteína|grasa|carbohidratos|gramos de la porción|etiqueta de la porción` (valores por 100 g; un séptimo campo opcional fija las kcal). `build_foods.py` los compila a `foods.js`.
