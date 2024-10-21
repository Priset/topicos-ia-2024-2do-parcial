import json
from random import randint
from datetime import date, datetime
from llama_index.core.tools import QueryEngineTool, FunctionTool, ToolMetadata
from ai_assistant.rags import TravelGuideRAG
from ai_assistant.prompts import travel_guide_qa_tpl, travel_guide_description
from ai_assistant.config import get_agent_settings
from ai_assistant.models import (
    TripReservation,
    TripType,
    HotelReservation,
    RestaurantReservation,
)
from ai_assistant.utils import save_reservation

SETTINGS = get_agent_settings()

travel_guide_tool = QueryEngineTool(
    query_engine=TravelGuideRAG(
        store_path=SETTINGS.travel_guide_store_path,
        data_dir=SETTINGS.travel_guide_data_path,
        qa_prompt_tpl=travel_guide_qa_tpl,
    ).get_query_engine(),
    metadata=ToolMetadata(
        name="travel_guide", description=travel_guide_description, return_direct=False
    ),
)


# Tool functions
def reserve_flight(date_str: str, departure: str, destination: str) -> TripReservation:
    """
    ===> COMPLETE DESCRIPTION HERE <===
    """
    print(
        f"Making flight reservation from {departure} to {destination} on date: {date}"
    )
    reservation = TripReservation(
        trip_type=TripType.flight,
        departure=departure,
        destination=destination,
        date=date.fromisoformat(date_str),
        cost=randint(200, 700),
    )

    save_reservation(reservation)
    return reservation


flight_tool = FunctionTool.from_defaults(fn=reserve_flight, return_direct=False)

def reserve_bus(date_str: str, departure: str, destination: str) -> TripReservation:
    """
    Reserva un ticket de bus para una fecha específica.
    """
    print(f"Making bus reservation from {departure} to {destination} on date: {date_str}")
    reservation = TripReservation(
        trip_type=TripType.bus,
        departure=departure,
        destination=destination,
        date=date.fromisoformat(date_str),
        cost=randint(50, 300),
    )

    save_reservation(reservation)
    return reservation


bus_tool = FunctionTool.from_defaults(fn=reserve_bus, return_direct=False)


def reserve_hotel(checkin_date: str, checkout_date: str, hotel_name: str, city: str) -> HotelReservation:
    """
    Reserva un cuarto de hotel dado el hotel, ciudad y las fechas.
    """
    print(f"Making hotel reservation at {hotel_name} in {city} from {checkin_date} to {checkout_date}")
    reservation = HotelReservation(
        checkin_date=date.fromisoformat(checkin_date),
        checkout_date=date.fromisoformat(checkout_date),
        hotel_name=hotel_name,
        city=city,
        cost=randint(500, 1500),
    )

    save_reservation(reservation)
    return reservation


hotel_tool = FunctionTool.from_defaults(fn=reserve_hotel, return_direct=False)


def reserve_restaurant(date_time: str, restaurant: str, city: str, dish: str = "not specified") -> RestaurantReservation:
    """
    Reserva una mesa en un restaurante específico para una fecha y hora.
    """
    reservation_time = datetime.fromisoformat(date_time)
    print(f"Making restaurant reservation at {restaurant} in {city} on {reservation_time}")
    reservation = RestaurantReservation(
        reservation_time=reservation_time,
        restaurant=restaurant,
        city=city,
        dish=dish,
        cost=randint(20, 100),
    )

    save_reservation(reservation)
    return reservation


restaurant_tool = FunctionTool.from_defaults(fn=reserve_restaurant, return_direct=False)


# Tool para generar el resumen del viaje
def generate_trip_summary() -> str:
    """
    Genera un reporte detallado del viaje basado en el archivo de registro 'trip.json'.
    Incluye las reservas organizadas por lugar y fecha, un resumen del presupuesto total,
    y comentarios sobre las actividades y lugares reservados.
    """
    try:
        with open(SETTINGS.log_file, "r") as file:
            reservations = json.load(file)

        if not reservations:
            return "No se encontraron reservas en el archivo de log de viajes."

        # Resumen de reservas
        summary = ""
        total_cost = 0

        for reservation in reservations:
            reservation_type = reservation.get("reservation_type", "Desconocido")
            summary += f"\nTipo de Reserva: {reservation_type}\n"
            for key, value in reservation.items():
                if key != "reservation_type":
                    summary += f"{key.capitalize()}: {value}\n"
            total_cost += reservation.get("cost", 0)
            summary += "\n--------------------\n"

        summary += f"\nEl costo total del viaje es: {total_cost} USD.\n"
        return summary

    except FileNotFoundError:
        return "No se encontró el archivo de log de viajes."

trip_summary_tool = FunctionTool(
    fn=generate_trip_summary,
    metadata=ToolMetadata(
        name="trip_summary_tool",
        description="Genera un resumen del viaje basado en las reservas realizadas en el archivo de log.",
        return_direct=True
    )
)