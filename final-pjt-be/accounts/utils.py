# 05.22, 02:05 Comment 유저 사진 필드 떄문에 파일 자체 추가
def get_user_profile_image(user):
    profile_image = getattr(user, 'profile_image', None)
    return profile_image.url if profile_image else None
