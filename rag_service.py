import os
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from google.generativeai import embed_content

os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")

def get_embedding(text_content: str) -> list[float]:
    """
    Generates 768-dimensional embeddings asynchronously using Gemini.
    """
    response = embed_content(
        model="models/embedding-001",
        contents=text_content,
        task_type="retrieval_document"
    )
    return response['embedding']

async def retrieve_similar_apps(query: str, db: AsyncSession, limit: int = 3):
    """
    Asynchronous Vector Search using pgvector cosine distance (<=>).
    """
    query_vector = get_embedding(query)
    
    sql = text("""
        SELECT name, category, replaces, description, github_url 
        FROM freeware_apps 
        ORDER BY description_vector <=> :query_vector::vector 
        LIMIT :limit
    """)
    
    result = await db.execute(sql, {"query_vector": str(query_vector), "limit": limit})
    apps = result.fetchall()
    
    context_str = ""
    for app in apps:
        context_str += (
            f"- Name: {app.name}\n"
            f"  Category: {app.category}\n"
            f"  Replaces: {app.replaces}\n"
            f"  Description: {app.description}\n"
            f"  GitHub: {app.github_url}\n\n"
        )
        
    return context_str if context_str else "No local open-source alternatives found in database."