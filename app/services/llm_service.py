import re
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from app.schemas.place import PlaceOut
from app.schemas.chat import AIPlaceResult, ChatResponse
from app.utils.prompts import GENERAL_CHAT, FEW_SHOT_SEARCH, COT_RECOMMEND, GENERAL_KNOWLEDGE
from app.config import settings


_GREETINGS = re.compile(
    r"^(hi|hello|hey|good\s*(morning|afternoon|evening)|howdy|yo|sup|hiya|"
    r"how\s*are\s*you|what's\s*up|whassup|hows?\s*it\s*going|"
    r"nice\s*to\s*meet\s*you|thanks|thank\s*you|thx)$",
    re.IGNORECASE,
)


def _is_greeting(text: str) -> bool:
    return bool(_GREETINGS.match(text.strip().rstrip(".!?")))


def _build_llm():
    if not settings.groq_api_key:
        return None
    return ChatGroq(
        model=settings.llm_model,
        api_key=settings.groq_api_key,
        temperature=0.3,
    )


async def _call_llm(system: str, human: str, history: list | None = None, **kwargs) -> str | None:
    llm = _build_llm()
    if not llm:
        return None
    try:
        messages = [("system", system)]
        if history:
            for msg in history:
                messages.append((msg.role, msg.content))
        messages.append(("human", human))
        prompt = ChatPromptTemplate.from_messages(messages)
        chain = prompt | llm
        response = await chain.ainvoke(kwargs if kwargs else {})
        return response.content
    except Exception as e:
        print(f"LLM call failed: {e}")
        return None


async def _chat_general(query: str, history: list | None = None) -> ChatResponse:
    answer = await _call_llm(GENERAL_CHAT, "{query}", history=history, query=query)
    if not answer:
        answer = "Hi! I'm WayGems AI. Ask me about places to visit in Baku!"
    return ChatResponse(answer=answer, matches=[])


async def _knowledge_response(query: str, history: list | None = None) -> ChatResponse:
    answer = await _call_llm(GENERAL_KNOWLEDGE, "{query}", history=history, query=query)
    if not answer:
        answer = (
            "I don't have specific places in my database for that yet, but Baku has "
            "amazing spots like İçərişəhər (Old City), the Maiden Tower, Baku Boulevard, "
            "and the Heydar Aliyev Center. Try asking about a specific category!"
        )
    return ChatResponse(answer=answer, matches=[])


def _offline_response(query: str, places: list[PlaceOut]) -> ChatResponse:
    if not places:
        return ChatResponse(
            answer="I don't have specific places stored yet, but Baku has many great spots! Try asking about cafes, historical sites, or restaurants.",
            matches=[],
        )
    matches = [
        AIPlaceResult(place=p, confidence=0.5, reasoning="")
        for p in places[:5]
    ]
    place_names = ", ".join(p.name for p in places[:5])
    return ChatResponse(
        answer=f"Here are some places that might match: {place_names}.",
        matches=matches,
    )


async def _ai_response(prompt_template: str, query: str, places: list[PlaceOut], top_k: int, history: list | None = None) -> ChatResponse:
    if not places:
        return await _knowledge_response(query, history=history)

    llm = _build_llm()
    if not llm:
        return _offline_response(query, places)

    try:
        places_text = "\n".join(
            f"- {p.name}: {p.description} (rating: {p.rating}, address: {p.address})"
            for p in places[:top_k]
        )
        answer = await _call_llm(
            prompt_template,
            "User query: {query}\n\nDatabase results:\n{places}",
            history=history,
            query=query,
            places=places_text,
        )
        if not answer:
            return _offline_response(query, places)

        matches = [
            AIPlaceResult(place=p, confidence=0.5, reasoning="")
            for p in places[:3]
        ]
        return ChatResponse(answer=answer, matches=matches)
    except Exception as e:
        print(f"AI search failed: {e}")
        return _offline_response(query, places)


async def search_places_ai(query: str, places: list[PlaceOut], top_k: int = 5, history: list | None = None) -> ChatResponse:
    if _is_greeting(query):
        return await _chat_general(query, history=history)
    return await _ai_response(FEW_SHOT_SEARCH, query, places, top_k, history=history)


async def recommend_places_ai(query: str, places: list[PlaceOut], top_k: int = 5, history: list | None = None) -> ChatResponse:
    if _is_greeting(query):
        return await _chat_general(query, history=history)
    return await _ai_response(COT_RECOMMEND, query, places, top_k, history=history)
