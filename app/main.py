from fastapi import (
    FastAPI,
    BackgroundTasks,
    UploadFile,
    File,
    Query,
    HTTPException,
    Form,
)
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
from app.database import engine, init_db, SessionLocal
from app.models import ModerationRequest, ModerationResult
from app.schemas import (
    ModerateTextRequest,
    ModerateTextResponse,
    ModerateImageResponse,
    AnalyticsSummaryResponse,
)
from app.moderation import moderate_text_sightengine, moderate_image_sightengine
from app.notifications import send_email_notification
from sqlalchemy import func, select


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Smart Content Moderator API", lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")


def save_moderation_result(session, user_email: str, content_type: str, content_hash: str, moderation_result: dict):
    m_request = ModerationRequest(
        user_email=user_email,
        content_type=content_type,
        content_hash=content_hash,
        status="processed",
    )
    session.add(m_request)
    session.commit()
    session.refresh(m_request)

    m_result = ModerationResult(
        request_id=m_request.id,
        classification=moderation_result["classification"],
        confidence=moderation_result["confidence"],
        reasoning=moderation_result["reasoning"],
        llm_response=moderation_result.get("llm_response", ""),
    )
    session.add(m_result)
    session.commit()

    return m_request.id


def notify_if_flagged(background_tasks: BackgroundTasks, request_id: int, classification: str, reasoning: str, user_email: str):
    if classification != "safe":
        message = (
            f"Moderation Alert!\n"
            f"Request ID: {request_id}\n"
            f"Classification: {classification}\n"
            f"Reason: {reasoning}"
        )
        background_tasks.add_task(
            send_email_notification, request_id, user_email, "Content Moderation Alert", message
        )


@app.post("/api/v1/moderate/text", response_model=ModerateTextResponse)
async def moderate_text(payload: ModerateTextRequest, background_tasks: BackgroundTasks):
    try:
        moderation_result = moderate_text_sightengine(payload.text)

        with SessionLocal() as session:
            request_id = save_moderation_result(
                session,
                payload.email,
                "text",
                str(hash(payload.text)),
                moderation_result,
            )

        notify_if_flagged(
            background_tasks, request_id, moderation_result["classification"], moderation_result["reasoning"], payload.email
        )

        return ModerateTextResponse(
            classification=moderation_result["classification"],
            confidence=moderation_result["confidence"],
            reasoning=moderation_result["reasoning"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Moderation failed: {str(e)}")


@app.post("/api/v1/moderate/image", response_model=ModerateImageResponse)
async def moderate_image(
    background_tasks: BackgroundTasks,
    email: str = Form(...),
    file: UploadFile = File(...)
):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    image_data = await file.read()
    if len(image_data) > 5 * 1024 * 1024:  # 5MB limit
        raise HTTPException(status_code=400, detail="File too large")

    try:
        moderation_result = moderate_image_sightengine(image_data)

        with SessionLocal() as session:
            request_id = save_moderation_result(
                session,
                email,
                "image",
                str(hash(image_data)),
                moderation_result,
            )

        notify_if_flagged(
            background_tasks, request_id, moderation_result["classification"], moderation_result["reasoning"], email
        )

        return ModerateImageResponse(
            classification=moderation_result["classification"],
            confidence=moderation_result["confidence"],
            reasoning=moderation_result["reasoning"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image moderation failed: {str(e)}")


@app.get("/api/v1/analytics/summary", response_model=AnalyticsSummaryResponse)
async def analytics_summary(user: str = Query(...)):
    try:
        with SessionLocal() as session:
            total_requests = session.exec(
                select(func.count())
                .select_from(ModerationRequest)
                .where(ModerationRequest.user_email == user)
            ).scalar_one()

            classification_counts_query = session.exec(
                select(ModerationResult.classification, func.count())
                .join(ModerationRequest, ModerationResult.request_id == ModerationRequest.id)
                .where(ModerationRequest.user_email == user)
                .group_by(ModerationResult.classification)
            ).all()

            classification_counts = {classification: count for classification, count in classification_counts_query}

            last_request_at = session.exec(
                select(func.max(ModerationRequest.created_at)).where(ModerationRequest.user_email == user)
            ).scalar_one()

        return AnalyticsSummaryResponse(
            email=user,
            total_requests=total_requests,
            classification_counts=classification_counts,
            last_request_at=last_request_at,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch analytics summary: {str(e)}")


@app.get("/")
def root_redirect():
    return RedirectResponse(url="/static/index.html")
