import uvicorn
import os


if __name__ == '__main__':
    uvicorn.run(
        'app:app', 
        host=os.environ['WEB_API_HOST'], 
        port=int(os.environ['WEB_API_PORT']),
        log_level=os.environ['WEB_API_LOG_LEVEL'],
        proxy_headers=True, 
        reload=True
    )