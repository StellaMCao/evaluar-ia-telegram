import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
import os # <-- ¡ASEGÚRATE DE QUE ESTÉ AQUÍ!

# Configuración del logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Reemplaza 'YOUR_TELEGRAM_BOT_TOKEN' con el TOKEN que te dio BotFather ---
import os
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
# -----------------------------------------------------------------------------

# Diccionario de contenido para el chatbot
CONTENT = {
    "start": {
        "text": "¡Hola! Bienvenido al chatbot <b>Evaluar-IA</b>. Aquí encontrará información clave sobre la evaluación en la educación universitaria, especialmente en la era de la Inteligencia Artificial, basada en literatura especializada.",
        "buttons": [
            [("¿Qué es la evaluación educativa?", "1_main")],
            [("IA en la evaluación: oportunidades y desafíos", "2_main")],
            [("Tipos y funciones de evaluación", "3_main")],
            [("Evidencias de aprendizaje y pruebas auténticas", "4_main")],
            [("Enfoques innovadores de evaluación con IA", "5_main")],
            [("Preocupaciones éticas y pedagógicas", "6_main")],
            [("Glosario y referencias bibliográficas", "7_main")]
        ]
    },
    "1_main": {
        "text": "Ha seleccionado: ¿Qué es la evaluación educativa?",
        "buttons": [
            [("Definición y propósito", "1_1")],
            [("Relación con enseñanza y aprendizaje", "1_2")],
            [("Volver al menú principal", "start")]
        ]
    },
    "1_1": {
        "text": "La evaluación se define como 'señalar el valor de algo', 'estimar, apreciar, calcular el valor', o 'estimar los conocimientos, aptitudes y rendimiento de los alumnos' [Anijovich & Cappelletti, p. 16]. En este contexto, se considera una oportunidad para que los alumnos visibilicen sus logros y reconozcan sus debilidades y fortalezas, además de cumplir la función clásica de aprobar, promover y certificar [Anijovich & Cappelletti, p. 13].",
        "buttons": [
            [("Volver a ¿Qué es la evaluación educativa?", "1_main")],
            [("Volver al menú principal", "start")]
        ]
    },
    "1_2": {
        "text": "La evaluación es fundamental para medir el progreso y el rendimiento de los estudiantes. Black y Wiliam (1998) argumentan que una evaluación efectiva proporciona información crucial sobre el grado en que se están alcanzando los objetivos de aprendizaje [South Florida Journal, p. 120]. Stiggins (2002) enfatiza que las evaluaciones bien diseñadas proporcionan a los educadores información detallada sobre la eficacia de sus estrategias pedagógicas, permitiéndoles realizar ajustes necesarios para mejorar la calidad de la enseñanza [South Florida Journal, p. 121].",
        "buttons": [
            [("Volver a ¿Qué es la evaluación educativa?", "1_main")],
            [("Volver al menú principal", "start")]
        ]
    },
    "2_main": {
        "text": "Ha seleccionado: IA en la evaluación: oportunidades y desafíos.",
        "buttons": [
            [("Impacto general de la IA", "2_1")],
            [("Beneficios de la IA en evaluación", "2_2")],
            [("Desafíos en la implementación de IA", "2_3")],
            [("Volver al menú principal", "start")]
        ]
    },
    "2_1": {
        "text": "La Inteligencia Artificial (IA) está transformando rápidamente el panorama educativo, con un impacto particularmente significativo en los procesos de evaluación y retroalimentación. Esta revolución tecnológica promete mejorar la precisión, eficiencia y personalización de las evaluaciones, al tiempo que ofrece retroalimentación más oportuna y relevante para los estudiantes [Retos para la Investigación, p. 21]. La evaluación asistida por IA abarca una amplia gama de aplicaciones, desde sistemas de tutoría inteligente hasta plataformas de aprendizaje adaptativo [Retos para la Investigación, p. 21].",
        "buttons": [
            [("Volver a IA en la evaluación: oportunidades y desafíos", "2_main")],
            [("Volver al menú principal", "start")]
        ]
    },
    "2_2": {
        "text": "La IA tiene un impacto positivo moderado en el rendimiento académico (tamaño del efecto de 0.51) y un efecto más pronunciado en las habilidades de pensamiento crítico (tamaño del efecto de 0.68) [Retos para la Investigación, p. 26]. Se observaron mejoras significativas en la eficiencia de la evaluación, con una reducción del 40% en el tiempo de calificación y un aumento del 30% en la consistencia de las evaluaciones [Retos para la Investigación, p. 25; South Florida Journal, p. 131]. La implementación de sistemas de IA resultó en un incremento del 15% en las tasas de retención estudiantil y un aumento del 22% en la satisfacción con la retroalimentación recibida [Retos para la Investigación, p. 25; South Florida Journal, p. 125]. Permite retroalimentación inmediata y personalizada a gran escala [Retos para la Investigación, p. 21, 25; South Florida Journal, p. 139].",
        "buttons": [
            [("Volver a IA en la evaluación: oportunidades y desafíos", "2_main")],
            [("Volver al menú principal", "start")]
        ]
    },
    "2_3": {
        "text": "La integración de la IA en la evaluación y retroalimentación educativa plantea desafíos importantes. Cuestiones como la privacidad de los datos, la equidad algorítmica y la necesidad de mantener un equilibrio entre la automatización y el juicio humano son preocupaciones críticas que deben abordarse [Retos para la Investigación, p. 21]. Además, es esencial garantizar que los educadores estén adecuadamente capacitados para utilizar y comprender estas nuevas herramientas tecnológicas [Retos para la Investigación, p. 21].",
        "buttons": [
            [("Volver a IA en la evaluación: oportunidades y desafíos", "2_main")],
            [("Volver al menú principal", "start")]
        ]
    },
    "3_main": {
        "text": "Ha seleccionado: Tipos y funciones de evaluación.",
        "buttons": [
            [("Funciones principales de la evaluación", "3_1")],
            [("Evaluación formativa vs. evaluación para el aprendizaje", "3_2")],
            [("Marco de cuatro cuadrantes", "3_3")],
            [("Volver al menú principal", "start")]
        ]
    },
    "3_1": {
        "text": "Las principales funciones de la evaluación son:\n\n" +
                "<b>Diagnosticar-predecir:</b> Ajustes y regulaciones para las propuestas de enseñanza [Anijovich & Cappelletti, p. 20].\n\n" +
                "<b>Registrar-verificar:</b> Desempeño de los alumnos en relación con los objetivos [Anijovich & Cappelletti, p. 21].\n\n" +
                "<b>Ofrecer devoluciones-orientaciones:</b> Retroalimentación para que los alumnos tomen conciencia de logros y errores [Anijovich & Cappelletti, p. 21].\n\n" +
                "<b>Seleccionar-clasificar-jerarquizar:</b> Situar a los estudiantes en relación con otros [Anijovich & Cappelletti, p. 21].\n\n" +
                "<b>Certificar-promover:</b> Determinar si el alumno alcanza las competencias mínimas requeridas [Anijovich & Cappelletti, p. 21].",
        "buttons": [
            [("Volver a tipos y funciones de evaluación", "3_main")],
            [("Volver al menú principal", "start")]
        ]
    },
    "3_2": {
        "text": "La evaluación para el aprendizaje se diferencia de la evaluación formativa en varios puntos. La evaluación para el aprendizaje busca mejorar la enseñanza y el aprendizaje, mientras que la formativa es un enfoque de la evaluación. La primera se enfoca en el futuro inmediato, mientras que la segunda puede abarcar periodos más largos. Los beneficiarios principales de la evaluación para el aprendizaje son los alumnos y el profesor en el aula, mientras que la formativa puede ser útil para otros profesores y contextos [Anijovich & Cappelletti, p. 28].",
        "buttons": [
            [("Volver a tipos y funciones de evaluación", "3_main")],
            [("Volver al menú principal", "start")]
        ]
    },
    "3_3": {
        "text": "El 'Marco de los Cuatro Cuadrantes' de Brookhart (2013) organiza los tipos de evaluación:\n\n" +
                "<b>Cuadrante 1 (Evaluación interna):</b> Formativa, para docentes, ayuda a planificar según necesidades de estudiantes [Anijovich & Cappelletti, p. 25].\n\n" +
                "<b>Cuadrante 2 ('Rendición de cuentas'):</b> Evaluaciones estandarizadas (escuela, distrito, provincia, país), para informar y mejorar prácticas de enseñanza [Anijovich & Cappelletti, p. 25].\n\n" +
                "<b>Cuadrante 3 (Estrategias de evaluación formativa en el aula):</b> Docentes y alumnos buscan evidencias para mejorar logros [Anijovich & Cappelletti, p. 27].\n\n" +
                "<b>Cuadrante 4 (Evaluación sumativa por grados y cursos):</b> Analiza e interpreta calificaciones individuales de pruebas [Anijovich & Cappelletti, p. 27].",
        "buttons": [
            [("Volver a tipos y funciones de evaluación", "3_main")],
            [("Volver al menú principal", "start")]
        ]
    },
    "4_main": {
        "text": "Ha seleccionado: Evidencias de aprendizaje y pruebas auténticas.",
        "buttons": [
            [("¿Qué son las evidencias?", "4_1")],
            [("Planificación y búsqueda de evidencias", "4_2")],
            [("Más allá de las pruebas tradicionales", "4_3")],
            [("Volver al menú principal", "start")]
        ]
    },
    "4_1": {
        "text": "Las 'evidencias de aprendizaje' son informaciones relevantes para fundamentar juicios y decisiones. El término 'evidencia' remite a una certeza clara y manifiesta de la que no se puede dudar, a la prueba determinante en un proceso [Anijovich & Cappelletti, p. 62]. Poner en evidencia implica revelar o demostrar algo [Anijovich & Cappelletti, p. 62]. No existen evidencias únicas ni instrumentos únicos para recogerlas [Anijovich & Cappelletti, p. 63].",
        "buttons": [
            [("Volver a evidencias de aprendizaje y pruebas auténticas", "4_main")],
            [("Volver al menú principal", "start")]
        ]
    },
    "4_2": {
        "text": "Para planificar la búsqueda de evidencias, es relevante revisar los objetivos de aprendizaje y las actividades de enseñanza. El 'diseño en retrospectiva' de McTighe y Wiggins (2004) propone una 'hoja de ruta' para la evaluación, identificando aprendizajes esperados, determinando evidencias buscadas y planificando tareas [Anijovich & Cappelletti, p. 69].",
        "buttons": [
            [("Volver a evidencias de aprendizaje y pruebas auténticas", "4_main")],
            [("Volver al menú principal", "start")]
        ]
    },
    "4_3": {
        "text": "Para definir la búsqueda de evidencias de aprendizaje, es necesario referirse a objetivos y criterios. El análisis de las producciones cotidianas de los alumnos puede constituir evidencias de sus aprendizajes, lo que permite el principio de variedad de fuentes y continuidad entre enseñanza y evaluación [Anijovich & Cappelletti, p. 73]. Las interacciones entre docente y alumnos son la situación privilegiada para obtener evidencias formativas [Anijovich & Cappelletti, p. 66].",
        "buttons": [
            [("Volver a evidencias de aprendizaje y pruebas auténticas", "4_main")],
            [("Volver al menú principal", "start")]
        ]
    },
    "5_main": {
        "text": "Ha seleccionado: Enfoques innovadores de evaluación con IA.",
        "buttons": [
            [("Evaluaciones basadas en proyectos", "5_1")],
            [("Portafolios digitales", "5_2")],
            [("Evaluaciones interactivas y adaptativas con IA", "5_3")],
            [("Simulaciones y realidad virtual", "5_4")],
            [("Gamificación", "5_5")],
            [("Otros enfoques con IA", "5_6")],
            [("Volver al menú principal", "start")]
        ]
    },
    "5_1": {
        "text": "Este enfoque fomenta proyectos que requieren aplicación práctica de conocimientos, donde la originalidad y el pensamiento crítico son esenciales. Son reconocidos por su capacidad para evaluar competencias integrales y promover el aprendizaje activo y significativo [South Florida Journal, p. 141].",
        "buttons": [
            [("Volver a enfoques innovadores de evaluación con IA", "5_main")],
            [("Volver al menú principal", "start")]
        ]
    },
    "5_2": {
        "text": "Los portafolios digitales permiten a los estudiantes compilar trabajos a lo largo del tiempo, ofreciendo una visión holística de su progreso y aprendizaje [South Florida Journal, p. 141; Anijovich & Cappelletti, p. 78].",
        "buttons": [
            [("Volver a enfoques innovadores de evaluación con IA", "5_main")],
            [("Volver al menú principal", "start")]
        ]
    },
    "5_3": {
        "text": "Las evaluaciones interactivas y adaptativas con IA pueden ofrecer experiencias personalizadas que se ajustan en tiempo real a las capacidades de cada estudiante, revolucionando la evaluación al proporcionar desafíos adecuados al nivel de habilidad y promover la mejora continua [South Florida Journal, p. 141].",
        "buttons": [
            [("Volver a enfoques innovadores de evaluación con IA", "5_main")],
            [("Volver al menú principal", "start")]
        ]
    },
    "5_4": {
        "text": "Las simulaciones y la realidad virtual crean entornos inmersivos que simulan situaciones reales o históricas, permitiendo a los estudiantes demostrar su conocimiento en contextos prácticos y dinámicos [South Florida Journal, p. 141].",
        "buttons": [
            [("Volver a enfoques innovadores de evaluación con IA", "5_main")],
            [("Volver al menú principal", "start")]
        ]
    },
    "5_5": {
        "text": "La gamificación incorpora elementos de juegos en las evaluaciones para aumentar el compromiso y la motivación de los estudiantes, y evaluar habilidades de manera dinámica [South Florida Journal, p. 141].",
        "buttons": [
            [("Volver a enfoques innovadores de evaluación con IA", "5_main")],
            [("Volver al menú principal", "start")]
        ]
    },
    "5_6": {
        "text": "Otros enfoques incluyen el uso de análisis predictivo para evaluación continua, <i>peer review</i> asistido por IA, integración de <i>soft skills</i> en evaluaciones, uso de herramientas anti-plagio avanzadas, y evaluación basada en competencias [South Florida Journal, p. 148].",
        "buttons": [
            [("Volver a enfoques innovadores de evaluación con IA", "5_main")],
            [("Volver al menú principal", "start")]
        ]
    },
    "6_main": {
        "text": "Ha seleccionado: Preocupaciones éticas y pedagógicas.",
        "buttons": [
            [("Sesgos potenciales y comprensión humana", "6_1")],
            [("Privacidad y seguridad de datos", "6_2")],
            [("Costo y accesibilidad", "6_3")],
            [("Dificultades en la evaluación con IA", "6_4")],
            [("Volver al menú principal", "start")]
        ]
    },
    "6_1": {
        "text": "La principal preocupación (27.6% de los participantes) es el posible sesgo en la IA, lo que subraya la necesidad de sistemas transparentes y justos. La falta de comprensión humana (24.1%) indica conciencia sobre la singularidad del juicio humano, especialmente en áreas subjetivas de la evaluación [South Florida Journal, p. 134].",
        "buttons": [
            [("Volver a preocupaciones éticas y pedagógicas", "6_main")],
            [("Volver al menú principal", "start")]
        ]
    },
    "6_2": {
        "text": "Las inquietudes relacionadas con la privacidad y la seguridad de los datos (22.4% de los encuestados) reflejan la relevancia de proteger la información sensible de los estudiantes en la era digital. La protección de datos se presenta como un desafío crítico en la adopción de cualquier tecnología educativa [South Florida Journal, p. 134].",
        "buttons": [
            [("Volver a preocupaciones éticas y pedagógicas", "6_main")],
            [("Volver al menú principal", "start")]
        ]
    },
    "6_3": {
        "text": "Un 15.5% de los educadores están preocupados por el costo y la accesibilidad de la IA, lo que sugiere que las herramientas deben ser efectivas y accesibles para todas las instituciones y estudiantes, independientemente de sus recursos [South Florida Journal, p. 134].",
        "buttons": [
            [("Volver a preocupaciones éticas y pedagógicas", "6_main")],
            [("Volver al menú principal", "start")]
        ]
    },
    "6_4": {
        "text": "Los docentes enfrentan dificultades para evaluar la originalidad y creatividad (25%), el razonamiento lógico/procedimental (19%) y para detectar el plagio (25.9%) cuando los estudiantes utilizan herramientas de IA [South Florida Journal, p. 140]. La dificultad para evaluar la comprensión y el pensamiento crítico también son significativas [South Florida Journal, p. 140].",
        "buttons": [
            [("Volver a preocupaciones éticas y pedagógicas", "6_main")],
            [("Volver al menú principal", "start")]
        ]
    },
    "7_main": {
        "text": "Ha seleccionado: Glosario y referencias bibliográficas. ¿Qué desea consultar?",
        "buttons": [
            [("Glosario de términos", "7_1")],
            [("Referencias bibliográficas", "7_2")],
            [("Volver al menú principal", "start")]
        ]
    },
    "7_1": {
        "text": "<b>Glosario de términos:</b>\n\n" +
                "<b>Evaluación formativa:</b> Proceso continuo que provee información para mejorar el aprendizaje durante el curso [Anijovich & Cappelletti, p. 27].\n\n" +
                "<b>Evaluación sumativa:</b> Determina el logro final de los objetivos al final de un período, a menudo con fines de certificación [Anijovich & Cappelletti, p. 25].\n\n" +
                "<b>Evidencias de aprendizaje:</b> Información relevante recogida para fundamentar juicios de valor sobre los aprendizajes [Anijovich & Cappelletti, p. 61].\n\n" +
                "<b>Rúbricas:</b> Instrumentos de evaluación que describen los niveles de desempeño esperados para una tarea [Anijovich & Cappelletti, p. 101].\n\n" +
                "<b>Portafolios:</b> Colección organizada de trabajos de estudiantes que demuestran crecimiento y aprendizaje a lo largo del tiempo [Anijovich & Cappelletti, p. 78].\n\n" +
                "<b>IA en educación:</b> Sistemas informáticos que imitan funciones cognitivas humanas para procesar y analizar datos en el contexto educativo [South Florida Journal, p. 144].\n\n" +
                "<b>Sesgo algorítmico:</b> Inclinaciones injustas en los resultados de la IA debido a datos o diseño sesgados [South Florida Journal, p. 134].\n\n" +
                "<b>Retroalimentación multimodal:</b> Retroalimentación que combina diferentes tipos de datos (texto, voz, expresiones faciales) para una comprensión más completa [Retos para la Investigación, p. 23].",
        "buttons": [
            [("Volver a glosario y referencias bibliográficas", "7_main")],
            [("Volver al menú principal", "start")]
        ]
    },
    "7_2": {
        "text": "<b>Referencias bibliográficas:</b>\n\n" +
                "<b>Anijovich, Rebeca y Cappelletti, Graciela.</b> (2017). <i>La evaluación como oportunidad</i>. 1ª ed. Ciudad Autónoma de Buenos Aires: Paidós. ISBN 978-950-12-9485-9.\n\n" +
                "<b>Avalos Guijarro, Adriana de Los Ángeles.</b> (2024). \"Impacto de la Inteligencia Artificial en la evaluación y retroalimentación educativa.\" <i>Retos para la Investigación</i>, Vol. 3, No. 1 (Enero-Junio), pp. 19-32. ISSN:3028-868. DOI: <a href=\"https://doi.org/10.62465/rri.v3n1.2024.72\">https://doi.org/10.62465/rri.v3n1.2024.72</a>.\n\n" +
                "<b>Méndez-Mantuano, Marcel Oswaldo et al.</b> (2024). \"La evaluación académica en la era de la inteligencia artificial (IA).\" <i>South Florida Journal of Development</i>, Miami, v.5, n.1, pp. 119-148. ISSN 2675-5459. DOI: <a href=\"https://doi.org/10.46932/sfjdv5n1-010\">https://doi.org/10.46932/sfjdv5n1-010</a>.\n\n" +
                "Estas referencias corresponden a los documentos principales utilizados para elaborar la información de este chatbot. Se recomienda su consulta para mayor detalle y profundización.",
        "buttons": [
            [("Volver a glosario y referencias bibliográficas", "7_main")],
            [("Volver al menú principal", "start")]
        ]
    }
}

