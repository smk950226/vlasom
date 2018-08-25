from django.utils import timezone

NOW_YEAR = timezone.now().strftime("%Y")

birth_year_list = []
for i in range(100):
    birth_year_list.append(tuple((int(NOW_YEAR) - i, str(int(NOW_YEAR)-i)+'년')))
birth_year = tuple(birth_year_list)

birth_month_list = []
for i in range(12):
    birth_month_list.append(tuple((i+1, str(i+1)+'월')))
birth_month = tuple(birth_month_list)

birth_day_list = []
for i in range(31):
    birth_day_list.append(tuple((i+1, str(i+1)+'일')))
birth_day = tuple(birth_day_list)

gender_choice = (('M','남성'),('F','여성'))

join_channel = (('WEB', 'WEB'),('KAKAO', 'KAKAO'),('FACEBOOK','FACEBOOK'),('GOOGLE','GOOGLE'))

def get_image_filename(instance, filename):
    return '/'.join([instance.category_1.name, instance.user.nickname, filename])

def get_image_filename2(instance, filename):
    return '/'.join([instance.contents.category_1.name, instance.user.nickname, filename])

def profile_image_upload_to(instance, filename):
    return '/'.join(['profile', instance.nickname, filename])