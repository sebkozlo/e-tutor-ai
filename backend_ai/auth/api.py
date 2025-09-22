from ninja import Router


router = Router()


@router.get("/me", tags=["Auth"])
def secure_endpoint(request):
    return request.auth
