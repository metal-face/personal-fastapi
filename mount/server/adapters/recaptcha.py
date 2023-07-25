from server.utils import settings
from server.utils import services


async def verify_recaptcha(recaptcha_token: str) -> bool:
    res = await services.http_client.post(
        "https://www.google.com/recaptcha/api/siteverify",
        data={"secret": settings.RECAPTCHA_SECRET_KEY, "response": recaptcha_token},
    )
    res.raise_for_status()

    res_data = res.json()
    if not isinstance(res_data, dict):
        raise ValueError("Invalid response from recaptcha")

    return res_data.get("success", False)
