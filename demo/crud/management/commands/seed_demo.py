"""Populate the demo database with a small, realistic relational dataset.

Deterministic and idempotent — running it repeatedly yields the same data
(it clears the crud tables first). Also ensures a demo superuser exists.

    python manage.py seed_demo
"""

import datetime
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from crud.models import Company, Contact, Project, Tag, Task

COMPANIES = [
    ("Acme Technology", "tech", "https://acme.example"),
    ("Globex Finance", "finance", "https://globex.example"),
    ("Initech Software", "tech", "https://initech.example"),
    ("Umbrella Health", "health", "https://umbrella.example"),
    ("Wayne Media", "media", "https://wayne.example"),
    ("Stark Retail", "retail", "https://stark.example"),
]

TAGS = [
    ("Frontend", "primary"), ("Backend", "info"), ("Design", "success"),
    ("Urgent", "danger"), ("Research", "warning"), ("Infra", "secondary"),
]

CONTACT_NAMES = [
    "Ada Lovelace", "Grace Hopper", "Alan Turing", "Linus Torvalds",
    "Guido van Rossum", "Margaret Hamilton", "Ken Thompson", "Barbara Liskov",
    "Donald Knuth", "Tim Berners-Lee", "Dennis Ritchie", "Radia Perlman",
    "Brian Kernighan", "Anita Borg", "Edsger Dijkstra", "Katherine Johnson",
    "James Gosling", "Hedy Lamarr", "Bjarne Stroustrup", "Adele Goldberg",
    "John McCarthy", "Frances Allen", "Vint Cerf", "Joan Clarke",
]
ROLES = ["admin", "editor", "viewer"]
CONTACT_STATUS = ["active", "pending", "disabled"]

PROJECTS = [
    ("Website Redesign", "active"), ("Mobile App v2", "planning"),
    ("Data Warehouse", "active"), ("Payment Gateway", "on_hold"),
    ("Brand Refresh", "completed"), ("Customer Portal", "active"),
    ("Analytics Pipeline", "planning"), ("Security Audit", "active"),
    ("Inventory System", "on_hold"), ("Marketing Campaign", "completed"),
]

TASK_TITLES = [
    "Kick-off meeting", "Requirements gathering", "Design mockups",
    "Implementation", "Code review", "QA testing", "Deployment",
    "Documentation", "Stakeholder demo", "Retrospective",
]
TASK_STATUS_CYCLE = ["done", "done", "in_progress", "todo"]


class Command(BaseCommand):
    help = "Seed the demo database with a relational sample dataset (idempotent)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--no-superuser", action="store_true",
            help="Do not create the demo superuser (admin / adminpass).",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        today = datetime.date.today()

        # Clean slate (child → parent order).
        Task.objects.all().delete()
        Project.objects.all().delete()
        Contact.objects.all().delete()
        Tag.objects.all().delete()
        Company.objects.all().delete()

        companies = [
            Company.objects.create(name=n, industry=ind, website=url)
            for n, ind, url in COMPANIES
        ]
        tags = [Tag.objects.create(name=n, color=c) for n, c in TAGS]

        contacts = []
        for i, name in enumerate(CONTACT_NAMES):
            first = name.split()[0].lower()
            contacts.append(Contact.objects.create(
                name=name,
                email=f"{first}@{companies[i % len(companies)].name.split()[0].lower()}.example",
                role=ROLES[i % len(ROLES)],
                status=CONTACT_STATUS[i % len(CONTACT_STATUS)],
                company=companies[i % len(companies)],
            ))

        task_total = 0
        for i, (pname, status) in enumerate(PROJECTS):
            start = today - datetime.timedelta(days=60 - i * 5)
            project = Project.objects.create(
                name=pname,
                company=companies[i % len(companies)],
                status=status,
                budget=Decimal(25000 + i * 7500),
                start_date=start,
                due_date=start + datetime.timedelta(days=90),
                lead=contacts[i % len(contacts)],
            )
            team = [contacts[(i + k) % len(contacts)] for k in range(4)]
            project.team.set(team)
            project.tags.set([tags[i % len(tags)], tags[(i + 2) % len(tags)]])

            for k in range(4):
                title = TASK_TITLES[(i + k) % len(TASK_TITLES)]
                Task.objects.create(
                    project=project,
                    title=title,
                    status=TASK_STATUS_CYCLE[k % len(TASK_STATUS_CYCLE)],
                    assignee=team[k % len(team)],
                    due_date=start + datetime.timedelta(days=15 * (k + 1)),
                    order=k,
                )
                task_total += 1

        verbose = int(options.get("verbosity", 1))
        if not options["no_superuser"]:
            User = get_user_model()
            user, created = User.objects.get_or_create(
                username="admin",
                defaults={"is_staff": True, "is_superuser": True, "email": "admin@example.com"},
            )
            if created:
                user.set_password("adminpass")
                user.save()
                if verbose:
                    self.stdout.write(self.style.WARNING("Created superuser  admin / adminpass"))

        if verbose:
            self.stdout.write(self.style.SUCCESS(
                f"Seeded {len(companies)} companies, {len(tags)} tags, {len(contacts)} contacts, "
                f"{len(PROJECTS)} projects, {task_total} tasks."
            ))
