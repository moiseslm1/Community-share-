import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker

fake = Faker()

CATEGORIES = [
    'assembly', 'mounting', 'cleaning',
    'outdoor-maintenance', 'repairs', 'moving', 'cooking',
]

SERVICE_TEMPLATES = {
    'assembly': [
        ("IKEA Furniture Assembly", "I assemble IKEA and flat-pack furniture quickly and correctly."),
        ("Desk & Shelf Setup", "Office desks, bookshelves, and storage units assembled to spec."),
        ("Crib & Baby Furniture", "Safe, careful assembly of cribs, changing tables, and nursery furniture."),
    ],
    'mounting': [
        ("TV Wall Mounting", "I mount TVs of any size, hide cables, and level perfectly."),
        ("Picture & Mirror Hanging", "Gallery walls, heavy mirrors, and single frames hung straight."),
        ("Floating Shelf Installation", "Custom floating shelves measured, levelled, and anchored properly."),
    ],
    'cleaning': [
        ("Deep Home Cleaning", "Full top-to-bottom deep clean — kitchens, bathrooms, floors included."),
        ("Move-Out Cleaning", "Thorough cleaning so you get your deposit back."),
        ("Weekly Maintenance Clean", "Regular light cleaning to keep your home tidy and fresh."),
    ],
    'outdoor-maintenance': [
        ("Lawn Mowing & Edging", "Reliable weekly or bi-weekly lawn care with a clean finish."),
        ("Garden Weeding & Planting", "Weed removal, soil prep, and seasonal planting."),
        ("Leaf Blowing & Yard Cleanup", "Post-season cleanup — leaves, debris, and general tidying."),
    ],
    'repairs': [
        ("General Home Repairs", "Patching drywall, fixing leaky faucets, replacing fixtures."),
        ("Door & Window Fixes", "Sticking doors, broken locks, drafty windows — all sorted."),
        ("Appliance Troubleshooting", "Diagnosis and minor repairs on washers, dryers, and dishwashers."),
    ],
    'moving': [
        ("Local Moving Help", "Strong, reliable help loading and unloading your moving truck."),
        ("Furniture Rearranging", "Heavy lifting and room rearranging — no truck needed."),
        ("Junk Removal & Hauling", "Clearing out old furniture, appliances, and clutter."),
    ],
    'cooking': [
        ("Weekly Meal Prep", "Batch-cook healthy meals for the week so you're always covered."),
        ("Private Chef for Events", "Home-cooked dinner parties and small gatherings catered."),
        ("Cultural & Specialty Meals", "Authentic home-cooked dishes from various cuisines."),
    ],
}

LA_ZIPS = [
    '90001','90011','90020','90025','90034',
    '90041','90056','90064','90071','90210',
    '90230','90245','90266','90272','90290',
    '90401','90405','90501','90601','90630',
    '91001','91030','91101','91201','91301',
    '91401','91501','91601','91701','91801',
]

LA_COORDS = {
    '90001': (33.9731, -118.2479), '90011': (33.9994, -118.2717),
    '90020': (34.0658, -118.3089), '90025': (34.0447, -118.4432),
    '90034': (34.0170, -118.3986), '90041': (34.1397, -118.2072),
    '90056': (33.9886, -118.3644), '90064': (34.0325, -118.4197),
    '90071': (34.0522, -118.2527), '90210': (34.0901, -118.4065),
    '90230': (33.9986, -118.3920), '90245': (33.9164, -118.4016),
    '90266': (33.8867, -118.3964), '90272': (34.0440, -118.5255),
    '90290': (34.0965, -118.5839), '90401': (34.0195, -118.4912),
    '90405': (34.0069, -118.4780), '90501': (33.8344, -118.3148),
    '90601': (33.9628, -118.0331), '90630': (33.8148, -118.0370),
    '91001': (34.1486, -118.1073), '91030': (34.1025, -118.1089),
    '91101': (34.1478, -118.1445), '91201': (34.1625, -118.2592),
    '91301': (34.1561, -118.7192), '91401': (34.1819, -118.4013),
    '91501': (34.1858, -118.3089), '91601': (34.1697, -118.3764),
    '91701': (34.1064, -117.5931), '91801': (34.1486, -118.1277),
}

PHONE_AREA_CODES = ['213', '310', '323', '424', '562', '626', '747', '818']


def random_phone():
    area = random.choice(PHONE_AREA_CODES)
    return f"({area}) {random.randint(200,999)}-{random.randint(1000,9999)}"


