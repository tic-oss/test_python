from fastapi import APIRouter

router = APIRouter(
    prefix='/api'
)


@router.get("/management/health/liveness")
async def health_check():
    return {
        "status": "UP",
        "components": {
            "livenessState": {
                "status": "UP"
            }
        }
    }

@router.get("/management/health/readiness")
async def health_check():
    return {
        "status": "UP",
        "components": {
            "readinessState": {
                "status": "UP"
            }
        }
    }