from fastapi import Request
import asyncio


async def get_product_type_lock(request: Request) -> asyncio.Lock:
    return request.app.state.product_type_lock