def get_or_create_users(n=10):
    """Return n seeded users, creating them if they don't exist."""
    users = []
    for i in range(1, n + 1):
        username = f"neighbor{i}"
        user, _ = User.objects.get_or_create(
            username=username,
            defaults={
                'email': f"{username}@example.com",
                'first_name': fake.first_name(),
                'last_name': fake.last_name(),
            }
        )
        if not user.has_usable_password():
            user.set_password("Password123!")
            user.save()
        users.append(user)
    return users


class Command(BaseCommand):
    help = "Seed the database with fake services, requests, and job history."

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help='Clear existing seed data first')
        parser.add_argument('--services', type=int, default=40)
        parser.add_argument('--requests', type=int, default=20)
        parser.add_argument('--jobs', type=int, default=10)

    def handle(self, *args, **options):
        # Import here so the command file can live outside the app during setup
        from core.models import Service, ServiceRequest, UserJobHistory

        if options['clear']:
            Service.objects.filter(posted_by__username__startswith='neighbor').delete()
            ServiceRequest.objects.filter(posted_by__username__startswith='neighbor').delete()
            UserJobHistory.objects.filter(user__username__startswith='neighbor').delete()
            self.stdout.write(self.style.WARNING("Cleared existing seed data."))

        users = get_or_create_users(10)
        self.stdout.write(f"Using {len(users)} seed users.")

        #Services
        for _ in range(options['services']):
            cat = random.choice(CATEGORIES)
            title, desc = random.choice(SERVICE_TEMPLATES[cat])
            zip_code = random.choice(LA_ZIPS)
            lat, lng = LA_COORDS.get(zip_code, (34.0522, -118.2437))
            jitter = lambda: random.uniform(-0.015, 0.015)

            Service.objects.create(
                title=title,
                description=desc + " " + fake.sentence(),
                category=cat,
                address=fake.street_address() + f", Los Angeles, CA",
                zip_code=zip_code,
                phone_number=random_phone() if random.random() > 0.3 else '',
                latitude=lat + jitter(),
                longitude=lng + jitter(),
                posted_by=random.choice(users),
            )

        self.stdout.write(self.style.SUCCESS(f"Created {options['services']} services."))

        #Service Requests
        REQUEST_TITLES = [
            "Need help assembling new bed frame",
            "Looking for weekly lawn mowing",
            "Need someone to mount my 65\" TV",
            "Looking for a deep clean before move-in",
            "Need junk removed from garage",
            "Help moving furniture to new apartment",
            "Looking for home-cooked weekly meals",
            "Need drywall patch in living room",
            "Looking for someone to hang gallery wall",
            "Need help with IKEA wardrobe assembly",
        ]

        for _ in range(options['requests']):
            cat = random.choice(CATEGORIES)
            zip_code = random.choice(LA_ZIPS)
            ServiceRequest.objects.create(
                title=random.choice(REQUEST_TITLES),
                description=fake.paragraph(nb_sentences=2),
                category=cat,
                zip_code=zip_code,
                posted_by=random.choice(users),
            )

        self.stdout.write(self.style.SUCCESS(f"Created {options['requests']} service requests."))

        #Job History
        COMPANIES = [
            "TaskRabbit", "Handy", "Amazon Flex", "Instacart",
            "DoorDash", "Local Plumbing Co.", "GreenThumb Landscaping",
            "Sparkling Clean LLC", "QuickMove Helpers", "HomeFix Pros",
        ]

        for _ in range(options['jobs']):
            user = random.choice(users)
            start = fake.date_between(start_date='-12m', end_date='-1m')
            is_current = random.random() > 0.6
            end = None if is_current else fake.date_between(start_date=start, end_date='today')
            cat = random.choice(CATEGORIES)
            title_map = {
                'assembly': 'Furniture Assembler',
                'mounting': 'Installation Technician',
                'cleaning': 'Cleaning Specialist',
                'outdoor-maintenance': 'Lawn Care Technician',
                'repairs': 'Handyman',
                'moving': 'Moving Assistant',
                'cooking': 'Personal Chef',
            }
            UserJobHistory.objects.create(
                user=user,
                job_title=title_map[cat],
                company=random.choice(COMPANIES),
                location=f"Los Angeles, CA {random.choice(LA_ZIPS)}",
                description=fake.paragraph(nb_sentences=1),
                start_date=start,
                end_date=end,
                is_current=is_current,
            )

        self.stdout.write(self.style.SUCCESS(f"Created {options['jobs']} job history entries."))
        self.stdout.write(self.style.SUCCESS("Seeding complete!"))