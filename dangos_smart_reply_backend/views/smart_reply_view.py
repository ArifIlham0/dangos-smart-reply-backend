from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from ..middlewares.authentications import BearerTokenAuthentication
from ..middlewares.permissions import IsSuperUser
from ..serializers import SmartReplySerializer
from ..services.detector import detect_platform
from ..services.fetcher import fetch_html
from ..services.parsers.base import get_parser
from ..services.normalizer import normalize_tasks
from ..services.prompt_builder import build_prompt
from ..llm.claude_client import ask_claude
    
@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def smart_reply(request):
    try:
        serializer = SmartReplySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        url = serializer.validated_data["url"]
        question = serializer.validated_data["question"]

        platform = detect_platform(url)
        html = fetch_html(url)
        try:
            import subprocess
            subprocess.run(['pbcopy'], input=html.encode('utf-8'), check=True)
            print("HTML copied to clipboard")
        except Exception as exc:
            print("Failed to copy HTML to clipboard:", exc)

        print("Fetched HTML:", html[:500])

        parser = get_parser(platform)
        raw_tasks = parser.parse(html)
        print("Extracted Raw Tasks:", raw_tasks)

        tasks = normalize_tasks(raw_tasks)

        prompt = build_prompt(tasks, question)
        print("Generated Prompt:", prompt)
        answer = ask_claude(prompt)

        return Response({
            "status": status.HTTP_200_OK,
            "message": "Smart reply generated successfully",
            "data": answer,
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)