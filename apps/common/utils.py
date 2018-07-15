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

gender_choice = (('F','남성'),('M','여성'))

def get_image_filename(instance, filename):
    contents = instance.contents.id
    slug = slugify(contents)
    return "contents_images/%s/%s" % (slug, filename)  