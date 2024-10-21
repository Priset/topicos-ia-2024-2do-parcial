from fastapi import FastAPI, Depends, Query
from llama_index.core.agent import ReActAgent
from ai_assistant.agent import TravelAgent
from ai_assistant.models import AgentAPIResponse
from ai_assistant.tools import (
    reserve_bus,
    reserve_hotel,
    reserve_restaurant,
)
import json
from ai_assistant.config import get_agent_settings

SETTINGS = get_agent_settings()

def get_agent() -> ReActAgent:
    return TravelAgent().get_agent()


app = FastAPI(title="AI Agent")


@app.get("/recommendations/cities")
def recommend_cities(
    notes: list[str] = Query(...), agent: ReActAgent = Depends(get_agent)
):
    prompt = f"recommend cities in bolivia with the following notes: {notes}"
    return AgentAPIResponse(status="OK", agent_response=str(agent.chat(prompt)))

@app.get("/recommendations/hotels")
def recommend_hotels(city: str, notes: list[str] = Query(default=None), agent: ReActAgent = Depends(get_agent)):
    prompt = f"Recommend hotels in {city} with the following notes: {notes}"
    return AgentAPIResponse(status="OK", agent_response=str(agent.chat(prompt)))


@app.get("/recommendations/activities")
def recommend_activities(city: str, notes: list[str] = Query(default=None), agent: ReActAgent = Depends(get_agent)):
    prompt = f"Recommend activities in {city} with the following notes: {notes}"
    return AgentAPIResponse(status="OK", agent_response=str(agent.chat(prompt)))


@app.post("/reserve/bus")
def reserve_bus_endpoint(departure: str, destination: str, date: str):
    reservation = reserve_bus(date, departure, destination)
    return reservation


@app.post("/reserve/hotel")
def reserve_hotel_endpoint(checkin_date: str, checkout_date: str, hotel_name: str, city: str):
    reservation = reserve_hotel(checkin_date, checkout_date, hotel_name, city)
    return reservation


@app.post("/reserve/restaurant")
def reserve_restaurant_endpoint(date_time: str, restaurant: str, city: str, dish: str = "not specified"):
    reservation = reserve_restaurant(date_time, restaurant, city, dish)
    return reservation


@app.get("/trip_summary")
def trip_summary():
    with open(SETTINGS.log_file, "r") as file:
        reservations = json.load(file)
    total_cost = sum([reservation.get("cost", 0) for reservation in reservations])
    summary = {
        "reservations": reservations,
        "total_cost": total_cost,
        "message": f"Tu viaje tiene un costo total de {total_cost} USD.",
    }
    return summary