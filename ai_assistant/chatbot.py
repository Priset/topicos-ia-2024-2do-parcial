import gradio as gr
from ai_assistant.agent import TravelAgent
from ai_assistant.tools import (
    reserve_flight,
    reserve_bus,
    reserve_hotel,
    reserve_restaurant
)

agent = TravelAgent().get_agent()


def agent_response(message, history):
    # Verificar si el mensaje es sobre una reserva de vuelo
    if "reservar vuelo" in message.lower():
        # Aquí puedes ajustar los parámetros de acuerdo a la interacción real
        flight_reservation = reserve_flight("2023-12-01", "La Paz", "Santa Cruz")
        return f"Reservación de vuelo completada: {flight_reservation}"

    # Verificar si el mensaje es sobre una reserva de bus
    if "reservar bus" in message.lower():
        bus_reservation = reserve_bus("2023-12-05", "Cochabamba", "Sucre")
        return f"Reservación de bus completada: {bus_reservation}"

    # Verificar si el mensaje es sobre una reserva de hotel
    if "reservar hotel" in message.lower():
        hotel_reservation = reserve_hotel("2023-12-01", "2023-12-05", "Hotel Sol", "Santa Cruz")
        return f"Reservación de hotel completada: {hotel_reservation}"

    # Verificar si el mensaje es sobre una reserva de restaurante
    if "reservar restaurante" in message.lower():
        restaurant_reservation = reserve_restaurant("2023-12-07T20:00", "Gustu", "La Paz")
        return f"Reservación de restaurante completada: {restaurant_reservation}"

    # Si no es una reserva, seguir con la lógica del agente AI
    return agent.chat(message).response


if __name__ == "__main__":
    demo = gr.ChatInterface(agent_response, type="messages")
    demo.launch()