# Función para construir el teclado de botones
def build_keyboard(buttons_data):
    keyboard = []
    for row_data in buttons_data:
        row = []
        for text, callback_data in row_data:
            row.append(InlineKeyboardButton(text, callback_data=callback_data))
        keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)

# Manejador del comando /start
async def start(update: Update, context) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"¡Hola, {user.mention_html()}! {CONTENT['start']['text']}",
        reply_markup=build_keyboard(CONTENT['start']['buttons'])
    )

# Manejador de consultas de botones (CallbackQuery)
async def button(update: Update, context) -> None:
    query = update.callback_query
    await query.answer()

    page_key = query.data
    if page_key in CONTENT:
        page_info = CONTENT[page_key]
        text_to_send = page_info["text"]
        keyboard = build_keyboard(page_info["buttons"])
        await query.edit_message_text(
            text=text_to_send,
            reply_markup=keyboard,
            parse_mode='HTML'
        )
    else:
        await query.edit_message_text(
            text="Lo siento, esa opción no está disponible. Por favor, use el menú principal.",
            reply_markup=build_keyboard(CONTENT['start']['buttons']),
            parse_mode='HTML'
        )

# Manejador para cualquier otro mensaje
async def echo(update: Update, context) -> None:
    await update.message.reply_text(
        "Lo siento, no entiendo ese comando. Por favor, use los botones del menú.",
        reply_markup=build_keyboard(CONTENT['start']['buttons'])
    )

def main() -> None:
    """Inicia el bot."""
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':

    main()

