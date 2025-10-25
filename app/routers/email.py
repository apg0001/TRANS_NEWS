from fastapi import APIRouter, HTTPException
from ..schemas.models import EmailRequest
from ..services.email_service import EmailService

router = APIRouter()
email_service = EmailService()


@router.post("/email/send")
async def send_email(request: EmailRequest):
    """
    기사 정보를 이메일로 전송
    """
    if not email_service.is_configured():
        raise HTTPException(
            status_code=503, 
            detail="이메일 서비스가 설정되지 않았습니다. 관리자에게 문의하세요."
        )
    
    try:
        success = email_service.send_article_email(request.dict())
        
        if success:
            return {"message": "이메일이 성공적으로 전송되었습니다."}
        else:
            raise HTTPException(status_code=500, detail="이메일 전송에 실패했습니다.")
            
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"이메일 전송 중 오류가 발생했습니다: {str(e)}")
