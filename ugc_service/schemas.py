from .exceptions import ValidationError

def validate_create_review(data):
    if not isinstance(data, dict):
        raise ValidationError({"body": "Ожидается JSON-объект"})

    movie_id = data.get("movie_id")
    if type(movie_id) is not int or movie_id < 1:
        raise ValidationError({"movie_id": "Ожидается целое число >= 1"})

    kind = data.get("kind")
    if kind not in {"review", "comment", "rating"}:
        raise ValidationError({"kind": "Ожидается review, comment или rating"})

    author = data.get("author")
    if not isinstance(author, str) or len(author.strip()) < 2:
        raise ValidationError({"author": "Обязательное поле, минимум 2 символа"})

    content = data.get("content")
    if content is not None:
        if not isinstance(content, str) or len(content.strip()) > 2000:
            raise ValidationError({"content": "Некорректный текст отзыва (макс 2000 символов)"})
        content = content.strip()

    rating = data.get("rating")
    if rating is not None:
        if type(rating) is not int or not (1 <= rating <= 5):
            raise ValidationError({"rating": "Ожидается целое число от 1 до 5"})

    if kind in {"review", "comment"} and not content:
        raise ValidationError({"content": "Для review и comment нужен текст"})

    if kind == "rating" and rating is None:
        raise ValidationError({"rating": "Для rating нужна оценка"})

    return {
        "movie_id": movie_id,
        "kind": kind,
        "author": author.strip(),
        "content": content,
        "rating": rating,
    }


def validate_update_status(data):
    if not isinstance(data, dict):
        raise ValidationError({"body": "Ожидается JSON-объект"})

    status = data.get("status")
    if status not in {"active", "hidden", "pending"}:
        raise ValidationError({"status": "Недопустимый статус"})

    note = data.get("moderation_note")
    if note is not None:
        if not isinstance(note, str) or len(note.strip()) > 500:
            raise ValidationError({"moderation_note": "Некорректная заметка (макс 500 символов)"})
        note = note.strip()

    return {"status": status, "moderation_note": note}
