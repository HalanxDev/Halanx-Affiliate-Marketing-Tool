from django.template.defaultfilters import slugify

from utility.random_utils import generate_random_code


def create_slug(text, used_slugs):
    slug = None
    suffix = 0
    potential = base = slugify(text[:90])
    while not slug:
        if suffix:
            potential = "{}-{}".format(base, suffix)
        if potential not in used_slugs:
            slug = potential
        suffix += 1
    return slug


def get_topic_image_upload_path(instance, filename):
    return "faqs/topics/{}/{}-{}".format(instance.slug, generate_random_code(n=5), filename.split('/')[-1])
