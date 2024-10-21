from llama_index.core import PromptTemplate

travel_guide_description = """
Este sistema de Recuperación de Información Guiada por Inteligencia Artificial (RAG) proporciona información extensa sobre viajes en Bolivia.
Puedes realizar preguntas relacionadas con las principales ciudades, atracciones turísticas, actividades culturales, restaurantes, hoteles, 
y mucho más. Este sistema está diseñado para ayudarte a planificar itinerarios completos, ya sea para viajes cortos o largos, ofreciendo 
sugerencias personalizadas según las notas y preferencias del usuario. El sistema también puede proporcionar recomendaciones para reservas 
específicas, como vuelos, hoteles, buses y restaurantes, ajustándose a las necesidades del usuario.

Recuerda que puedes hacer preguntas específicas como:
- ¿Qué puedo visitar en La Paz si me gusta la historia y la cultura?
- ¿Cuáles son los mejores restaurantes en Cochabamba para comida tradicional?
- ¿Qué actividades de aventura hay en Santa Cruz?
"""

travel_guide_qa_str = """
Dada la siguiente información sobre un viaje a Bolivia: {notes},
por favor proporciona recomendaciones personalizadas sobre actividades turísticas, restaurantes y hoteles en {city}.

Los resultados deben basarse en las siguientes preferencias del usuario:
- Tipo de actividades que disfruta (culturales, de aventura, relajación, etc.)
- Tipo de comida/restaurantes que prefiere (local, internacional, vegetariano, etc.)
- Tipo de alojamiento que prefiere (lujo, económico, boutique, familiar, etc.)

Por favor, organiza las recomendaciones en las siguientes categorías:
1. **Actividades y lugares para visitar**: Proporcione al menos 3 recomendaciones relevantes para {city}.
2. **Restaurantes recomendados**: Incluye el tipo de comida, rango de precios, y recomendaciones especiales si aplica.
3. **Hoteles recomendados**: Proporcione opciones basadas en calidad, presupuesto y accesibilidad.

Asegúrate de que las recomendaciones sean claras y estén alineadas con las notas proporcionadas.
"""

agent_prompt_str = """
Eres un agente de inteligencia artificial especializado en la planificación de viajes en Bolivia. Tienes acceso a varias herramientas 
que pueden ofrecer recomendaciones sobre actividades turísticas, restaurantes, hoteles, y otros detalles relacionados con viajes. 
Tu tarea es utilizar estas herramientas para ayudar a los usuarios a planificar viajes completos, ya sea proporcionando información 
útil, sugiriendo reservas o creando itinerarios personalizados.

Tienes las siguientes capacidades:
- Consultar información turística relevante a través de una base de datos.
- Realizar recomendaciones personalizadas basadas en preferencias del usuario.
- Facilitar la reserva de vuelos, buses, hoteles y restaurantes.
- Crear reportes detallados de itinerarios y presupuestos basados en las reservas hechas.

Al interactuar con el usuario, asegúrate de hacer preguntas relevantes para obtener más detalles cuando sea necesario. Puedes ofrecer 
información precisa, recomendaciones claras y opciones adecuadas de reservas para mejorar la experiencia del usuario.
"""

travel_guide_qa_tpl = PromptTemplate(travel_guide_qa_str)
agent_prompt_tpl = PromptTemplate(agent_prompt_str)
