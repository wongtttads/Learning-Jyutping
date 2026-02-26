import json

def handler(event, context):
    """Netlify函数处理粤语发音请求"""
    
    # 解析请求
    path = event.get('path', '')
    http_method = event.get('httpMethod', 'GET')
    
    # 处理不同的API端点
    if path == '/api/health' and http_method == 'GET':
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'status': 'ok',
                'service': 'Cantonese TTS Server (Netlify Functions)',
                'supported': False,
                'use_web_speech': True,
                'message': '请使用浏览器原生的Web Speech API进行发音'
            })
        }
    
    elif path == '/api/speak' and http_method == 'POST':
        try:
            body = json.loads(event.get('body', '{}'))
            text = body.get('text', '')
            
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'success': False,
                    'error': '服务器不支持粤语发音',
                    'web_speech_mode': True,
                    'message': '请使用浏览器原生的Web Speech API',
                    'text': text
                })
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'success': False,
                    'error': str(e)
                })
            }
    
    elif path == '/api/stop' and http_method == 'POST':
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'success': True,
                'message': '已停止'
            })
        }
    
    elif path == '/api/status' and http_method == 'GET':
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'is_speaking': False,
                'supported': False,
                'use_web_speech': True,
                'platform': 'netlify_function'
            })
        }
    
    else:
        return {
            'statusCode': 404,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': 'API端点不存在'
            })
        }