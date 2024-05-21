import logging
from django.http import HttpResponse
from moviepy.editor import TextClip, CompositeVideoClip, ColorClip
from .models import VideoRequest   

# Настройка логгера
logger = logging.getLogger(__name__)

def generate_video(request):
    text = request.GET.get('text', '')  # Получаем текст из параметров запроса
    output_path = "output.mp4"  # Определяем путь для выходного файла
    max_duration = 3
    fps = 60
    bg_color = (255, 192, 203)
    text_color = 'white'
    font_size = 60
    default_speed = 800

    try:
        # Ваш код для генерации видео
        screen_width, screen_height = 100, 100
        text_clip = TextClip(text, fontsize=font_size, color=text_color, font='Amiri-Bold', size=(None, screen_height))
        text_length = text_clip.size[0]
        normal_duration = (text_length + screen_width) / default_speed
        if normal_duration > max_duration:
            text_speed = (text_length + screen_width) / max_duration
            duration = max_duration
        else:
            text_speed = default_speed
            duration = normal_duration
        def scroll_text(t):
            text_x = screen_width - text_speed * t
            return (text_x, 'center')
        background_clip = ColorClip(size=(screen_width, screen_height), color=bg_color, duration=duration)
        video = CompositeVideoClip([background_clip, text_clip.set_position(scroll_text).set_duration(duration)], size=(screen_width, screen_height))
        video = video.set_fps(fps)
        video.write_videofile(output_path, codec='libx264')
        
        video_request = VideoRequest.objects.create(text=text)

        # Логирование успешного завершения
        logger.info("Video successfully generated.")

        # Возвращаем видеофайл в ответе
        with open(output_path, 'rb') as video_file:
            response = HttpResponse(video_file.read(), content_type='video/mp4')
            response['Content-Disposition'] = 'attachment; filename="output.mp4"'
        return response
    except Exception as e:
        logger.error(f"Error generating video: {e}")
        return HttpResponse(f"Error generating video.{e}", status=500)
        with open(output_path, 'rb') as video_file:
            response = HttpResponse(video_file.read(), content_type='video/mp4')
            response['Content-Disposition'] = 'attachment; filename="output.mp4"'
        return response
    except Exception as e:
        # Логирование ошибки
        logger.error(f"Error generating video: {e}")
        # Возвращаем ошибку в ответе
        return HttpResponse("Error generating video.", status=500)
