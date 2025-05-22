import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.files.base import ContentFile
from faker import Faker
from apps.registration.models import Customer
from apps.property.models import Property,Category


import os
import random
from django.core.files import File

fake = Faker()

class Command(BaseCommand):
    help = 'Seed users, customers, categories, and properties'


    def update_property_images_same(self):
        image_dir = os.path.join(os.path.dirname(__file__), 'property')  # 'property' folder in same dir
        image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

        if not image_files:
            print("No images found in 'property' folder.")
            return

        properties = Property.objects.all()

        for i, prop in enumerate(properties):
            image_filename = image_files[i % len(image_files)]
            image_path = os.path.join(image_dir, image_filename)

            with open(image_path, 'rb') as img_file:
                prop.image.save(f'property_image_{prop.id}.jpg', File(img_file), save=False)
                img_file.seek(0)  # reset pointer for thumbnail
                prop.thumbnail.save(f'property_thumb_{prop.id}.jpg', File(img_file), save=True)

            print(f"Updated property ID {prop.id} with image: {image_filename}")

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding database...")

        # Create Users and Customers
        # users = []
        # for i in range(3):
        #     username = f'user{i+1}'
        #     user = User.objects.create_user(username=username, email=fake.email(),password='@kaSrv11')
        #     customer = Customer.objects.create(
        #         name=fake.name(),
        #         is_email_verified=True,
        #         created_by=user
        #     )
        #     users.append(customer)
        #     self.stdout.write(self.style.SUCCESS(f"Created user and customer: {username}"))

        # # Create Categories
        # categories = []
        # for i, cat_title in enumerate(['house', 'apartment', 'flat']):
        #     category, _ = Category.objects.get_or_create(
        #         title=cat_title,
        #         slug=slugify(cat_title),
        #         ordering=i
        #     )
        #     categories.append(category)
        #     self.stdout.write(self.style.SUCCESS(f"Created category: {cat_title}"))

        # # Create Properties
        # for i in range(10):
        #     title = fake.address()
        #     prop = Property.objects.create(
        #         title=title,
        #         slug=slugify(title),
        #         description=fake.text(),
        #         latitude=fake.latitude(),
        #         longitude=fake.longitude(),
        #         price=round(random.uniform(10000, 50000), 2),
        #         customer=random.choice(users),
        #         category=random.choice(categories),
        #     )

        #     self.stdout.write(self.style.SUCCESS(f"Created property: {prop.title}"))

        self.update_property_images_same()

        self.stdout.write(self.style.SUCCESS("✅ Database seeded successfully!"))
